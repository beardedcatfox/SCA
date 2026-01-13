from django.db import models

from cats.models import Cat


class Mission(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.SET_NULL, null=True, blank=True, related_name='missions')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Mission {self.id} - {'Completed' if self.is_completed else 'Active'}"


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='targets')
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.country})"

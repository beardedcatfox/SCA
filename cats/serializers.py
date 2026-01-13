from rest_framework import serializers
from .models import Cat
from .validators import validate_breed

class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = '__all__'
        read_only_fields = ['is_available']

    def validate_breed(self, value):
        validate_breed(value)
        return value

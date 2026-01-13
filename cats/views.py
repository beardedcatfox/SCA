from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Cat
from .serializers import CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.missions.filter(is_completed=False).exists():
            return Response(
                {"error": "Cannot delete cat with active missions."},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Mission, Target
from .serializers import MissionSerializer, TargetSerializer, AssignCatSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.cat:
            return Response(
                {"error": "Cannot delete a mission assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        serializer = AssignCatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(mission, serializer.validated_data)
            return Response(MissionSerializer(mission).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TargetViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    def update(self, request, *args, **kwargs):
        target = self.get_object()
        if target.is_completed or target.mission.is_completed:
            return Response(
                {"error": "Cannot update a completed target or mission."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        target = self.get_object()
        if target.mission.is_completed:
            return Response(
                {"error": "Mission already completed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        target.is_completed = True
        target.save()

        if all(t.is_completed for t in target.mission.targets.all()):
            target.mission.is_completed = True
            target.mission.cat.is_available = True
            target.mission.cat.save()
            target.mission.save()
        return Response(TargetSerializer(target).data)

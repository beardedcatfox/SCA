from rest_framework import serializers

from .models import Mission, Target
from cats.models import Cat


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_completed']

    def validate(self, data):
        instance = self.instance
        if instance:
            if instance.is_completed or instance.mission.is_completed:
                raise serializers.ValidationError("Cannot update a completed target or mission.")
        return data


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'is_completed', 'targets', 'created_at', 'updated_at']
        read_only_fields = ['is_completed', 'created_at', 'updated_at']

    def validate_targets(self, value):
        if len(value) < 1 or len(value) > 3:
            raise serializers.ValidationError("A mission must have between 1 and 3 targets.")
        return value

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission


class AssignCatSerializer(serializers.Serializer):
    cat_id = serializers.PrimaryKeyRelatedField(queryset=Cat.objects.filter(is_available=True))

    def update(self, instance, validated_data):
        cat = validated_data['cat_id']
        if instance.cat:
            raise serializers.ValidationError("Mission already assigned to a cat.")
        if not cat.is_available:
            raise serializers.ValidationError("Cat is not available.")
        instance.cat = cat
        cat.is_available = False
        cat.save()
        instance.save()
        return instance

from .models import (
    ProjectType,
    Project,
    Person,
    ProjectSet,
    ProjectArea,
    BudgetItem,
    Task,
    ProjectPhase,
    ProjectPriority,
    TaskStatus,
    Note,
)
from rest_framework import serializers
from django.db.models import Q


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        exclude = ["createdDate", "updatedDate"]


class ProjectPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhase
        exclude = ["createdDate", "updatedDate"]


class ProjectPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPriority
        exclude = ["createdDate", "updatedDate"]


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person

        exclude = ["createdDate", "updatedDate"]


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType

        exclude = ["createdDate", "updatedDate"]


class BudgetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetItem

        exclude = ["createdDate", "updatedDate"]


class ProjectAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectArea

        exclude = ["createdDate", "updatedDate", "location"]


class ProjectSetGetSerializer(serializers.ModelSerializer):
    sapProjects = serializers.SerializerMethodField()
    sapNetworks = serializers.SerializerMethodField()
    phase = ProjectPhaseSerializer(read_only=True)

    class Meta:
        model = ProjectSet

        exclude = ["createdDate", "updatedDate"]

    def get_sapNetworks(self, obj):
        return [
            network
            for obj in obj.project_set.all()
            .filter(~Q(sapNetwork=None))
            .values("sapNetwork")
            for network in obj["sapNetwork"]
        ]

    def get_sapProjects(self, obj):
        return [
            project
            for obj in obj.project_set.all()
            .filter(~Q(sapNetwork=None))
            .values("sapProject")
            for project in obj["sapProject"]
        ]


class ProjectSetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSet

        exclude = ["createdDate", "updatedDate"]


class ProjectGetSerializer(serializers.ModelSerializer):
    projectReadiness = serializers.SerializerMethodField()
    projectSet = ProjectSetCreateSerializer(read_only=True)
    siteId = BudgetItemSerializer(read_only=True)
    area = ProjectAreaSerializer(read_only=True)
    type = ProjectTypeSerializer(read_only=True)
    priority = ProjectPrioritySerializer(read_only=True)
    phase = ProjectPhaseSerializer(read_only=True)
    personPlanning = PersonSerializer(read_only=True)
    personProgramming = PersonSerializer(read_only=True)
    personConstruction = PersonSerializer(read_only=True)

    class Meta:
        model = Project

        exclude = ["createdDate", "updatedDate"]

    def get_projectReadiness(self, obj):
        return obj.projectReadiness()


class ProjectCreateSerializer(serializers.ModelSerializer):
    projectReadiness = serializers.SerializerMethodField()

    class Meta:
        model = Project

        exclude = ["createdDate", "updatedDate"]

    def get_projectReadiness(self, obj):
        return obj.projectReadiness()


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person

        exclude = ["createdDate", "updatedDate"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task

        exclude = ["createdDate", "updatedDate"]


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = ["createdDate", "updatedDate"]

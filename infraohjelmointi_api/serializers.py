from .models import ProjectType, Project, Person, ProjectSet, ProjectArea, BudgetItem
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    projectReadiness = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

        lookup_field = "type"
        extra_kwargs = {"url": {"lookup_field": "type"}}

    def get_projectReadiness(self, obj):
        return obj.projectReadiness()


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = "__all__"


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


class ProjectSetSerializer(serializers.ModelSerializer):
    sapProjects = serializers.SerializerMethodField()
    sapNetworks = serializers.SerializerMethodField()

    class Meta:
        model = ProjectSet
        fields = "__all__"

    def get_sapProjects(self, obj):
        return obj.sapProjects()

    def get_sapNetworks(self, obj):
        return obj.sapNetworks()


class ProjectAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectArea
        fields = "__all__"


class BudgetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetItem
        fields = "__all__"

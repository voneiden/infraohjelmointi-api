# Generated by Django 4.1.3 on 2022-12-21 14:12

from django.db import migrations


def populate_ProjectQualityLevel_data(apps, schema_editor):
    ProjectQualityLevel = apps.get_model("infraohjelmointi_api", "ProjectQualityLevel")
    qualityLevels = [
        "1class",
        "2class",
        "3class",
        "A1",
        "A2",
        "A3",
        "B",
        "C",
    ]
    for level in qualityLevels:
        ProjectQualityLevel.objects.create(value=level)


def populate_ConstructionPhase_data(apps, schema_editor):
    ConstructionPhase = apps.get_model("infraohjelmointi_api", "ConstructionPhase")
    constructionPhases = [
        "planning",
        "contractCalculation",
        "additionalWork",
        "reception",
    ]
    for phase in constructionPhases:
        ConstructionPhase.objects.create(value=phase)


def populate_PlanningPhase_data(apps, schema_editor):
    PlanningPhase = apps.get_model("infraohjelmointi_api", "PlanningPhase")
    PlanningPhases = [
        "projectPlanning",
        "generalDesign",
        "parkPlaning",
        "trafficPlanning",
        "streetDesign",
        "buildingDesign",
    ]
    for phase in PlanningPhases:
        PlanningPhase.objects.create(value=phase)


class Migration(migrations.Migration):

    dependencies = [
        (
            "infraohjelmointi_api",
            "0017_constructionphase_planningphase_projectqualitylevel_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(populate_ProjectQualityLevel_data),
        migrations.RunPython(populate_PlanningPhase_data),
        migrations.RunPython(populate_ConstructionPhase_data),
    ]

# Generated by Django 4.1.3 on 2022-12-02 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("infraohjelmointi_api", "0005_alter_note_project_alter_note_updatedby"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="sapProject",
        ),
        migrations.AddField(
            model_name="project",
            name="sapProject",
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ]

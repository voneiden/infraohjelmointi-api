# Generated by Django 4.1.3 on 2022-11-22 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "infraohjelmointi_api",
            "0002_budgetitem_person_projectarea_projectset_task_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectset",
            name="responsiblePerson",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="infraohjelmointi_api.person",
            ),
        ),
    ]

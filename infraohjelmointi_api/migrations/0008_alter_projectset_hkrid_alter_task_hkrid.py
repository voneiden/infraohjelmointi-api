# Generated by Django 4.1.3 on 2022-12-09 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infraohjelmointi_api', '0007_project_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectset',
            name='hkrId',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='hkrId',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]

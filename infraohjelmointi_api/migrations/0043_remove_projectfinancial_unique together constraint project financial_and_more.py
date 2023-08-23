# Generated by Django 4.1.3 on 2023-08-22 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infraohjelmointi_api', '0042_projecthashtag_archived_alter_projecthashtag_value'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='projectfinancial',
            name='Unique together Constraint Project Financial',
        ),
        migrations.AddField(
            model_name='projectfinancial',
            name='forFrameView',
            field=models.BooleanField(default=False),
        ),
        migrations.AddConstraint(
            model_name='projectfinancial',
            constraint=models.UniqueConstraint(fields=('project', 'year', 'forFrameView'), name='Unique together Constraint Project Financial'),
        ),
    ]

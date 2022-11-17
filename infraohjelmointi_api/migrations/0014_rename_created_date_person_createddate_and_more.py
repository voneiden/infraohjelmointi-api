# Generated by Django 4.1.3 on 2022-11-17 12:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('infraohjelmointi_api', '0013_remove_project_unique together constraint project_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='created_date',
            new_name='createdDate',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='updated_date',
            new_name='updatedDate',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='created_date',
            new_name='createdDate',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='updated_date',
            new_name='updatedDate',
        ),
        migrations.AddField(
            model_name='budgetitem',
            name='createdDate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='budgetitem',
            name='updatedDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='projectarea',
            name='createdDate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectarea',
            name='updatedDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='projectset',
            name='createdDate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectset',
            name='updatedDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='projecttype',
            name='createdDate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projecttype',
            name='updatedDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='task',
            name='createdDate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='updatedDate',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

# Generated by Django 4.1.3 on 2022-12-19 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infraohjelmointi_api', '0015_projectcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='category_temp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='infraohjelmointi_api.projectcategory'),
        ),
    ]

# Generated by Django 4.2.2 on 2023-08-08 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0004_rename_stateoforigin_studentmodel_age_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='phone',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]

# Generated by Django 4.2.2 on 2023-08-08 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0002_user_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Males'), ('F', 'Female')], max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='stateOfOrigin',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='surname',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]

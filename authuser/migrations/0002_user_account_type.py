# Generated by Django 4.2.2 on 2023-08-07 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='account_type',
            field=models.CharField(blank=True, choices=[('student', 'Student'), ('lecturer', 'Lecturer')], max_length=250, null=True),
        ),
    ]

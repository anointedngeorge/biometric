# Generated by Django 4.2.2 on 2023-08-15 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_createattendance_time_elapsed2'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestTaskOnHeroku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=500)),
            ],
        ),
    ]

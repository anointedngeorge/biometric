# Generated by Django 4.2.2 on 2023-08-12 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0010_alter_user_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='account_type2',
            field=models.CharField(choices=[('', '-----'), ('student', 'Student'), ('lecturer', 'Lecturer')], default='', max_length=250),
        ),
    ]

# Generated by Django 5.1.5 on 2025-01-27 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_register_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]

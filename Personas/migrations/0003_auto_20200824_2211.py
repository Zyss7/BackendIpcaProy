# Generated by Django 3.1 on 2020-08-25 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Personas', '0002_auto_20200824_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='discapacidad',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]

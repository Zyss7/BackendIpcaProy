# Generated by Django 3.1.5 on 2021-02-28 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Matriculas', '0010_auto_20210223_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumnoaula',
            name='amie',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alumnoaula',
            name='grado_dependencia',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alumnoaula',
            name='mies',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alumnoaula',
            name='tipo_familia',
            field=models.TextField(blank=True, null=True),
        ),
    ]

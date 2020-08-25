# Generated by Django 3.1 on 2020-08-25 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Personas', '0004_auto_20200824_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discapacidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auth_estado', models.CharField(default='A', max_length=10)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('porcentaje', models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='persona',
            name='discapacidad',
        ),
        migrations.AddField(
            model_name='persona',
            name='tiene_discapacidad',
            field=models.CharField(default='NO', max_length=10),
        ),
        migrations.AddField(
            model_name='persona',
            name='discapacidades',
            field=models.ManyToManyField(blank=True, to='Personas.Discapacidad'),
        ),
    ]

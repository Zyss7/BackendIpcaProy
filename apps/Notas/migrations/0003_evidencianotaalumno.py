# Generated by Django 3.1.5 on 2021-02-23 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Notas', '0002_notaalumno_titulo'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvidenciaNotaAlumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auth_estado', models.CharField(default='A', max_length=10)),
                ('url', models.URLField()),
                ('nota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidencias', to='Notas.notaalumno')),
            ],
            options={
                'db_table': 'EvidenciasNotasAlumno',
            },
        ),
    ]
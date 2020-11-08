from rest_framework import serializers
from rest_framework.serializers import ALL_FIELDS

from core.models import Tarea, Docente, Persona, Aula, Alumno, Discapacidad


class TareaSerializer(serializers.ModelSerializer):
    # estudiantes = EstudianteTareaSerializer(many=True)

    class Meta:
        model = Tarea
        fields = ALL_FIELDS


class DiscapacidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discapacidad
        fields = ALL_FIELDS


class PersonaSerializer(serializers.ModelSerializer):
    # discapacidades = DiscapacidadSerializer(many=True)
    discapacidades = serializers.SerializerMethodField()

    class Meta:
        model = Persona
        fields = ALL_FIELDS

    def get_discapacidades(self, obj: Persona):
        return [discapacidad.nombre for discapacidad in obj.discapacidades.all()]


class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = ALL_FIELDS


class DocenteSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()
    aulas = serializers.SerializerMethodField()

    class Meta:
        model = Docente
        fields = ALL_FIELDS

    def get_aulas(self, obj):
        aulas = Aula.objects.filter(docentes__in=[obj], periodo__estado='ABIERTO')
        return [aula.mapper() for aula in aulas]


class AlumnoSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()

    class Meta:
        model = Alumno
        fields = ALL_FIELDS

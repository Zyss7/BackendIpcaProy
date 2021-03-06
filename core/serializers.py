from rest_framework import serializers
from rest_framework.serializers import ALL_FIELDS

from core.models import Tarea, Personal, Persona, Aula, Alumno, Discapacidad, ListaReproduccion, PeriodoLectivo, Usuario


class TareaSerializer(serializers.ModelSerializer):
    # estudiantes = EstudianteTareaSerializer(many=True)

    class Meta:
        model = Tarea
        fields = ALL_FIELDS


class TareaAlumnoSerializer(serializers.ModelSerializer):
    estado = serializers.SerializerMethodField(read_only=True)
    show = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tarea
        fields = ALL_FIELDS
        identificacion = ''

    def get_estado(self, obj: Tarea):
        return 'PENDIENTE'

    def get_show(self, obj: Tarea):
        return False


class DiscapacidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discapacidad
        fields = ALL_FIELDS


class PersonaSerializer(serializers.ModelSerializer):
    # discapacidades = DiscapacidadSerializer(many=True)
    discapacidades = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    usuario = serializers.SerializerMethodField()

    class Meta:
        model = Persona
        fields = ALL_FIELDS

    def get_discapacidades(self, obj: Persona):
        return obj.discapacidades.values_list('nombre', flat=True).all()

    def get_str(self, obj: Persona):
        return obj.__str__()

    def get_usuario(self, obj: Persona):
        usuario = Usuario.objects.values('username', ).filter(
            persona__identificacion=obj.identificacion
        ).first()
        return usuario


class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = ALL_FIELDS


class DocenteSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()
    aulas = serializers.SerializerMethodField()

    class Meta:
        model = Personal
        fields = ALL_FIELDS

    def get_aulas(self, obj):
        aulas = Aula.objects.filter(docentes__in=[obj], periodo__estado=PeriodoLectivo.EstadosPeriodo.ABIERTO.value)
        return [aula.mapper() for aula in aulas]
        # return []


class AlumnoSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()

    class Meta:
        model = Alumno
        fields = ALL_FIELDS


class ListaReproduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaReproduccion
        fields = ALL_FIELDS


class UsuarioSerializaer(serializers.ModelSerializer):
    persona = PersonaSerializer()

    class Meta:
        model = Usuario
        # fields = ALL_FIELDS
        exclude = ('password',)

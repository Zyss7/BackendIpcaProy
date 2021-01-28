from django.db import models

from BackStrawBerryPy.models import BaseModel
from apps.Personas.models import Personal, Alumno


# Create your models here.


class PeriodoLectivo(BaseModel):
    class EstadosPeriodo(models.IntegerChoices):
        CERRADO = 0
        ABIERTO = 1

    nombre = models.CharField(max_length=155)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.PositiveSmallIntegerField(default=1, choices=EstadosPeriodo.choices)
    fecha_fin_clases = models.DateField()
    observaciones = models.TextField(null=True, blank=True)

    # responsables = models.JSONField(null=True, blank=True)

    coordinador = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='coordinador')
    sub_coordinador = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='sub_coordinador')

    # @staticmethod
    # def cerrar_periodo(id):
    #     periodo: PeriodoLectivo = PeriodoLectivo.objects.filter(
    #         pk=id,
    #         estado=PeriodoLectivo.EstadosPeriodo.ABIERTO.value
    #     ).first()
    #
    #     matriculas: QuerySet[AlumnoAula] = AlumnoAula.objects.filter(
    #         aula__periodo__id=id,
    #         estado_matricula=AlumnoAula.EstadosMatricula.CREADA.value
    #     )
    #
    #     for matricula in matriculas:
    #         matricula.estado_matricula = AlumnoAula.EstadosMatricula.FINALIZADA.value
    #
    #     AlumnoAula.objects.bulk_update(matriculas, ['estado_matricula'])
    #
    #     return dict(periodo=periodo, matriculas=matriculas)

    class Meta:
        db_table = 'PeriodoLectivos'


class Aula(BaseModel):
    nombre = models.CharField(max_length=50)
    # numero = models.PositiveSmallIntegerField(null=True)
    # TODO: averiguar si tiene jornada
    capacidad = models.PositiveSmallIntegerField()
    grado = models.PositiveSmallIntegerField()
    alumnos = models.ManyToManyField(Alumno, through='AlumnoAula', blank=True)
    docentes = models.ManyToManyField(Personal)
    periodo = models.ForeignKey(PeriodoLectivo, on_delete=models.CASCADE)
    observaciones = models.TextField(null=True, blank=True)
    jornada = models.CharField(max_length=50, default='MATUTINA')

    class Meta:
        db_table = 'Aulas'


class Materia(BaseModel):
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=20)
    grado = models.PositiveSmallIntegerField()
    horas_presencial = models.PositiveSmallIntegerField()
    descripcion = models.TextField(null=True, blank=True)
    objetivo = models.TextField(null=True, blank=True)
    objetivo_especifico = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Materias'


# MATRICULA
class AlumnoAula(BaseModel):
    class EstadosMatricula(models.IntegerChoices):
        CREADA = 0
        ANULADA = 1
        FINALIZADA = 2

    diagnostico_clinico = models.TextField(null=True, blank=True)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    numero_matricula = models.CharField(max_length=155, default='', unique=True)
    matricula = models.TextField(null=True, blank=True)
    aporte_voluntario = models.DecimalField(decimal_places=2, max_digits=6)
    tratamiento = models.TextField(null=True, blank=True)

    total_faltas = models.PositiveSmallIntegerField(default=0)

    diagnostico_final = models.TextField(null=True, blank=True)

    motivo_anulacion = models.TextField(null=True, blank=True)

    estado_matricula = models.PositiveSmallIntegerField(
        default=EstadosMatricula.CREADA.value,
        choices=EstadosMatricula.choices
    )

    def generar_numero_matricula(self):
        return f'M-{self.pk}{self.alumno.id}{self.aula.pk}{self.alumno.persona.pk}'

    def verificar_matricula_creada(self):
        return False

    def save(self, *args, **kwargs):
        is_nueva = self.pk is None
        matricula = super(AlumnoAula, self).save(*args, **kwargs)

        if is_nueva:
            self.numero_matricula = self.generar_numero_matricula()
            self.matricula = self.numero_matricula
            self.save()

        return matricula

    '''
        PREGUNTAS:
            - En caso de retirarce del IPCA que ocurre con la matricula?
    '''

    class Meta:
        db_table = 'AlumnoAulas'


class Falta(BaseModel):
    alumno = models.ForeignKey(AlumnoAula, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField(null=True)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'FaltasAlumno'


class NotaAlumno(BaseModel):
    alumno_aula = models.ForeignKey(AlumnoAula, on_delete=models.CASCADE)

    class Meta:
        db_table = 'NotaAlumnos'


# MallaAlumno
'''
class NotaMateria(BaseModel):
    alumno_aula = models.ForeignKey(AlumnoAula, on_delete=models.CASCADE)
    valor = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    observaciones = models.TextField(null=True, blank=True)
    materia = models.JSONField()
    # materia_fk = models.ForeignKey(Materia, on_delete=models.CASCADE)
    notas = models.JSONField(null=True, blank=True)


        PREGUNTAS:
            - Formato de notas?
            - Tipos de reportes que necesitan?
            - Tienen minimos y maximo?

        matematica:
            valorFinal: 100,
            notas:[
                {
                    titulo:'Paseo1'
                    valor:10
                    fechaRegistro:2020-10-12-08:00:45,
                    descripcion:'COMENTARIOS DOCENTE',
                    usuario: objUser
                }
            ]


    class Meta:
        db_table = 'NotaMateria'
'''

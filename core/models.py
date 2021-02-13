from django.db import models

# Create your models here.
AUTH_ESTADOS = {
    'ACTIVO': 'A',
    'INACTIVO': 'I'
}


class Tarea(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    titulo = models.TextField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    descripcion_hablada = models.TextField(null=True, blank=True)

    fecha_entrega = models.DateTimeField(null=True, blank=True)

    docente = models.JSONField(null=True, blank=True)
    estudiantes = models.JSONField(null=True, blank=True)
    alumnos = models.JSONField(null=True, blank=True)
    estado_envio = models.CharField(max_length=20, default='PENDIENTE')

    class Meta:
        db_table = 'MLN_Tareas'
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ("-created_at",)


'''
TODO: CREAR UN CRON para eliminar las listas de reproduccion que llevan eliminadas mas de 3 semanas
'''


class ListaReproduccion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # TODO: validar el unique en back y front
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(null=True, blank=True)
    videos = models.JSONField(null=True, blank=True)
    alumnos = models.JSONField(null=True, blank=True)
    creador = models.JSONField(null=True, blank=True)

    auth_estado = models.CharField(max_length=10, default='A')

    class Meta:
        db_table = 'ListaReproduccion'
        ordering = ("titulo",)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_estado = models.CharField(max_length=10, default='A')

    class Meta:
        abstract = True

    def __to_json__(self):
        obj_json = self.__dict__
        obj_json['created_at'] = self.created_at.isoformat()
        obj_json['updated_at'] = self.updated_at.isoformat()
        obj_json.pop('_state')
        return obj_json


class FuncionPersonal(BaseModel):
    DOCENTE: str = 'docente'
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=50)
    descripcion = models.TextField()

    class Meta:
        db_table = 'RolesPersonal'
        managed = False


class Discapacidad(BaseModel):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Discapacidades'
        managed = False


class Persona(BaseModel):
    identificacion = models.CharField(max_length=30, unique=True)
    tipo_identificacion = models.CharField(max_length=20, )
    primer_nombre = models.CharField(max_length=30)
    segundo_nombre = models.CharField(max_length=30)
    primer_apellido = models.CharField(max_length=30)
    segundo_apellido = models.CharField(max_length=30)

    pais_nacimiento = models.CharField(max_length=30, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    genero = models.CharField(max_length=10, )
    estado_civil = models.CharField(max_length=20, null=True, blank=True)

    tiene_discapacidad = models.CharField(max_length=10, default="NO")
    discapacidades = models.ManyToManyField(Discapacidad, blank=True)
    carnet_conadis = models.CharField(max_length=50, default='NO REGISTRA')

    porcentaje_discapacidad = models.PositiveSmallIntegerField(default=0)
    etnia = models.CharField(max_length=30, null=True, blank=True)

    tipo_sangre = models.CharField(max_length=30, null=True, blank=True)

    pais_residencia = models.CharField(max_length=150, null=True, blank=True)
    provincia_residencia = models.CharField(max_length=150, null=True, blank=True)
    canton_residencia = models.CharField(max_length=150, null=True, blank=True)
    parroquia_residencia = models.CharField(max_length=150, null=True, blank=True)
    direccion_domiciliaria = models.TextField(null=True, blank=True)

    telefono = models.CharField(max_length=20, null=True, blank=True)
    celular_uno = models.CharField(max_length=20, null=True, blank=True)
    celular_dos = models.CharField(max_length=20, null=True, blank=True)
    correo = models.CharField(max_length=30, null=True, blank=True)

    foto = models.URLField(null=True, blank=True)
    extras = models.JSONField(null=True, blank=True)

    def full_name(self):
        return f'{self.primer_nombre} {self.primer_apellido}'

    def __str__(self):
        return f'{self.identificacion} {self.full_name()}'

    class Meta:
        db_table = 'Personas'
        managed = False


class Personal(BaseModel):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    funciones = models.ManyToManyField(FuncionPersonal, blank=True)
    titulo = models.CharField(max_length=150)
    tipo_titulo = models.CharField(max_length=150)
    area_de_trabajo = models.TextField(null=True, blank=True, default='NO REGISTRA')

    class Meta:
        db_table = 'Personal'
        managed = False

    def full_name(self):
        return self.persona.full_name()

    def __str__(self):
        return self.persona.__str__()


class Alumno(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='alumno')

    padre = models.JSONField(null=True, blank=True)

    madre = models.JSONField(null=True, blank=True)

    representante = models.JSONField(null=True, blank=True)

    contacto_emergencia = models.JSONField(null=True, blank=True)

    observaciones = models.TextField(null=True, blank=True)

    historia_clinica = models.CharField(max_length=20, null=True, blank=True)

    trastornos_asociados = models.TextField(null=True, blank=True)

    grado_dependencia = models.TextField(null=True, blank=True)

    bono = models.CharField(max_length=50, default="Ninguno")
    tipo_bono = models.CharField(max_length=50)
    afiliacion_iess = models.CharField(max_length=10)
    quintil_pobreza = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'Alumnos'

    def mapper(self):
        persona = self.persona
        return dict(
            id=self.id,
            id_persona=persona.id,
            identificacion=persona.identificacion,
            primer_nombre=persona.primer_nombre,
            segundo_nombre=persona.segundo_nombre,
            primer_apellido=persona.primer_apellido,
            segundo_apellido=persona.segundo_apellido,
            str=persona.__str__()
        )


class Aula(models.Model):
    nombre = models.CharField(max_length=50)
    capacidad = models.PositiveSmallIntegerField()
    grado = models.PositiveSmallIntegerField()
    alumnos = models.ManyToManyField(Alumno, through='AlumnoAula', blank=True)
    docentes = models.ManyToManyField(Personal)
    periodo = models.ForeignKey('PeriodoLectivo', on_delete=models.CASCADE)
    observaciones = models.TextField(null=True, blank=True)
    jornada = models.CharField(max_length=50, default='MATUTINA')

    class Meta:
        managed = False
        db_table = 'Aulas'

    def mapper(self):
        return dict(
            id=self.id,
            nombre=self.nombre,
            grado=self.grado,
            periodo=self.periodo.mapper(),
            docentes=[docente.persona.__str__() for docente in self.docentes.all()],
            observaciones=self.observaciones,
            alumnos=[alumno.mapper() for alumno in self.alumnos.all()]
        )


class AlumnoAula(BaseModel):
    diagnostico_clinico = models.TextField(null=True, blank=True)

    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    numero_matricula = models.CharField(max_length=155, default='')
    matricula = models.TextField(null=True, blank=True)
    aporte_voluntario = models.DecimalField(decimal_places=2, max_digits=6)
    tratamiento = models.TextField(null=True, blank=True)
    info_faltas = models.JSONField(null=True, blank=True)
    diagnostico_final = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'AlumnoAulas'


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
    coordinador = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='coordinador')
    sub_coordinador = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='sub_coordinador')

    class Meta:
        managed = False
        db_table = 'PeriodoLectivos'

    def mapper(self):
        return dict(
            nombre=self.nombre,
            fecha_inicio=self.fecha_inicio,
            fecha_fin=self.fecha_fin,
            estado=self.estado,
        )

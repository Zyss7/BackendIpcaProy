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


class Alumno(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    auth_estado = models.CharField(max_length=10)
    padre = models.JSONField(blank=True, null=True)
    madre = models.JSONField(blank=True, null=True)
    representante = models.JSONField(blank=True, null=True)
    contacto_emergencia = models.JSONField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    persona = models.ForeignKey('Persona', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Alumno'

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


class AlumnoAula(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    auth_estado = models.CharField(max_length=10)
    nota_final = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    numero_faltas = models.SmallIntegerField()
    tratamiento = models.TextField()
    diagnostico = models.TextField()
    diagnostico_final = models.TextField(blank=True, null=True)
    aporte_voluntario = models.DecimalField(max_digits=6, decimal_places=2)
    alumno = models.ForeignKey(Alumno, models.DO_NOTHING)
    aula = models.ForeignKey('Aula', models.DO_NOTHING)
    matricula = models.TextField()
    faltas = models.JSONField()
    numero_matricula = models.CharField(max_length=155)

    class Meta:
        managed = False
        db_table = 'AlumnoAula'


class Aula(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    auth_estado = models.CharField(max_length=10)
    nombre = models.CharField(max_length=50)
    capacidad = models.SmallIntegerField()
    grado = models.SmallIntegerField()
    observaciones = models.TextField(blank=True, null=True)
    periodo = models.ForeignKey('Periodolectivo', models.DO_NOTHING)
    jornada = models.CharField(max_length=50)
    docentes = models.ManyToManyField('Docente')
    alumnos = models.ManyToManyField(Alumno, through='AlumnoAula', blank=True)

    class Meta:
        managed = False
        db_table = 'Aula'

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


class Discapacidad(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    auth_estado = models.CharField(max_length=10)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    porcentaje = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Discapacidad'


class Docente(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    auth_estado = models.CharField(max_length=10)
    codigo = models.CharField(max_length=50, blank=True, null=True)
    tipo_titulo = models.CharField(max_length=120)
    titulo = models.CharField(max_length=255)
    observaciones = models.TextField(blank=True, null=True)
    persona = models.ForeignKey('Persona', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Docente'


class Materia(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    auth_estado = models.CharField(max_length=10)
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=20)
    grado = models.SmallIntegerField()
    horas_presencial = models.SmallIntegerField()
    descripcion = models.TextField(blank=True, null=True)
    objetivo = models.TextField(blank=True, null=True)
    objetivo_especifico = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Materia'


class Notamateria(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    auth_estado = models.CharField(max_length=10)
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)
    materia = models.JSONField()
    notas = models.JSONField()
    alumno_aula = models.ForeignKey(AlumnoAula, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'NotaMateri'


class Periodolectivo(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    auth_estado = models.CharField(max_length=10)
    nombre = models.CharField(max_length=155)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=30)
    fecha_fin_clases = models.DateField()
    observaciones = models.TextField(blank=True, null=True)
    responsables = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PeriodoLectivo'

    def mapper(self):
        return dict(
            nombre=self.nombre,
            fecha_inicio=self.fecha_inicio,
            fecha_fin=self.fecha_fin,
            estado=self.estado,
        )


class Persona(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    auth_estado = models.CharField(max_length=10)
    identificacion = models.CharField(unique=True, max_length=30)
    tipo_identificacion = models.CharField(max_length=20)
    primer_nombre = models.CharField(max_length=30)
    segundo_nombre = models.CharField(max_length=30)
    primer_apellido = models.CharField(max_length=30)
    segundo_apellido = models.CharField(max_length=30)
    genero = models.CharField(max_length=10)
    sexo = models.CharField(max_length=10)
    foto = models.CharField(max_length=200, blank=True, null=True)
    tipo_sangre = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    calle_principal = models.CharField(max_length=150, blank=True, null=True)
    calle_secundaria = models.CharField(max_length=150, blank=True, null=True)
    lugar_referencia = models.CharField(max_length=150, blank=True, null=True)
    numero_casa = models.CharField(max_length=30, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    correo = models.CharField(max_length=30, blank=True, null=True)
    tiene_discapacidad = models.CharField(max_length=10)
    carnet_conadis = models.CharField(max_length=50)
    porcentaje_discapacidad = models.SmallIntegerField()
    ocupacion = models.CharField(max_length=120, blank=True, null=True)
    nivel_formacion = models.CharField(max_length=255, blank=True, null=True)
    extras = models.JSONField(blank=True, null=True)
    discapacidades = models.ManyToManyField(Discapacidad, blank=True)

    class Meta:
        managed = False
        db_table = 'Persona'

    def __str__(self):
        return f"{self.identificacion} {self.primer_apellido} {self.primer_nombre}"

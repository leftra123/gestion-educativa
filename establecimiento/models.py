from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

def validar_encargado(value):
    encargado = Docente.objects.get(id=value)
    if encargado.rol != Docente.Rol.DOCENTE_AULA:
        raise ValidationError("El encargado debe ser un docente de aula.")

class Establecimiento(models.Model):
    RBD = models.IntegerField(primary_key=True)
    DV = models.CharField(max_length=1)
    nombre = models.CharField(max_length=100)
    encargado = models.ForeignKey('Docente', null=True, blank=True, on_delete=models.SET_NULL, validators=[validar_encargado])

    def __str__(self):
        return self.nombre

class Persona(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, null=True, blank=True, unique=True)
    id_extranjero = models.CharField(max_length=50, null=True, blank=True, unique=True)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Documento(models.Model):
    id = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Docente(Persona):
    rol = models.CharField(max_length=50)
    tipo_contrato = models.CharField(max_length=50)
    subvencion = models.CharField(max_length=50)
    horas_tipo_contrato = models.IntegerField(default=0)
    horas_subvencion_normal = models.IntegerField(default=0)
    horas_subvencion_sep = models.IntegerField(default=0)
    horas_subvencion_pie = models.IntegerField(default=0)

class DocenteEstablecimiento(models.Model):
    id = models.AutoField(primary_key=True)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    # total de horas por subvencion
    horas_subvencion_normal = models.IntegerField(default=0)
    horas_subvencion_sep = models.IntegerField(default=0)
    horas_subvencion_pie = models.IntegerField(default=0)
    # total de horas por tipo de contrato
    horas_tipo_contrato = models.IntegerField(default=0)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    

class Bienio(models.Model):
    id = models.AutoField(primary_key=True)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    horas_acumuladas = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.docente.nombre} - {self.fecha_inicio} - {self.fecha_fin}"

class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    grado = models.CharField(max_length=50)
    letra = models.CharField(max_length=1)
    seccion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.establecimiento.nombre}"

class Asistente(Persona):
    cargo = models.CharField(max_length=100)
    horas_semanales = models.PositiveIntegerField()
    fecha_contratacion = models.DateField()
    tipo_contrato = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nombre}" 

class AsistenteEstablecimiento(models.Model):
    id = models.AutoField(primary_key=True)
    asistente = models.ForeignKey(Asistente, on_delete=models.CASCADE)
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()

    def __str__(self):
        return f"{self.asistente.nombre} - {self.establecimiento.nombre} - {self.fecha_inicio} - {self.fecha_termino}"
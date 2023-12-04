from django.db import models


class Curso(models.Model):
    nombre = models.CharField(max_length=40)
    comision = models.IntegerField ()

class Profesores(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()
    profesion = models.CharField(max_length=30)

class Estudiantes(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()

class Entregable(models.Model):
    nombre = models.CharField(max_length=30)
    fecha_entrega = models.DateField()
    entregado = models.CharField(max_length=2)

from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader
from Pagina.forms import CursoForm
from Pagina.models import Curso,Profesores,Estudiantes,Entregable
import datetime

def inicio(request):
    return render(request, 'index.html')
 
    
def profesores(request):
    if request.method == 'POST':
        profesor = Profesores(
            nombre = request.POST["nombre"], 
            apellido = request.POST["apellido"],
            email = request.POST["email"],
            profesion = request.POST["profesion"]
            )
        profesor.save()
        return render(request, 'index.html')

    return render(request, "profesores.html")


def estudiantes(request):
    if request.method == 'POST':
        estudiante= Estudiantes(
            nombre = request.POST["nombre"], 
            apellido = request.POST["apellido"],
            email = request.POST["email"]
            )
        estudiante.save()
        return render(request, 'index.html')

    return render(request, "estudiantes.html")

def entregables(request):
    if request.method == 'POST':
        entregable= Entregable(
            nombre = request.POST["nombre"], 
            fecha_entrega = request.POST["fecha_entrega"],
            entregado = request.POST["entregado"]
            )
        entregable.save()
        return render(request, 'index.html')

    return render(request, "entregables.html")



def cursos(request):
    if request.method == 'POST':
        mi_formulario = CursoForm(request.POST)

        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data 
            curso = Curso(nombre=informacion["nombre"], comision=informacion["comision"])
            curso.save()
            return render(request, 'index.html')

    else:
        mi_formulario = CursoForm()
        return render(request, "cursos.html", {"mi_formulario" : mi_formulario})
    


def resultado_busqueda(request):
    cursos_encontrados = []
    nombre_curso = ""

    if 'Curso' in request.GET:
        nombre_curso = request.GET['Curso']
        cursos_encontrados = Curso.objects.filter(nombre__icontains=nombre_curso)

    return render(request, "resultado_busqueda.html", {'nombre_curso': nombre_curso, 'cursos': cursos_encontrados})



def buscar_curso(request):
    
    return render(request, "buscar_curso.html")


def buscar(request):
    cursos_encontrados = []
    nombre_curso = ""

    if 'Curso' in request.GET:
        nombre_curso = request.GET['Curso']
        cursos_encontrados = Curso.objects.filter(nombre__icontains=nombre_curso)

    return render(request, "buscar_curso.html", {'nombre_curso': nombre_curso, 'cursos': cursos_encontrados})
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader
from Pagina.forms import CursoForm, ProfesorForm, EntregableForm ,UserCreationFormCustom, UserEditForm  
from Pagina.models import Curso,Profesores,Estudiantes,Entregable
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from Pagina.models import Avatar
from django.contrib.auth.decorators import login_required



import datetime
@login_required

def inicio(request):
    return render(request, 'index.html')


def acerca_de_mi(request):
    return render(request, 'about.html')

def leer_mas(request):
    return render(request, 'leermas.html')
 
 

@login_required
def bienvenida(request):
    # Asegúrate de que el usuario tenga un avatar y que la imagen esté presente
    if hasattr(request.user, 'avatar') and request.user.avatar and request.user.avatar.imagen:
        avatar_url = request.user.avatar.imagen.url
    else:
        avatar_url = None
    
    mensaje_bienvenida = f"Bienvenido, {request.user.username}."

    return render(request, 'bienvenida.html', {'avatar_url': avatar_url, 'mensaje_bienvenida': mensaje_bienvenida})


def profesores(request):
    if request.method == 'POST':
        mi_formulario = ProfesorForm(request.POST)
        if mi_formulario.is_valid:
            profesor = Profesores(
                nombre = request.POST["nombre"], 
                apellido = request.POST["apellido"],
                email = request.POST["email"],
                profesion = request.POST["profesion"]
                )
            profesor.save()
            return render(request, 'bienvenida.html')
        else:
            mi_formulario=ProfesorForm()
            return render(request, "profesores.html")
    return render(request, "profesores.html")

def estudiantes(request):
    if request.method == 'POST':
        estudiante= Estudiantes(
            nombre = request.POST["nombre"], 
            apellido = request.POST["apellido"],
            email = request.POST["email"]
            )
        estudiante.save()
        return render(request, 'bienvenida.html')

    return render(request, "estudiantes.html")

def entregables(request):
    if request.method == 'POST':
        mi_formulario= EntregableForm(request.POST)
        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            entregable = Entregable(nombre=informacion["nombre"], fecha_entrega=informacion["fecha_entrega"], entregado=informacion["entregado"])
            entregable.save()
            return render(request, 'bienvenida.html')
    else:
        mi_formulario=EntregableForm()
        return render(request, "entregables.html",{"mi_formulario" : mi_formulario})



def cursos(request):
    if request.method == 'POST':
        mi_formulario = CursoForm(request.POST)

        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data 
            curso = Curso(nombre=informacion["nombre"], comision=informacion["comision"])
            curso.save()
            return render(request, 'bienvenida.html')

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


def leer_profesores(request):
    profesor=Profesores.objects.all()

    contexto = {"profesores": profesor}
    return render(request, "leer_profesores.html", contexto)

class CursoListView (ListView):
    model = Curso
    context_object_name = "cursos"
    template_name = "cursos_listas.html"

class CursoDetailView(DetailView):
    model = Curso
    template_name = "cursos_detail.html"


class CursoCreateView(CreateView):
    model = Curso
    template_name = "cursos_crear.html"
    success_url = reverse_lazy('ListaCurso')
    fields=['nombre','comision']

class CursoUpdateView(UpdateView):
    model = Curso
    template_name = "cursos_editar.html"
    success_url = reverse_lazy('ListaCurso')
    fields=['nombre','comision']

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = "cursos_borrar.html"
    success_url = reverse_lazy('ListaCurso')

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')

            user = authenticate(username=usuario, password=contrasenia)

            if user is not None:
                login(request, user)
                return redirect('Bienvenida')  # Cambia 'bienvenida' a 'Bienvenida'

            else:
                messages.error(request, "Credenciales incorrectas. Inténtalo de nuevo.")

    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})
    

def registro(request):
    if request.method == 'POST':
        form = UserCreationFormCustom(request.POST, request.FILES)

        if form.is_valid():
            usuario = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            imagen = request.FILES.get('imagen')

            nuevo_usuario = form.save(commit=False)
            nuevo_usuario.username = usuario
            nuevo_usuario.email = email
            nuevo_usuario.set_password(password)
            nuevo_usuario.save()

            # Inicia sesión después del registro
            login(request, nuevo_usuario)

            # Verifica si hay una imagen antes de intentar actualizarla
            if imagen:
                avatar, created = Avatar.objects.get_or_create(user=nuevo_usuario)
                avatar.imagen = imagen
                avatar.save()

            return redirect('Bienvenida')

    else:
        form = UserCreationFormCustom()

    return render(request, "registro.html", {"form": form})

def editarPerfil(request):
    usuario = request.user

    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST, request.FILES, instance=request.user)

        if miFormulario.is_valid():
            # Guarda el formulario sin actualizar la imagen del avatar
            miFormulario.save()

            # Verifica si el usuario tiene un avatar
            if hasattr(usuario, 'avatar'):
                # Ahora, verifica si hay una imagen nueva antes de intentar actualizarla
                if 'avatar' in request.FILES:
                    usuario.avatar.imagen = request.FILES.get('avatar')
                    usuario.avatar.save()
            else:
                # Si el usuario no tiene un avatar, crea uno y guarda la imagen
                avatar = Avatar.objects.create(user=usuario, imagen=request.FILES.get('avatar'))

            messages.success(request, "Perfil actualizado exitosamente.")
            return redirect('Bienvenida')

    else:
        miFormulario = UserEditForm(instance=request.user)

    return render(request, 'editar_perfil.html', {"miFormulario": miFormulario, "usuario": usuario})
    
    
class CambiarContrasenia(LoginRequiredMixin, PasswordChangeView):
    template_name= 'cambiar_contrasenia.html'
    success_url = reverse_lazy('EditarPerfil')



class EstudiantesListView (ListView):
    model = Estudiantes
    context_object_name = "estudiantes"
    template_name = "estudiantes_listas.html"

class EstudiantesDetailView(DetailView):
    model = Estudiantes
    template_name = "estudiantes_detail.html"


class EstudiantesCreateView(CreateView):
    model = Estudiantes
    template_name = "estudiantes_crear.html"
    success_url = reverse_lazy('ListaEstudiante')
    fields=['nombre','apellido', 'email']

class EstudiantesUpdateView(UpdateView):
    model = Estudiantes
    template_name = "estudiantes_editar.html"
    success_url = reverse_lazy('ListaEstudiante')
    fields=['nombre','apellido', 'email']

class EstudiantesDeleteView(DeleteView):
    model = Estudiantes
    template_name = "estudiantes_borrar.html"
    success_url = reverse_lazy('ListaEstudiante')



class ProfesorListView (ListView):
    model = Profesores
    context_object_name = "profesores"
    template_name = "profesores_listas.html"

class ProfesorDetailView(DetailView):
    model = Profesores
    template_name = "profesores_detail.html"


class ProfesorCreateView(CreateView):
    model = Profesores
    template_name = "profesores_crear.html"
    success_url = reverse_lazy('ListaProfesor')
    fields=['nombre','apellido', 'email', 'profesion']

class ProfesorUpdateView(UpdateView):
    model = Profesores
    template_name = "profesores_editar.html"
    success_url = reverse_lazy('ListaProfesor')
    fields=['nombre','apellido', 'email', 'profesion']

class ProfesorDeleteView(DeleteView):
    model = Profesores
    template_name = "profesores_borrar.html"
    success_url = reverse_lazy('ListaProfesor')



class EntregableListView (ListView):
    model = Entregable
    context_object_name = "entregable"
    template_name = "entregables_listas.html"

class EntregableDetailView(DetailView):
    model = Entregable
    template_name = "entregables_detail.html"


class EntregableCreateView(CreateView):
    model = Entregable
    template_name = "entregables_crear.html"
    success_url = reverse_lazy('ListaEntregable')
    fields=['nombre','fecha_entrega', 'entregado']

class EntregableUpdateView(UpdateView):
    model = Entregable
    template_name = "entregables_editar.html"
    success_url = reverse_lazy('ListaEntregable')
    fields = ['nombre', 'fecha_entrega', 'entregado']

class EntregableDeleteView(DeleteView):
    model = Entregable
    template_name = "entregables_borrar.html"
    success_url = reverse_lazy('ListaEntregable')




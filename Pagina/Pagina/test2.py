from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from Pagina.models import Profesores, Curso, Estudiantes, Entregable

class PaginaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profesor = Profesores.objects.create(nombre='Test', apellido='Profesor', email='test@example.com', profesion='TestProf')
        self.curso = Curso.objects.create(nombre='Test Curso', comision=101)
        self.estudiante = Estudiantes.objects.create(nombre='Test', apellido='Estudiante', email='test@example.com')
        self.entregable = Entregable.objects.create(nombre='Test Entregable', fecha_entrega='2023-12-31', entregado='S')

    def test_acceso_vistas_protegidas(self):
        response = self.client.get(reverse('Bienvenida'))
        self.assertEqual(response.status_code, 302)  # Redirección a la página de inicio de sesión

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('Bienvenida'))
        self.assertEqual(response.status_code, 200)  # Acceso permitido

    def test_creacion_profesor(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('NuevoProfesor'), {'nombre': 'Nuevo', 'apellido': 'Profesor', 'email': 'nuevo@example.com', 'profesion': 'NuevoProf'})
        self.assertEqual(response.status_code, 200)

        nuevo_profesor = Profesores.objects.get(email='nuevo@example.com')
        self.assertEqual(nuevo_profesor.nombre, 'Nuevo')
        self.assertEqual(nuevo_profesor.apellido, 'Profesor')

    def test_creacion_curso(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('NuevoCurso'), {'nombre': 'Nuevo Curso', 'comision': 102})
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

        nuevo_curso = Curso.objects.get(nombre='Nuevo Curso')
        self.assertEqual(nuevo_curso.comision, 102)

    def test_creacion_estudiante(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('NuevoEstudiante'), {'nombre': 'Nuevo', 'apellido': 'Estudiante', 'email': 'nuevo_estudiante@example.com'})
        self.assertEqual(response.status_code, 200)

        nuevo_estudiante = Estudiantes.objects.get(email='nuevo_estudiante@example.com')
        self.assertEqual(nuevo_estudiante.nombre, 'Nuevo')
        self.assertEqual(nuevo_estudiante.apellido, 'Estudiante')

    def test_creacion_entregable(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('NuevoEntregable'), {'nombre': 'Nuevo Entregable', 'fecha_entrega': '2023-12-31', 'entregado': 'S'})
        self.assertEqual(response.status_code, 200)

        nuevo_entregable = Entregable.objects.get(nombre='Nuevo Entregable')
        self.assertEqual(nuevo_entregable.fecha_entrega.strftime('%Y-%m-%d'), '2023-12-31')
        self.assertEqual(nuevo_entregable.entregado, 'S')

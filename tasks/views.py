from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from .forms import TaskForm
from .models import Task

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':  # Si el metodo es get devuelvo la pagina html.
        return render(request, 'signup.html', {
            # Funcion propia de Django que envia un form de creacion de usuario en la base de datos.
            'auth_form': UserCreationForm()
        })
    if request.method == 'POST':  # Si el metodo es post proceso los datos.
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Forma de registrar usuario con el modelo de django que ya existe.
                # Crea el usuario y cifra la pass
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()  # Guarda el usuario en la base
                # Django genera automaticamente una cookie con info del usuario. Se le pasa el request y el user a guardar
                login(request, user)
                return redirect('tasks')
            except IntegrityError as e:  # Se maneja el error especifico. Hay que importarlo.
                print(e)
                return render(request, 'signup.html', {
                    'auth_form': UserCreationForm(),
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'signup.html', {
                'auth_form': UserCreationForm(),
                'error': 'Passwords do not match'
            })

@login_required#Forma de proteger rutas para que no puedas acceder si no estan logueados
def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')#Busca las tareas que estan completadas y las ordena desde la ultima a la mas reciente
    return render(request, 'tasks.html', {
        'tasks': tasks,
        'completed': True
    })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm()
        })
    if request.method == 'POST':
        try:
            form = TaskForm(request.POST)#Forma de guardar informacion a travez del formulario que se creo
            new_task = form.save(commit=False)#Devuelve lo que se va a guardar en la base de datos pero con el commit=False no lo guarda.
            new_task.user = request.user#En toda peticion si el usuario esta autenticado siempre se envia. Esta es la forma de acceder.
            new_task.save()#Guardamos los datos en la base
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm(),
                'error': 'Please provide valid data'
            })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)#Obtiene la tarea si existe, sino devuelve 404.
        form = TaskForm(instance=task)#Llena el formulario ya creado con la tarea obtenida
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
            })
    if request.method == 'POST':
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)#Le pasamos los nuevos datos desde el post y la tarea que le corresponde actualizar
            form.save()#Guarda las modificaciones
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            'error': 'Error updating task'
            })

@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def task_delete(request, task_id):#Obtengo la tarea y la elimino con su metodo delete()
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)  # Deslogueamos con la funcion que Django nos ofrece
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            # Funcion propia de Django que envia un formulario de autenticacion.
            'form': AuthenticationForm()
        })
    if request.method == 'POST':
        # Funcion propia de Django para verificar que el usuario existe en la base. Si existe devuelve el usuario, sino 'None'.
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            # Funcion propia de Django que envia un formulario de autenticacion.
            'form': AuthenticationForm(),
            'error': 'Username or password is incorrect'
        })
        else:
            login(request, user)
            return redirect('tasks')

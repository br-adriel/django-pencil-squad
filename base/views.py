from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render

from .forms import RoomForm
from .models import Room, Topic


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)
        except:
            messages.error(request, 'O usuário não existe')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Nome de usuário ou senha inválidos')

    context = {}
    return render(request, "base/login_register.html", context)


def logout_user(request):
    logout(request)
    return redirect('home')


def home(request):
    q = ''
    if request.GET.get('q') != None:
        q = request.GET.get('q')

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {
        'room': room
    }
    return render(request, 'base/room.html', context)


def create_room(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/delete.html', context)

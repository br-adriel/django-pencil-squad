from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm

from .forms import RoomForm
from .models import Room, Topic, Message


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
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

    context = {'page': page}
    return render(request, "base/login_register.html", context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Um erro ocorreu')

    page = 'register'
    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)


@login_required(login_url='login')
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
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics,
               'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    participants = room.participants.all()

    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('comment')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    messages = room.message_set.all().order_by('-created')
    context = {
        'participants': participants,
        'room': room,
        'room_messages': messages
    }

    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Permissão de exclusão negada!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'obj': message}
    return render(request, 'base/delete.html', context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
                "user": user,
                "rooms": rooms,
                "room_messages": room_messages,
                "topics": topics
            }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Permissão de edição negada!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Permissão de exclusão negada!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/delete.html', context)

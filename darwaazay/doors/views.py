from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from . import models
from . import forms
# Create your views here.

def loginPage(request):
    pagename = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if(user):
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')


    context = {'pagename':pagename}
    return render(request, 'doors/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")

    pagename = 'register'
    form = UserCreationForm()
    context = {'pagename':pagename, 'form':form}
    return render(request, 'doors/login_register.html', context)

def home(request):
    q = request.GET.get('q')
    if(q):
        rooms = models.Room.objects.filter(
            Q(topic__name__icontains = q) |
            Q(name__icontains = q) |
            Q(host__username__icontains = q) |
            Q(description__icontains=q)
        )
    else:
        rooms = models.Room.objects.all()
    topics = models.Topic.objects.all()
    room_count = rooms.count()
    if(q):
        room_messages = models.Message.objects.filter(
            Q(room__name__icontains=q) |
            Q(room__topic__name__icontains=q) |
            Q(room__host__username__icontains=q) |
            Q(room__description__icontains=q)
        ).order_by('-created')
    else:
        room_messages = models.Message.objects.all().order_by('-created')

    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'doors/home.html', context)

def room(request, pk):
    room = models.Room.objects.get(id=int(pk))
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == "POST":
        message = models.Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'doors/room.html', context)

def userProfile(request, pk):
    user = models.User.objects.get(id=int(pk))
    rooms = user.room_set.all()
    topics = models.Topic.objects.all()
    room_messages = user.message_set.all().order_by('-created')
    context = {'user':user, 'rooms':rooms, 'topics':topics, 'room_messages':room_messages}
    return render(request, 'doors/profile.html', context)

@login_required(login_url="login")
def createRoom(request):
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = forms.RoomForm()
    context = {'form':form}
    return render(request, 'doors/room_form.html', context)

@login_required(login_url="login")
def updateRoom(request, pk):
    room = models.Room.objects.get(id=int(pk))

    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
        form = forms.RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = forms.RoomForm(instance=room)
    context = {'form':form}
    return render(request, 'doors/room_form.html', context)

@login_required(login_url="login")
def deleteRoom(request,pk):
    room = models.Room.objects.get(id=int(pk))
    if request.user != room.host:
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'doors/delete.html', context)

@login_required(login_url="login")
def deleteMessage(request,pk):
    message = models.Message.objects.get(id=int(pk))
    if request.user != message.user:
        return HttpResponse("You are not allowed to delete this message")
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request, 'doors/delete.html', context)


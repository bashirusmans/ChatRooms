from django.shortcuts import render, redirect
from django.db.models import Q
from . import models
from . import forms
# Create your views here.

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
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count}
    return render(request, 'doors/home.html', context)

def room(request, pk):
    room = models.Room.objects.get(id=int(pk))
    context = {'room':room}
    return render(request, 'doors/room.html', context)

def createRoom(request):
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = forms.RoomForm()
    context = {'form':form}
    return render(request, 'doors/room_form.html', context)

def updateRoom(request, pk):
    room = models.Room.objects.get(id=int(pk))
    if request.method == 'POST':
        form = forms.RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = forms.RoomForm(instance=room)
    context = {'form':form}
    return render(request, 'doors/room_form.html', context)

def deleteRoom(request,pk):
    room = models.Room.objects.get(id=int(pk))
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'doors/delete.html', context)
from django.shortcuts import render, redirect
from . import models
from . import forms
# Create your views here.

def home(request):
    rooms = models.Room.objects.all()
    context = {'rooms':rooms}
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
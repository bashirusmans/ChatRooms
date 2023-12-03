from django.shortcuts import render
from . import models
# Create your views here.

def home(request):
    rooms = models.Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'doors/home.html', context)

def room(request, pk):
    room = models.Room.objects.get(id=int(pk))
    context = {'room':room}
    return render(request, 'doors/room.html', context)
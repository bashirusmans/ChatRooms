from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
# Create your views here.



def loginPage(request):

    '''
      Handles user authentication for the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect or HttpResponse: Redirects to 'home' if the user is authenticated,
        else renders the login page with appropriate context.
    
    '''

    pagename = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if(user):
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')


    context = {'pagename':pagename}
    return render(request, 'doors/login_register.html', context)



def logoutUser(request):

    '''
      Logs out the currently authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to 'home' after logging out.
    
    '''

    logout(request)
    return redirect('home')




def registerUser(request):

    '''
      Handles user registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect or HttpResponse: Redirects to 'home' after successful registration,
        else renders the registration page with appropriate context.
    
    '''

    if request.method == "POST":
        form = forms.MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")

    pagename = 'register'
    form = forms.MyUserCreationForm()
    context = {'pagename':pagename, 'form':form}
    return render(request, 'doors/login_register.html', context)




@login_required(login_url="login")
def updateUser(request):

    '''
        Handles user profile updates.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect or HttpResponse: Redirects to the user profile page after successful update,
        else renders the user update page with appropriate context.
    
    '''

    user = request.user
    if request.method == "POST":
        if user.username == request.POST.get('username'):
            pass
        else:
            try:
                named_user = models.User.objects.get(username=request.POST.get('username'))
                message = 'Username ' + named_user.username + ' is already taken'
                messages.error(request, message)
                return redirect('update-user')
            except:
                pass
        form = forms.UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
        else:
            messages.error(request, 'An error occured during updation')
    form = forms.UserForm(instance=user)
    context = {'form':form}
    return render(request, 'doors/edit-user.html', context)




def home(request):

    '''
     Displays the home page with a list of rooms and topics.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the home page with appropriate context.
    
    '''

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
    topics = models.Topic.objects.all()[0:5]

    room_count = rooms.count()
    total_room_count = models.Room.objects.all().count()
    if(q):
        room_messages = models.Message.objects.filter(
            Q(room__name__icontains=q) |
            Q(room__topic__name__icontains=q) |
            Q(room__host__username__icontains=q) |
            Q(room__description__icontains=q)
        ).order_by('-created')
    else:
        room_messages = models.Message.objects.all().order_by('-created')

    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages, 'total_room_count':total_room_count}
    return render(request, 'doors/home.html', context)

def room(request, pk):

    '''
    Displays a specific room with its messages and participants.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the room to be displayed.

    Returns:
        HttpResponse: Renders the room page with appropriate context.
    
    '''

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

    '''
    Displays the profile page for a specific user.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the user whose profile is to be displayed.

    Returns:
        HttpResponse: Renders the user profile page with appropriate context.

    '''

    user = models.User.objects.get(id=int(pk))
    rooms = user.room_set.all()
    total_room_count = models.Room.objects.all().count()
    topics = models.Topic.objects.all()
    room_messages = user.message_set.all().order_by('-created')
    context = {'user':user, 'rooms':rooms, 'topics':topics, 'room_messages':room_messages, 'total_room_count':total_room_count}
    return render(request, 'doors/profile.html', context)





@login_required(login_url="login")
def createRoom(request):

    '''
    Handles the creation of a new room.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect or HttpResponse: Redirects to 'home' after successful room creation,
        else renders the room creation page with appropriate context.
    
    '''

    form = forms.RoomForm()
    topics = models.Topic.objects.all()
    if request.method == 'POST':
        # form = forms.RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = models.Topic.objects.get_or_create(name = topic_name)
        models.Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        
        return redirect('home')

    context = {'form':form, 'topics':topics, 'create':True}
    return render(request, 'doors/room_form.html', context)





@login_required(login_url="login")
def updateRoom(request, pk):

    '''
     Handles the update of an existing room.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the room to be updated.

    Returns:
        HttpResponseRedirect or HttpResponse: Redirects to 'home' after successful room update,
        else renders the room update page with appropriate context.

    Raises:
        NotPermitted: If the user does not have authority to change the room.
    
    '''


    room = models.Room.objects.get(id=int(pk))

    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = models.Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
    form = forms.RoomForm(instance=room)
    context = {'form':form, 'room': room}
    return render(request, 'doors/room_form.html', context)





@login_required(login_url="login")
def deleteRoom(request,pk):

    '''
     Handles the deletion of an existing room.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the room to be deleted.

    Returns:
        HttpResponseRedirect or HttpResponse: Redirects to 'home' after successful room deletion,
        else renders the room deletion confirmation page with appropriate context.

    Raises:
        NotPermitted: If the user does not have authority to delete the room.
    
    '''

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

    '''    
    Handles the deletion of an existing message.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the message to be deleted.

    Returns:
        HttpResponseRedirect or HttpResponse: Redirects to 'home' after successful message deletion,
        else renders the message deletion confirmation page with appropriate context.

    Raises:
        NotPermitted: If the user does not have authority to delete the message.
    
    '''

    message = models.Message.objects.get(id=int(pk))
    if request.user != message.user:
        return HttpResponse("You are not allowed to delete this message")
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request, 'doors/delete.html', context)

def topicsPage(request):

    '''
    Displays a page with a list of topics.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the topics page with appropriate context.

    '''

    q = request.GET.get('q')
    if (q):
        topics = models.Topic.objects.filter(
            Q(name__icontains=q)
        )
    else:
        topics = models.Topic.objects.all()
    total_room_count = models.Room.objects.all().count()
    context = {'topics':topics, 'total_room_count':total_room_count}
    return render(request, 'doors/topics.html', context)




def activityPage(request):

    '''
     Displays a page with a list of all room messages.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the activity page with appropriate context.

    '''
    
    room_messages = models.Message.objects.all()
    context = {'room_messages':room_messages}
    return render(request, 'doors/activity.html', context)


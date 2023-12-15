from django.forms import ModelForm
from . import models

class RoomForm(ModelForm):
    class Meta:
        model = models.Room
        fields = "__all__"
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'email']

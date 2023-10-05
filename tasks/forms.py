from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task, Photo 

class reg_add(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class PasswordResetRequestForm(forms.Form):
    username_or_email = forms.CharField(max_length=255, label="Username or Email")

class TaskForm(forms.ModelForm):
    created_at = forms.DateTimeField(disabled=False)  # Custom field
    last_updated_at = forms.DateTimeField(disabled=False)

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'completed']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

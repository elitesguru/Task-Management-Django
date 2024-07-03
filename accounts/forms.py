from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Task, ChatMessage

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='', label='Email address')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class LoginForm(AuthenticationForm):
    pass

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'invite_colleagues']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Task Description', 'rows': 3}),
            'priority': forms.Select(attrs={'placeholder': 'Priority'}),
            'invite_colleagues': forms.TextInput(attrs={'placeholder': 'Invite Colleagues (comma separated usernames)'}),
        }

class ChatMessageForm(forms.ModelForm):
    recipients = forms.CharField(help_text='Enter usernames separated by commas')

    class Meta:
        model = ChatMessage
        fields = ['content']

def create_task_view():
    return None
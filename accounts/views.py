from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg,Q
from django.contrib.auth.models import User
from .models import Task, ChatMessage
from .forms import SignUpForm, LoginForm, CreateTaskForm, ChatMessageForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def home_view(request):
    tasks = Task.objects.filter(user=request.user)
    chat_messages = ChatMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).order_by('timestamp')
    create_task_form = CreateTaskForm()
    chat_message_form = ChatMessageForm()

    if request.method == 'POST':
        if 'title' in request.POST:
            create_task_form = CreateTaskForm(request.POST)
            if create_task_form.is_valid():
                task = create_task_form.save(commit=False)
                task.user = request.user
                task.save()
                return redirect('home')
        elif 'content' in request.POST:
            chat_message_form = ChatMessageForm(request.POST)
            if chat_message_form.is_valid():
                message = chat_message_form.save(commit=False)
                message.sender = request.user
                message.save()
                recipients = request.POST.getlist('recipients')
                for username in recipients:
                    recipient = User.objects.filter(username=username.strip()).first()
                    if recipient:
                        message.recipient.add(recipient)
                message.save()
                messages.success(request, 'Message sent successfully.')
                return redirect('home')

    context = {
        'user': request.user,
        'tasks': tasks,
        'chat_messages': chat_messages,  # Make sure chat_messages is included in context
        'create_task_form': create_task_form,
        'chat_message_form': chat_message_form,
    }
    return render(request, 'accounts/home.html', context)

@login_required
def task_list_view(request):
    tasks = Task.objects.all().order_by('-created_at')
    context = {
        'tasks': tasks
    }
    return render(request, 'accounts/task_list.html', context)

@login_required
def task_analysis_view(request):
    total_tasks = Task.objects.count()
    high_priority_tasks = Task.objects.filter(priority='high').count()
    medium_priority_tasks = Task.objects.filter(priority='medium').count()
    low_priority_tasks = Task.objects.filter(priority='low').count()
    average_progress = Task.objects.aggregate(Avg('progress'))['progress__avg']
    context = {
        'total_tasks': total_tasks,
        'high_priority_tasks': high_priority_tasks,
        'medium_priority_tasks': medium_priority_tasks,
        'low_priority_tasks': low_priority_tasks,
        'average_progress': average_progress,
    }
    return render(request, 'accounts/task_analysis.html', context)

@login_required
def chat_view(request):
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.sender = request.user
            chat_message.save()
            for recipient in form.cleaned_data['recipients']:
                chat_message.recipient.add(recipient)
            chat_message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('chat')
    else:
        form = ChatMessageForm()

    chat_messages = ChatMessage.objects.all().order_by('-timestamp')
    context = {
        'chat_messages': chat_messages,
        'form': form,
    }
    return render(request, 'accounts/chat.html', context)
def create_task_view(request):

    return HttpResponse("Create Task Page")
@login_required
def send_message(request):
    if request.method == 'POST':

        pass  # Replace with your message sending code
    return redirect('chat_view')
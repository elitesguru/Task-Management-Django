from django.urls import path
from . import views
from .views import signup_view, login_view, home_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('send_message/', views.send_message, name='send_message'),
    path('home/', home_view, name='home'),
    path('task_list/', views.task_list_view, name='task_list'),
    path('task_analysis/', views.task_analysis_view, name='task_analysis'),
    path('chat/', views.chat_view, name='chat'),
    path('create_task/', views.create_task_view, name='create_task'),
]

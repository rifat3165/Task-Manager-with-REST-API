"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from tasks.views import AddPhotoToTaskView, TaskDeleteView, TaskListView, TaskUpdateView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', views.login_form),
    path('register/', views.reg_form),
    path('success/', views.login_success),
    path('logout/', views.logout_form),
    path('cpass/', views.change_pass),
    path('reset/', views.password_reset_request),
    path('tasklist/', views.TaskListView.as_view(), name='task_list'),
    path('tasklist/<int:pk>', views.TaskDetailView.as_view(), name='task_detail'),
    path('taskcreate/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/add_photo/', AddPhotoToTaskView.as_view(), name='add_photo_to_task'),
    path('<int:pk>/delete/', views.DeletePhotoView.as_view(), name='delete_photo'),


    path('api/tasks/', views.TaskApi_list_create.as_view(), name='task-list'),
    path('api/tasks/<int:pk>/', views.TaskApi_retrieve_update_destroy.as_view(), name='task-detail'),

    

    
]

"""BackendIpcaProy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path

from core import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/v1/create-tarea', views.create_tarea),
    path('api/v1/tareas/<int:id>', views.tarea_by_id),
    path('api/v1/get-info-usuario', views.get_informacion_usuario),
    path('api/v1/get-tareas', views.get_tareas),
    path('api/v1/notificar-tarea', views.notificar_tarea),
    path('api/v1/get-user-id', views.get_user_id),
]

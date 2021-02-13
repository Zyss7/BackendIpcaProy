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

base_url = 'api/v1/'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(f'{base_url}create-tarea', views.create_tarea),
    path(f'{base_url}tareas/<int:id>', views.tarea_by_id),
    path(f'{base_url}get-info-usuario', views.get_informacion_usuario),
    path(f'{base_url}get-tareas', views.get_tareas),
    path(f'{base_url}notificar-tarea', views.notificar_tarea),
    path(f'{base_url}get-user-id', views.get_user_id),
    path(f'{base_url}delete-tarea/<int:id>', views.delete_tarea),

    # lista de reproduccion
    path(f'{base_url}crear-lista-reproduccion', views.crear_lista_reproduccion),
    path(f'{base_url}editar-lista-reproduccion-by-id/<int:id>', views.editar_lista_reproduccion_by_id),
    path(f'{base_url}eliminar-lista-reproduccion-by-id/<int:id>', views.eliminar_lista_reproduccion_by_id),
    path(f'{base_url}get-lista-reproduccion-by-id/<int:id>', views.get_lista_reproduccion_by_id),
    path(f'{base_url}get-listas-reproduccion', views.get_listas_reproduccion),
]

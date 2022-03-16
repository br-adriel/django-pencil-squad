from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('salas/criar', views.create_room, name='create-room'),
    path('salas/editar/<str:pk>', views.update_room, name='update-room'),
    path('salas/apagar/<str:pk>', views.delete_room, name='delete-room'),
    path('salas/<str:pk>', views.room, name='room'),
]

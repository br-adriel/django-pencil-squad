from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('squads/criar', views.create_room, name='create-room'),
    path('squads/editar/<str:pk>', views.update_room, name='update-room'),
    path('squads/apagar/<str:pk>', views.delete_room, name='delete-room'),
    path('squads/<str:pk>', views.room, name='room'),
]

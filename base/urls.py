from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('login', views.login_page, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register_user, name="register"),

    path('profile/<str:pk>', views.user_profile, name="user-profile"),

    path('squads/criar', views.create_room, name='create-room'),
    path('squads/editar/<str:pk>', views.update_room, name='update-room'),
    path('squads/apagar/<str:pk>', views.delete_room, name='delete-room'),
    path('squads/<str:pk>', views.room, name='room'),
    path('squads/comentario/apagar/<str:pk>',
         views.delete_message, name='delete-message')
]

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('topics', views.topics_page, name='topics-page'),
    path('activity', views.activity_page, name='activity-page'),

    path('login', views.login_page, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register_user, name="register"),

    path('profile/edit', views.update_user, name='update-user'),
    path('profile/<str:pk>', views.user_profile, name="user-profile"),

    path('squads/criar', views.create_room, name='create-room'),
    path('squads/editar/<str:pk>', views.update_room, name='update-room'),
    path('squads/apagar/<str:pk>', views.delete_room, name='delete-room'),
    path('squads/<str:pk>', views.room, name='room'),
    path('squads/comentario/apagar/<str:pk>',
         views.delete_message, name='delete-message')
]

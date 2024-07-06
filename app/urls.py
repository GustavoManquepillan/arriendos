from django.urls import path
from .views import index, register, profile, register_profile, update_profile, register_inmueble, get_inmuebles, update_inmueble, messages
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    path('', index, name='home'),
    path('login/', LoginView.as_view(next_page='home'), name='login_url'),
    path('logout/', LogoutView.as_view(next_page='login_url'), name='logout'),
    path('register/', register ,name='register'),
    path('profile/', profile, name='profile'),
    path('register_profile/', register_profile, name='register_profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('inmuebles/', get_inmuebles, name='get_inmuebles'),
    path('register_inmueble/', register_inmueble, name='register_inmueble'),
    path('update_inmueble/<int:pk>/', update_inmueble, name='update_inmueble'),
    path('inmuebles/delete/<int:pk>/', views.delete_inmueble, name='delete_inmueble'),
    path('contact/<int:id>/', views.contact, name='contact'),
    path('contact_success/', views.contact_success, name='contact_success'),
    path('messages/', messages, name='mensaje'),

]
 
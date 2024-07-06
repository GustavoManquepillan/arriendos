from django import forms
from django.contrib.auth.models import User
from .models import Perfil, Inmueble,Contact
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    # Agrega cualquier personalización que necesites aquí
    pass
class UserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username':'Nombre de Usuario',
            'first_name':'Nombre', 
            'last_name': 'Apellido',
            'email':'Correo electronico', 
            'password1':'Contraseña', 
            'password2':'Repita la contraseña'
        }
    
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('tipo_usuario','rut','direccion','telefono')


class InmuebleForm(forms.ModelForm):
    #id_usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    class Meta:

        model = Inmueble
        fields = (
            'id_tipo_inmueble','id_comuna','id_region', 
            'nombre_inmueble', 'm2_construido', 'numero_banos', 
            'numero_hab','direccion', 'descripcion','imagen_url'
            )   #registra todos los campos disponibles

        labels = {
            'id_tipo_inmueble':'Tipo de Inmueble',
            'id_comuna':'Comuna',
            'id_region':'Region', 
            'nombre_inmueble':'Nombre Inmueble',
            'm2_construido':'Metros cuadrados construidos', 
            'numero_banos':'Numero de Baños', 
            'numero_hab':'Numero de habitaciones',
            'direccion':'Direccion',
            'descripcion':'Descripcion',
            'imagen_url': 'Imagen del Inmueble',
            }   #registra todos los campos disponibles

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('correo','nombre','mensaje')
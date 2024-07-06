from django.contrib import admin
from .models import Tipo_usuario, Tipo_inmueble, Perfil, Usuario, Inmueble, Comuna, Region, Contact

admin.site.register(Tipo_usuario)
admin.site.register(Tipo_inmueble)
admin.site.register(Perfil)
admin.site.register(Usuario)
admin.site.register(Inmueble)
admin.site.register(Comuna)
admin.site.register(Region)
admin.site.register(Contact)

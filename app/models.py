from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

def validate_min_value(value):
# Validación personalizada
    if value <= 0:
        raise ValidationError('Los metros cuadrados construidos deben ser positivos.')

class Usuario(models.Model):
    """ este usuario se usa para registrarse, loggearse, etc auth.User"""
    id_usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        # Lógica personalizada antes de guardar
        super(Usuario, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'Usuario: {self.id_usuario.username}'


class Inmueble(models.Model):
    id_usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE) 
    id_tipo_inmueble = models.ForeignKey('Tipo_inmueble', on_delete=models.CASCADE)
    id_comuna = models.ForeignKey('Comuna', on_delete=models.CASCADE)
    id_region = models.ForeignKey('Region', on_delete=models.CASCADE)
    nombre_inmueble = models.CharField(max_length=200)
    m2_construido = models.FloatField(validators=[validate_min_value], default=0)
    numero_banos = models.PositiveIntegerField(default=0)
    numero_hab = models.PositiveIntegerField(default=0)
    direccion = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen_url = models.URLField(blank=True, null=True)
    

    def save(self, *args, **kwargs):
        # Lógica personalizada antes de guardar
        self.nombre_inmueble = self.nombre_inmueble.title()  # Capitalizar el nombre del inmueble
        
        # Llamar al método save() original
        super(Inmueble, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre_inmueble} ({self.id_tipo_inmueble})'


class Region(models.Model):
    region = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Lógica personalizada antes de guardar
        self.region = self.region.title()  # Capitalizar el nombre de la región
        
        # Llamar al método save() original
        super(Region, self).save(*args, **kwargs)

    def __str__(self):
        return self.region


class Comuna(models.Model):
    comuna = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Lógica personalizada antes de guardar
        self.comuna = self.comuna.title()  # Capitalizar el nombre de la comuna
        
        # Llamar al método save() original
        super(Comuna, self).save(*args, **kwargs)

    def __str__(self):
        return self.comuna


class Tipo_inmueble(models.Model):
    CHOICES = [
        ('Departamento', 'Departamento'),
        ('Casa', 'Casa'),
        ('Parcela', 'Parcela'),
    ]
    tipo = models.CharField(max_length=12, choices=CHOICES)
    
    def __str__(self):
        return self.tipo


class Tipo_usuario(models.Model):
    CHOICES = (
        ('Arrendador', 'Arrendador'),
        ('Arrendatario', 'Arrendatario'),
    )
    tipo = models.CharField(max_length=12, choices=CHOICES)
    
    def save(self, *args, **kwargs):
        # Lógica personalizada antes de guardar
        self.tipo = self.tipo.title()  # Capitalizar el tipo de usuario
        
        # Llamar al método save() original
        super(Tipo_usuario, self).save(*args, **kwargs)

    def __str__(self):
        return self.tipo


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.ForeignKey('Tipo_usuario', on_delete=models.CASCADE)
    rut = models.CharField(max_length=12)
    direccion = models.CharField(max_length=255)
    cuidad =models.CharField(max_length=50)
    telefono = models.CharField(max_length=12)
    correo = models.EmailField(max_length=50)
    

    def save(self, *args, **kwargs):
        # Lógica personalizada antes de guardar
        self.direccion = self.direccion.title()  # Capitalizar la dirección
        
        # Llamar al método save() original
        super(Perfil, self).save(*args, **kwargs)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'
    
class Contact(models.Model):
    arrendador = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    nombre_inmueble = models.CharField(max_length=200)  
    correo = models.EmailField()
    nombre = models.CharField(max_length=64)
    mensaje = models.TextField()
    
    def save(self, *args, **kwargs):
        # Lógica personalizada antes de guardar
        
        self.mensaje = self.mensaje.title()
        
        super(Contact, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.correo} - Mensaje: {self.mensaje}"
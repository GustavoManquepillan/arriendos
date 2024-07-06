from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Inmueble, Perfil, Comuna, Region, Contact
from .forms import UserForm, CustomAuthenticationForm, PerfilForm, InmuebleForm, ContactForm

def index(request):
    regiones = Region.objects.all()
    comunas = Comuna.objects.all()
    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')
    inmuebles = Inmueble.objects.all()

    if region_id:
        inmuebles = inmuebles.filter(id_region=region_id)
    if comuna_id:
        inmuebles = inmuebles.filter(id_comuna=comuna_id)
    context = {
        'inmuebles': inmuebles,
        'regiones': regiones,
        'comunas': comunas
    }
    return render(request, 'index.html', context)


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                perfil = Perfil.objects.get(usuario=user)
                if perfil.tipo_usuario.tipo == 'Arrendador':
                    return redirect('get_inmuebles')
                else:
                    return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    perfil = Perfil.objects.get(usuario=request.user)
    return render(request, 'profile.html', {'perfil': perfil})

def register_profile(request):
    usuario = request.user 
    if request.method == "POST":
        form = PerfilForm(request.POST)
        if form.is_valid():
            usuario = usuario
            tipo = form.cleaned_data['tipo_usuario']
            rut = form.cleaned_data['rut']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            correo = usuario.email
            
            datos = Perfil(
                usuario=usuario,
                tipo_usuario=tipo,
                rut=rut,
                direccion=direccion,
                telefono=telefono,
                correo=correo,
                )
            datos.save()
            return HttpResponseRedirect('/profile/')
            
    else:
    #si es que tenemos el metodo get
        form = PerfilForm()
        context = {
            'form':form,
            'title':'Crear perfil'
        }
    return render(request, 'register_profile.html', context)
    

def update_profile(request):
    usuario = request.user
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            perfil = Perfil.objects.filter(usuario=usuario).update(**form.cleaned_data)
            return redirect('profile')
    else: 
        perfil = Perfil.objects.filter(usuario=usuario)
        if perfil.exists():
            perfil = perfil.first()
            form = PerfilForm(instance=perfil)
            context = {
                'form':form,
                'title':'Actualizar Perfil'
            }

        return render(request, 'update_profile.html', context)
    
    
def register(request):
    if request.user.is_authenticated:
        return redirect('profile')  
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            ultimo_usuario_creado = authenticate(request, username=username, password=password)
            login(request, ultimo_usuario_creado)
            return redirect('profile')  
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)    


@login_required(login_url='/login/')
def register_inmueble(request):
    usuario = request.user
    tipo = Perfil.objects.get(usuario=usuario).tipo_usuario.tipo
    if request.method == "POST":
        form = InmuebleForm(request.POST)
        if form.is_valid():
            tipo_inmueble = form.cleaned_data['id_tipo_inmueble']
            comuna = form.cleaned_data['id_comuna']
            region = form.cleaned_data['id_region']
            nombre_inmueble = form.cleaned_data['nombre_inmueble']
            m2_construido = form.cleaned_data['m2_construido']
            numero_banos = form.cleaned_data['numero_banos']
            numero_hab = form.cleaned_data['numero_hab']
            direccion = form.cleaned_data['direccion']
            descripcion = form.cleaned_data['descripcion']
            imagen_url = form.cleaned_data['imagen_url']
           
            datos = Inmueble(
                id_usuario=usuario,
                id_tipo_inmueble=tipo_inmueble,
                id_comuna=comuna,
                id_region=region,
                nombre_inmueble=nombre_inmueble,
                m2_construido=m2_construido, 
                numero_banos=numero_banos,
                numero_hab=numero_hab,
                direccion=direccion,
                descripcion=descripcion,
                imagen_url=imagen_url
            )
            datos.save()
            return HttpResponseRedirect('/inmuebles/')
    else:
        form = InmuebleForm()
        context = {
            'form': form,
            'tipo': tipo,
            'title': 'Registrar Inmueble'
        }
        return render(request, 'register_inmueble.html', context)

    

@login_required
def get_inmuebles(request):
    user = request.user
    try:
        perfil = Perfil.objects.get(usuario=user)
        print("Perfil encontrado:", perfil)  # Depuración
        tipo_usuario = perfil.tipo_usuario.tipo
        print("Tipo de usuario:", tipo_usuario)  # Depuración
        if tipo_usuario == 'Arrendador':
            # Si el usuario es un arrendador, filtrar los inmuebles por el usuario actual
            inmuebles = Inmueble.objects.filter(id_usuario=user)
            print("Inmuebles del arrendador:", inmuebles)  # Depuración
        else:
            # Si el usuario no es un arrendador, mostrar todos los inmuebles
            inmuebles = Inmueble.objects.all()
            print("Todos los inmuebles:", inmuebles)  # Depuración
    except Perfil.DoesNotExist:
        print("El perfil no existe para el usuario:", user)  # Depuración
        # Si no se encuentra el perfil, mostrar todos los inmuebles por defecto
        inmuebles = Inmueble.objects.all()
    
    context = {
        'inmuebles': inmuebles,
        'perfil': perfil if 'perfil' in locals() else None,  # Manejar el caso en que el perfil no está definido
    }
    return render(request, 'welcome.html', context)





@login_required(login_url='/login/')
def update_inmueble(request, pk):
    usuario = request.user
    tipo = Perfil.objects.get(usuario=usuario).tipo_usuario.tipo
    inmueble = Inmueble.objects.get(pk=pk)

    if request.method =="POST":
        form = InmuebleForm(request.POST)
        if form.is_valid():
            inmueble = Inmueble.objects.filter(pk=pk).update(**form.cleaned_data)
            #el metodo update funciona solo con querysets por lo que no funcionara con el metodo get del object
            
            return HttpResponseRedirect('/inmuebles/')
        
    ###CON EL GET
    elif inmueble.id_usuario.id == usuario.id:
    #nos traemos el objeto Inmueble con pk = pk
        form = InmuebleForm(instance=inmueble)
        context = {
                    'form':form,
                    'title':'Editar Inmueble',
                    'tipo':tipo
                    }
    else:
        form = 'Inmueble no encontrado'
        context = {
                    'form':form,
                    'title':'Usted no tiene acceso a esta propiedad',
                    'tipo':tipo
                    }
    return render(request,'update_inmueble.html', context)



@login_required(login_url='/login/')
def delete_inmueble(request, pk):
    # Intentar recuperar el objeto Inmueble con la clave primaria `pk`
    inmueble = get_object_or_404(Inmueble, pk=pk)

    # Verificar si el usuario actual es el propietario del inmueble
    if inmueble.id_usuario == request.user:
        if request.method == 'POST':
            # Si el formulario se envía (solicitud POST), eliminar el inmueble
            inmueble.delete()
            return redirect('get_inmuebles')  # Redirigir a la lista de inmuebles después de la eliminación

        # Renderizar la página de confirmación si el método de solicitud es GET
        context = {
            'inmueble': inmueble,
            'title': 'Eliminar Inmueble'
        }
        return render(request, 'confirm_delete_inmueble.html', context)
    else:
        # Devolver una respuesta 403 Prohibido si el usuario no es el propietario
        return HttpResponseRedirect("No tienes permiso para eliminar este inmueble")


def contact(request, id):
    usuario = request.user
    tipo = Perfil.objects.get(usuario=usuario).tipo_usuario.tipo
    inmueble = Inmueble.objects.get(pk=id)
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            nombre = form.cleaned_data['nombre']
            mensaje = form.cleaned_data['mensaje']
            nombre_inmueble = inmueble.nombre_inmueble
            arrendador = inmueble.id_usuario

            data = Contact(
                nombre_inmueble=nombre_inmueble,
                correo=correo,
                arrendador=arrendador,
                nombre=nombre,
                mensaje=mensaje,
            )
            data.save()
            return redirect('contact_success')  # Asegúrate de que esta ruta está definida en urls.py

    form = ContactForm()
    context = {
                'form':form,
                'title':'Contacta al Propietario',
                'tipo':tipo
            }
    return render(request,'contact.html', context)
    

def messages(request):
    usuario = request.user
    messages = Contact.objects.filter(arrendador=usuario)
    tipo = Perfil.objects.get(usuario=usuario).tipo_usuario.tipo

    context = {
                    'messages':messages,
                    'tipo':tipo
                }
    return render(request, 'mensajes.html', context)


def contact_success(request):
    return render(request, 'contact_success.html')
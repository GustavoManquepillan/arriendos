import os
from .models import Inmueble, Tipo_inmueble, User

def guardar_inmuebles_en_txt(query, nombre_archivo):
    # Obtener la ruta absoluta del directorio "archivos" dentro de la aplicación
    directorio_archivos = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivos')

    # Comprobar si el directorio "archivos" existe, si no, crearlo
    if not os.path.exists(directorio_archivos):
        os.makedirs(directorio_archivos)

    # Crear la ruta absoluta del archivo de texto
    ruta_archivo = os.path.join(directorio_archivos, nombre_archivo)

    # Abrir el archivo de texto en modo escritura
    with open(ruta_archivo, 'w') as archivo:
        # Escribir cada inmueble en el archivo de texto
        for inmueble in query:
            archivo.write(f"Nombre: {inmueble.nombre_inmueble}\n")
            archivo.write(f"Descripción:\n")
            archivo.write(f"    M2 Construidos: {inmueble.m2_construido}\n")
            archivo.write(f"    Número de Baños: {inmueble.numero_banos}\n")
            archivo.write(f"    Número de Habitaciones: {inmueble.numero_hab}\n")
            archivo.write(f"    Dirección: {inmueble.direccion}\n\n")

def get_all_inmuebles():
    # Utilizamos el ORM de Django para obtener todos los inmuebles
    inmuebles = Inmueble.objects.all()
    return inmuebles

def insertar_inmueble(nombre_inmueble, m2_construido, numero_banos, numero_hab, direccion):
    # Creamos un nuevo objeto Inmueble con los datos proporcionados
    nuevo_inmueble = Inmueble(nombre_inmueble=nombre_inmueble, 
                              m2_construido=m2_construido,
                              numero_banos=numero_banos,
                              numero_hab=numero_hab,
                              direccion=direccion)
    # Guardamos el nuevo inmueble en la base de datos
    nuevo_inmueble.save()

def actualizar_inmueble(id_inmueble, nombre_inmueble, m2_construido, numero_banos, numero_hab, direccion):
    # Obtenemos el inmueble que queremos actualizar
    inmueble = Inmueble.objects.get(id=id_inmueble)
    # Actualizamos sus atributos
    inmueble.nombre_inmueble = nombre_inmueble
    inmueble.m2_construido = m2_construido
    inmueble.numero_banos = numero_banos
    inmueble.numero_hab = numero_hab
    inmueble.direccion = direccion
    # Guardamos los cambios en la base de datos
    inmueble.save()

def borrar_inmueble(id_inmueble):
    # Obtenemos el inmueble que queremos borrar
    inmueble = Inmueble.objects.get(id=id_inmueble)
    # Borramos el inmueble de la base de datos
    inmueble.delete()

def get_list_inmuebles(comuna=None):
    select = f"""
    SELECT A.id, C.comuna, B.region, nombre_inmueble, m2_construido, numero_banos, numero_hab, direccion
    FROM app_inmueble AS A
    INNER JOIN app_region AS B ON A.id_region_id = B.id
    INNER JOIN app_comuna AS C ON A.id_comuna_id = C.id
    WHERE C.comuna LIKE '{comuna}'
    """

    query = Inmueble.objects.raw(select)

    # Guardar los inmuebles en un archivo de texto
    guardar_inmuebles_en_txt(query, f"inmuebles_{comuna}.txt")

def get_inmuebles(region=''):
    select = f"""
    SELECT A.id, C.comuna, B.region, nombre_inmueble, m2_construido, numero_banos, numero_hab, direccion
    FROM app_inmueble AS A
    INNER JOIN app_region AS B ON A.id_region_id = B.id
    INNER JOIN app_comuna AS C ON A.id_comuna_id = C.id
    WHERE B.region LIKE '%{region}%'
    """

    query = Inmueble.objects.raw(select)

    # Guardar los inmuebles en un archivo de texto
    guardar_inmuebles_en_txt(query, f"inmuebles_{region}.txt")

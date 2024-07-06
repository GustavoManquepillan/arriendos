from ...models import Inmueble

query = "SELECT * FROM app_inmueble"

inmuebles = Inmueble.objects.raw(query)

for c in todas:
    archi.write(c.comuna)
    archi.write('\n')
archi.close()
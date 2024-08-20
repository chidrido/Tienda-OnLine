from configuracion.wsgi import *
from aplicaciones.administrador.models import Categoria

data = ['Leche y derivados', 'Carnes, pescados y huevos', 'Patatas, legumbres, frutos secos',
        'Verduras y Hortalizas', 'Frutas', 'Cereales y derivados, azúcar y dulces',
        'Grasas, aceite y mantequilla']

for i in data:
    cat = Categoria(nombre=i)
    cat.save()
    print('Guardado registro N°{}'.format(cat.id))

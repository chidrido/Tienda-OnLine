from configuracion.wsgi import *
import csv
from aplicaciones.administrador.models import Producto

with open('C:/Users/chidr/OneDrive/Desktop/Archivo_csv.csv')as reader:
    data = {}
    reader = csv.DictReader(reader, delimiter=';')
    for row in reader:
        codigo = row['Cod.Barras']
        pvp = row['PVP']
        Producto.objects.filter(codigo=codigo).update(pvp=pvp)
    


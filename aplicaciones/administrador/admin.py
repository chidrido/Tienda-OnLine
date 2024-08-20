from django.contrib import admin
from aplicaciones.administrador.models import Producto, Cesta, Importar

admin.site.register(Producto)
admin.site.register(Cesta)
admin.site.register(Importar)

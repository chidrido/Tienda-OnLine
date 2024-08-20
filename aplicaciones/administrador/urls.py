from django.urls import path

from .views.cesta.views import CestaListView, CestaDeleteView, CestaFacturaPdfView
from .views.categoria.views import *
from .views.clientes.views import ClienteCreateView, ClienteUpdateView, ClienteDeleteView, ClienteListView, \
    ClienteSuperCreateView, ClienteSuperUpdateView
from .views.favoritos.views import FavoritosListView, FavoritosDeleteView, FavoritosCestaCreateView
from .views.gestiona_favoritos.views import GestionaFavoritosListView
from .views.importar_csv.views import ImportarCSVListView, ImportarCSVUpdateView, ImportarCSVDeleteView
from .views.muestra_oferta.views import MuestraOfertasListView
from .views.gestiona.views import GestionaProductosListView, GestionaProductosUpdateView, GestionaProductosDeleteView, \
    GestionaProductosCreateView
from .views.ofertas.views import OfertaUpdateView, OfertaCreateView, OfertaListView, OfertaDeleteView
from .views.productos.views import ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView
from .views.subcategoria.views import SubCategoriaFormView, SubCategoriaDeleteView, SubCategoriaUpdateView, \
    SubCategoriaCreateView, SubCategoriaListView
from .views.super.views import SuperListView  # , PruebaListView,
from .views.test.views import TestView
from aplicaciones.administrador.views.panelcontrol.views import *
from aplicaciones.administrador.views.ventas.views import VentaListView, VentaCreateView, VentaDeleteView, \
    VentaUpdateView, VentaFacturaPdfView

app_name = 'administrador'

urlpatterns = [
    # categoria
    path('categoria/lista/', CategoriaListView.as_view(), name='categoria_lista'),
    path('categoria/crear/', CategoriaCreateView.as_view(), name='categoria_crear'),
    path('categoria/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('categoria/eliminar/<int:pk>/', CategoriaDeleteView.as_view(), name='categoria_eliminar'),
    path('categoria/form/', CategoriaFormView.as_view(), name='categoria_form'),
    # subcategoria
    path('subcategoria/lista/', SubCategoriaListView.as_view(), name='subcategoria_lista'),
    path('subcategoria/crear/', SubCategoriaCreateView.as_view(), name='subcategoria_crear'),
    path('subcategoria/editar/<int:pk>/', SubCategoriaUpdateView.as_view(), name='subcategoria_editar'),
    path('subcategoria/eliminar/<int:pk>/', SubCategoriaDeleteView.as_view(), name='subcategoria_eliminar'),
    path('subcategoria/form/', SubCategoriaFormView.as_view(), name='subcategoria_form'),
    # clientes
    path('cliente/lista/', ClienteListView.as_view(), name='cliente_lista'),
    path('cliente/crear/', ClienteCreateView.as_view(), name='cliente_crear'),
    path('cliente/editar/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('cliente/eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_eliminar'),
    path('cliente/crearperfil/', ClienteSuperCreateView.as_view(), name='cliente_crearSuper'),
    path('cliente/editarperfil/<int:pk>/', ClienteSuperUpdateView.as_view(), name='cliente_editarSuper'),
    # productos
    path('producto/lista/', ProductoListView.as_view(), name='producto_lista'),
    path('producto/crear/', ProductoCreateView.as_view(), name='producto_crear'),
    path('producto/editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_editar'),
    path('producto/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_eliminar'),
    # oferta
    path('oferta/lista/', OfertaListView.as_view(), name='oferta_lista'),
    path('oferta/crear/', OfertaCreateView.as_view(), name='oferta_crear'),
    path('oferta/editar/<int:pk>/', OfertaUpdateView.as_view(), name='oferta_editar'),
    path('oferta/eliminar/<int:pk>/', OfertaDeleteView.as_view(), name='oferta_eliminar'),
    # ventas
    path('ventas/lista/', VentaListView.as_view(), name='venta_lista'),
    path('ventas/crear/', VentaCreateView.as_view(), name='venta_crear'),
    path('ventas/editar/<int:pk>/', VentaUpdateView.as_view(), name='venta_editar'),
    path('ventas/eliminar/<int:pk>/', VentaDeleteView.as_view(), name='venta_eliminar'),
    path('ventas/factura/pdf/<int:pk>/', VentaFacturaPdfView.as_view(), name='venta_factura'),
    # Super tienda
    path('super/lista/', SuperListView.as_view(), name='super_lista'),
    path('super/lista/<str:pk>/', SuperListView.as_view(), name='super_lista_id'),
    # Cesta tienda
    path('cesta/lista/', CestaListView.as_view(), name='cesta_lista'),
    path('cesta/eliminar/<int:pk>/', CestaDeleteView.as_view(), name='cesta_eliminar'),
    path('cesta/factura/pdf/<int:pk>/', CestaFacturaPdfView.as_view(), name='cesta_factura'),
    # muestra oferta
    path('muestraoferta/lista/', MuestraOfertasListView.as_view(), name='muestra_oferta_lista'),
    # favoritos
    path('favoritos/lista/', FavoritosListView.as_view(), name='favoritos_lista'),
    path('favoritos/eliminar/<int:pk>/', FavoritosDeleteView.as_view(), name='favoritos_eliminar'),
    path('favoritos/agregar_cesta/<int:pk>/', FavoritosCestaCreateView.as_view(), name='favoritos_agregar'),
    # gestiona favoritos
    path('gestiona_favoritos/lista/', GestionaFavoritosListView.as_view(), name='gestiona_favoritosLista'),
    # gestiona productos
    path('gestiona/lista/', GestionaProductosListView.as_view(), name='gestiona_lista'),
    path('gestiona/crear/', GestionaProductosCreateView.as_view(), name='gestiona_crear'),
    path('gestiona/editar/<int:pk>/', GestionaProductosUpdateView.as_view(), name='gestiona_editar'),
    path('gestiona/eliminar/<int:pk>/', GestionaProductosDeleteView.as_view(), name='gestiona_eliminar'),
    # Importar CSV
    path('importar/lista/', ImportarCSVListView.as_view(), name='importar_lista'),
    path('importar/editar/<int:pk>/', ImportarCSVUpdateView.as_view(), name='importar_editar'),
    path('importar/eliminar/<int:pk>/', ImportarCSVDeleteView.as_view(), name='importar_eliminar'),
    # inicio
    path('panelcontrol/', PanelControlView.as_view(), name='panel_control'),
    # test
    path('test/', TestView.as_view(), name='test'),
]

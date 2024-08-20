from django.urls import path

from aplicaciones.usuarios.views import *

app_name = 'usuario'

urlpatterns = [
    # usuarios
    path('lista/', UsuarioListView.as_view(), name='usuario_lista'),
    path('crear/', UsuarioCreateView.as_view(), name='usuario_crear'),
    path('editar/<int:pk>/', UsuarioUpdateView.as_view(), name='usuario_editar'),
    path('eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='usuario_eliminar'),
    path('cambia/grupo/<int:pk>/', MiView.as_view(), name='usuario_grupo'),
    # path('perfil/', UsuarioPerfilView.as_view(), name='usuario_perfil'),
]

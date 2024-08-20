"""configuracion URL Configuration

The `urlpatterns` list routes URLs to oferta. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function oferta
    1. Add an import:  from my_app import oferta
    2. Add a URL to urlpatterns:  path('', oferta.home, name='home')
Class-based oferta
    1. Add an import:  from other_app.oferta import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from aplicaciones.paginainicio.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='inicio'),                                        # página de inicio
    path('adm/', include('aplicaciones.administrador.urls')),                            # llama a tienda
    path('login/', include('aplicaciones.login.urls')),
    path('reporte/', include('aplicaciones.reportes.urls')),
    path('usuario/', include('aplicaciones.usuarios.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

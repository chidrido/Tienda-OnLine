from django.urls import path

from aplicaciones.reportes.views import ReporteVentaView

app_name = 'reporte'

urlpatterns = [
    # reportes
    path('venta/', ReporteVentaView.as_view(), name='venta_reporte'),
]

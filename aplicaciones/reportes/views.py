from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from aplicaciones.administrador.models import Venta
from aplicaciones.reportes.forms import ReporteForm


class ReporteVentaView(TemplateView):
    template_name = 'venta/reporte.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'busca_reportes':
                data = []
                comienza_datos = request.POST.get('comienza_datos', '')
                acaba_datos = request.POST.get('acaba_datos', '')
                buscar = Venta.objects.all()
                if len(comienza_datos) and len(acaba_datos):
                    buscar = buscar.filter(date_joined__range=[comienza_datos, acaba_datos])
                for s in buscar:
                    data.append([
                        s.id,
                        s.cliente.first_name,
                        s.cliente.last_name,
                        s.date_joined.strftime('%Y-%m-%d'),
                        format(s.subtotal, '.2f'),
                        format(s.iva, '.2f'),
                        format(s.total, '.2f'),
                    ])

                subtotal = buscar.aggregate(r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')

                data.append([
                    '---',
                    '---',
                    '---',
                    '---',
                    format(subtotal, '.2f'),
                ])

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Reporte de Ventas'
        context['entidad'] = 'Reportes'
        context['lista_url'] = reverse_lazy('venta_reporte')
        context['form'] = ReporteForm()
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context

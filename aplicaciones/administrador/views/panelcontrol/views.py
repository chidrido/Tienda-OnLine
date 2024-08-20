from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Coalesce
from django.db.models import Sum, DecimalField
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from datetime import datetime
from aplicaciones.administrador.mixins import ValidatePermissionRequiredMixin
from aplicaciones.administrador.models import Venta, Producto, DetVenta, Categoria, Importar


class PanelControlView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'panel_control.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        data = {}
        try:
            action = request.POST['action']
            if action == 'grafico_ventas_mes':
                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.get_grafico_ventas_mes()
                }
            elif action == 'get_grafico_productos_mes_ano':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.get_grafico_productos_mes_ano(),
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_grafico_ventas_mes(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Venta.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                data.append(float(total))
        except:
            pass
        return data

    def get_grafico_productos_mes_ano(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for p in Producto.objects.all():
                total = DetVenta.objects.filter(venta__date_joined__year=year, venta__date_joined__month=month, prod__id=p.id).aggregate(
                    r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                if total > 0:
                    data.append({
                        'name': p.nombre,
                        'y': float(total)
                    })
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['grafico_ventas_mes'] = self.get_grafico_ventas_mes()
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context

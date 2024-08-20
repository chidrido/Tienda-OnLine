from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from datetime import datetime
from aplicaciones.administrador.mixins import ValidatePermissionRequiredMixin
from aplicaciones.administrador.models import Categoria, Venta, Producto, DetVenta


class GestionaFavoritosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Producto
    template_name = 'gestiona_favoritos/gestionafavoritos_Lista.html'
    permission_required = 'aplicaciones.view_categoria'

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
                        'codigo': p.codigo,
                        'nombre': p.nombre,
                        'cat': p.cat.nombre,
                        'subcat': p.subcat.nombre,
                        'total': float(total)
                    })
        except:
            pass
        return data

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'busca_datos':
                data = []
                var = self.get_grafico_productos_mes_ano()
                for i in var:
                    data.append(i)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # devuelve un diccionario
        context['titulo'] = 'Listado de Categorías'
        context['entidad'] = 'Categorías'
        context['lista_url'] = reverse_lazy('administrador:categoria_lista')
        context['crear_url'] = reverse_lazy('administrador:categoria_crear')
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context

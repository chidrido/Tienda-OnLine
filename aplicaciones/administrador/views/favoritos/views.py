from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView, CreateView
from aplicaciones.administrador.models import Favoritos, Cesta, Producto
from django.urls import reverse_lazy


class FavoritosListView(LoginRequiredMixin, ListView):
    model = Favoritos
    template_name = 'favoritos/favoritos_lista.html'
    # permission_required = 'aplicaciones.view_favoritos'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            id_cliente = request.user.id
            if action == 'busca_datos':
                data = []
                for i in Favoritos.objects.filter(id_cliente=id_cliente):
                    item = i.toJSON()
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # devuelve un diccionario
        context['titulo'] = 'Listado de Favoritos'
        context['entidad'] = 'Favoritos'
        return context


class FavoritosDeleteView(LoginRequiredMixin, DeleteView):
    model = Favoritos
    template_name = 'favoritos/eliminar.html'
    success_url = reverse_lazy('administrador:favoritos_lista')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lista_url'] = reverse_lazy('administrador:favoritos_lista')
        # halla el nombre del producto y lo muestra en context
        objeto = Favoritos.objects.filter(id_cliente=self.request.user.id).get(id=self.kwargs['pk'])
        datos = objeto.toJSON()['id_producto']
        context['nombre'] = datos['nombre']
        return context


class FavoritosCestaCreateView(LoginRequiredMixin, ListView):
    model = Cesta
    template_name = 'favoritos/agregar_cesta.html'
    # permission_required = 'aplicaciones.view_favoritos'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        # print(request.POST)
        try:
            action = request.POST['action']
            id_cliente = request.user.id
            if action == 'agregar_cesta':
                print(id_cliente)
                print(request.POST)
                pk = self.kwargs['pk']
                print('pk', pk)
                producto = Producto.objects.get(id=pk)
                comprueba = Cesta.objects.filter(id_cliente=id_cliente).filter(id_producto_id=pk)
                if not comprueba:
                    print('comprueba', comprueba)
                    with transaction.atomic():
                        ces = Cesta()
                        ces.id_cliente = id_cliente
                        ces.id_producto_id = producto.id
                        print('producto.id:', producto.id)
                        ces.cuartos = ''
                        comp_cuarto = Producto.objects.filter(id=producto.id).filter(cuartos=True)
                        if comp_cuarto:
                            ces.cuartos = 'unidad'
                            ces.cuartos_checkbox = True
                        ces.cant = 1
                        ces.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # devuelve un diccionario
        context['titulo'] = 'Listado de Favoritos'
        context['entidad'] = 'Favoritos'
        var_nombre = Producto.objects.get(id=self.kwargs['pk'])
        nombre = var_nombre.nombre
        context['nombre'] = nombre
        return context

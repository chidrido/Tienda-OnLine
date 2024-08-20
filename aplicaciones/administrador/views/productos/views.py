from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from aplicaciones.administrador.forms import ProductoForm
from aplicaciones.administrador.mixins import ValidatePermissionRequiredMixin
from aplicaciones.administrador.models import Producto, SubCategoria, Categoria, Cliente, Venta


class ProductoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Producto
    template_name = 'producto/lista.html'
    success_url = reverse_lazy('administrador:producto_lista')
    url_redirect = success_url
    permission_required = 'aplicaciones.change_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            action = request.POST['action']
            if action == 'busca_datos':
                for i in Producto.objects.all():
                    data.append(i.toJSON())
            elif action == 'busca_datos_categoria':
                cate = request.POST['datos']
                if cate == 'Todos':
                    for i in Producto.objects.all():
                        data.append(i.toJSON())
                else:
                    for i in Producto.objects.filter(cat_id=cate):
                        data.append(i.toJSON())
            elif action == 'selecciona_checkbox':
                valor_id = request.POST['valor']
                checked = request.POST['checked']
                if checked == 'true':
                    checked = True
                else:
                    checked = False
                Producto.objects.filter(codigo=valor_id).update(oferta_checkbox=checked)
            elif action == 'selecciona_checkbox_ayala':
                valor_id = request.POST['valor']
                checked = request.POST['checked']
                if checked == 'true':
                    checked = True
                else:
                    checked = False
                Producto.objects.filter(codigo=valor_id).update(especial=checked)
            elif action == 'selecciona_checkbox_activos':
                valor_id = request.POST['valor']
                checked = request.POST['checked']
                if checked == 'true':
                    checked = True
                else:
                    checked = False
                Producto.objects.filter(codigo=valor_id).update(activo=checked)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Productos'
        context['crear_url'] = reverse_lazy('administrador:producto_crear')
        context['lista_url'] = reverse_lazy('administrador:producto_lista')
        context['entidad'] = 'Productos'
        context['categorias'] = Categoria.objects.all()
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class ProductoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear.html'
    success_url = reverse_lazy('administrador:producto_lista')
    permission_required = 'aplicaciones.add_producto'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            elif action == 'buscar_subcat_id':
                data = []
                for i in SubCategoria.objects.filter(cat_id=request.POST['id']):
                    data.append({'id': i.id, 'nombre': i.nombre})
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Producto'
        context['entidad'] = 'Productos'
        context['lista_url'] = self.success_url
        context['action'] = 'add'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class ProductoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear.html'
    success_url = reverse_lazy('administrador:producto_lista')
    permission_required = 'aplicaciones.change_producto'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Producto'
        context['entidad'] = 'Productos'
        context['lista_url'] = self.success_url
        context['action'] = 'edit'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class ProductoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Producto
    template_name = 'producto/eliminar.html'
    success_url = reverse_lazy('administrador:producto_lista')
    permission_required = 'aplicaciones.delete_producto'
    url_redirect = success_url

    @method_decorator(login_required)
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
        context['titulo'] = 'Eliminar Producto'
        context['entidad'] = 'Productos'
        context['lista_url'] = self.success_url
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context

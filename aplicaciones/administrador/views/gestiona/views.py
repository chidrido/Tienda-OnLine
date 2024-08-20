from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from aplicaciones.administrador.forms import GestionaForm, ProductoForm
from aplicaciones.administrador.models import Categoria, Venta, Producto, SubCategoria, Cesta
from aplicaciones.administrador.mixins import ValidatePermissionRequiredMixin


class GestionaProductosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Producto
    template_name = 'gestiona/lista.html'
    permission_required = 'aplicaciones.view_producto'
    permission_required = 'aplicaciones.change_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            print(request.POST)
            action = request.POST['action']
            if action == 'busca_datos':
                for i in Producto.objects.filter(cat__nombre='Frutería'):
                    data.append(i.toJSON())
            elif action == 'busca_subcategoria':
                data = [{'id': '', 'text': '------------'}]
                for i in SubCategoria.objects.filter(cat_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.nombre, 'data': i.cat.toJSON()})
            elif action == 'busca_productos':
                id_subcat = request.POST['id']
                for i in Producto.objects.filter(subcat_id=id_subcat):
                    data.append(i.toJSON())
            elif action == 'busca_todo':
                for i in Producto.objects.all():
                    data.append(i.toJSON())
            elif action == 'selecciona_checkbox':
                print(request.POST)
                valor_id = request.POST['valor']
                checked = request.POST['checked']
                if checked == 'true':
                    checked = True
                else:
                    checked = False
                Producto.objects.filter(id=valor_id).update(activo=checked)
            elif action == 'selecciona_checkboxoferta':
                valor_id = request.POST['valor']
                checked = request.POST['checked']
                if checked == 'true':
                    checked = True
                else:
                    checked = False
                Producto.objects.filter(id=valor_id).update(oferta_checkbox=checked)
            elif action == 'selecciona_especial':
                valor_id = request.POST['valor']
                checked = request.POST['checked']
                if checked == 'true':
                    checked = True
                else:
                    checked = False
                Producto.objects.filter(id=valor_id).update(especial=checked)
            elif action == 'selecciona_cuartos':
                valor_id = request.POST['valor']
                checked = request.POST['checked']
                if checked == 'true':
                    checked = True
                else:
                    checked = False
                Producto.objects.filter(id=valor_id).update(cuartos=checked)
                if checked:
                    Cesta.objects.filter(id_producto=valor_id).update(cuartos='unidad', cuartos_checkbox=checked)
                else:
                    Cesta.objects.filter(id_producto=valor_id).update(cuartos='', cuartos_checkbox=checked)

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestionar los Productos'
        context['lista_url'] = reverse_lazy('administrador:gestiona_lista')
        context['crear_url'] = reverse_lazy('administrador:gestiona_crear')
        context['entidad'] = 'Gestionar'
        context['subcategorias'] = SubCategoria.objects.all()[0:3]
        context['form'] = GestionaForm()
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class GestionaProductosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'gestiona/editar.html'
    success_url = reverse_lazy('administrador:gestiona_lista')
    permission_required = 'aplicaciones.change_producto'
    url_redirect = success_url

    # @method_decorator(login_required)
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
        context['titulo'] = 'Editar Producto Gestionado'
        context['entidad'] = 'Gestionar'
        context['lista_url'] = self.success_url
        context['action'] = 'edit'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class GestionaProductosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Producto
    template_name = 'gestiona/eliminar.html'
    success_url = reverse_lazy('administrador:gestiona_lista')
    permission_required = 'aplicaciones.delete_producto'
    url_redirect = success_url

    # @method_decorator(login_required)
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
        context['titulo'] = 'Eliminar Producto Gestionado'
        context['entidad'] = 'Gestionar'
        context['lista_url'] = self.success_url
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class GestionaProductosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'gestiona/crear.html'
    success_url = reverse_lazy('administrador:gestiona_lista')
    permission_required = 'aplicaciones.add_producto'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear un Producto nuevo'
        context['entidad'] = 'Gestionar'
        context['lista_url'] = self.success_url
        context['action'] = 'add'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context

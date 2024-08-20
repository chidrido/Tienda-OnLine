from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from aplicaciones.administrador.forms import CategoriaForm, SubCategoriaForm
from aplicaciones.administrador.mixins import ValidatePermissionRequiredMixin
from aplicaciones.administrador.models import SubCategoria, Venta, Categoria, Producto


class SubCategoriaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = SubCategoria
    template_name = 'subcategoria/lista.html'
    permission_required = 'aplicaciones.view_subcategoria'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(request.POST)
            if action == 'busca_datos':
                data = []
                for i in SubCategoria.objects.all():
                    data.append(i.toJSON())
            elif action == 'busca_datos_subcategoria':
                data = []
                cate = request.POST['datos']
                for i in SubCategoria.objects.filter(cat_id=cate):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # devuelve un diccionario
        context['titulo'] = 'Listado de Subcategorías'
        context['entidad'] = 'Subcategorías'
        context['lista_url'] = reverse_lazy('administrador:subcategoria_lista')
        context['crear_url'] = reverse_lazy('administrador:subcategoria_crear')
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        context['categorias'] = Categoria.objects.all()
        return context


class SubCategoriaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    url_redirect = reverse_lazy('administrador:subcategoria_lista')
    model = SubCategoria
    form_class = SubCategoriaForm
    template_name = 'subcategoria/crear.html'
    permission_required = 'aplicaciones.add_subcategoria'
    success_url = reverse_lazy('administrador:subcategoria_lista')

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
        context['titulo'] = 'Crear Subcategorías'
        context['entidad'] = 'Subcategorías'
        context['lista_url'] = reverse_lazy('administrador:subcategoria_lista')
        context['action'] = 'add'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class SubCategoriaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = SubCategoria
    form_class = SubCategoriaForm
    template_name = 'subcategoria/crear.html'
    permission_required = 'aplicaciones.change_subcategoria'
    success_url = reverse_lazy('administrador:subcategoria_lista')

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
        context['titulo'] = 'Editar una subcategoria'
        context['entidad'] = 'Subcategorías'
        context['lista_url'] = reverse_lazy('administrador:subcategoria_lista')
        context['action'] = 'edit'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class SubCategoriaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = SubCategoria
    template_name = 'subcategoria/eliminar.html'
    success_url = reverse_lazy('administrador:subcategoria_lista')
    permission_required = 'aplicaciones.delete_subcategoria'

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):                           # el método 'dispatch' redirecciona
        self.object = self.get_object()                                     # según el parámetro sea tipo POST o GET
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
        context['titulo'] = 'Eliminar una Categoría'
        context['entidad'] = 'Subcategorías'
        context['lista_url'] = reverse_lazy('administrador:subcategoria_lista')
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class SubCategoriaFormView(LoginRequiredMixin, ValidatePermissionRequiredMixin, FormView):
    form_class = SubCategoriaForm
    template_name = 'subcategoria/crear.html'
    success_url = reverse_lazy('administrador:subcategoria_lista')

    def form_valid(self, form):
        print(form.is_valid())
        # print(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.is_valid())
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario | Subcategoría'
        context['entidad'] = 'Subcategorías'
        context['lista_url'] = reverse_lazy('administrador:subcategoria_lista')
        context['action'] = 'add'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context

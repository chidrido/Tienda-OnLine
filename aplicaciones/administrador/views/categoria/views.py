from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from aplicaciones.administrador.forms import CategoriaForm
from aplicaciones.administrador.mixins import ValidatePermissionRequiredMixin
from aplicaciones.administrador.models import Categoria, Venta


class CategoriaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Categoria
    template_name = 'categoria/lista.html'
    permission_required = 'aplicaciones.view_categoria'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'busca_datos':
                data = []
                posicion = 1
                for i in Categoria.objects.all():
                    item = i.toJSON()
                    item['posicion'] = posicion
                    data.append(item)
                    posicion += 1
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


class CategoriaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria/crear.html'
    success_url = reverse_lazy('administrador:categoria_lista')
    permission_required = 'aplicaciones.add_categoria'
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
        context['titulo'] = 'Crear Categorías'
        context['entidad'] = 'Categorías'
        context['lista_url'] = self.success_url
        context['action'] = 'add'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class CategoriaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria/crear.html'
    success_url = reverse_lazy('administrador:categoria_lista')
    permission_required = 'aplicaciones.change_categoria'
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
        context['titulo'] = 'Editar una Categoria'
        context['entidad'] = 'Categorias'
        context['lista_url'] = self.success_url
        context['action'] = 'edit'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class CategoriaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'categoria/eliminar.html'
    success_url = reverse_lazy('administrador:categoria_lista')
    permission_required = 'aplicaciones.delete_categoria'
    url_redirect = success_url

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
        context['entidad'] = 'Categorías'
        context['lista_url'] = self.success_url
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class CategoriaFormView(FormView):
    form_class = CategoriaForm
    template_name = 'categoria/crear.html'
    success_url = reverse_lazy('administrador:categoria_lista')

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
        context['titulo'] = 'Formulario | Categoría'
        context['entidad'] = 'Categorias'
        context['lista_url'] = reverse_lazy('administrador:categoria_lista')
        context['action'] = 'add'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context

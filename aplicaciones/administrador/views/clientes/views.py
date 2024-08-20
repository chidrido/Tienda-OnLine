from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import csrf_token
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from aplicaciones.administrador.forms import ClienteForm
from aplicaciones.administrador.mixins import ValidatePermissionRequiredMixin
from aplicaciones.administrador.models import Cliente, Cesta, Venta


class ClienteListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Cliente
    template_name = 'cliente/lista.html'
    permission_required = 'administrador.view_cliente'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'busca_datos':
                print(request.POST)
                data = []
                for i in Cliente.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Clientes'
        context['crear_url'] = reverse_lazy('administrador:cliente_crear')
        context['lista_url'] = reverse_lazy('administrador:cliente_lista')
        context['entidad'] = 'Clientes'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class ClienteCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/crear.html'
    success_url = reverse_lazy('administrador:cliente_lista')
    permission_required = 'aplicaciones.add_cliente'
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
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear un Cliente'
        context['entidad'] = 'Clientes'
        context['lista_url'] = self.success_url
        context['action'] = 'add'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/crear.html'
    success_url = reverse_lazy('administrador:cliente_lista')
    permission_required = 'administrador.change_cliente'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(request.POST)
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
        context['titulo'] = 'Editar un Cliente'
        context['entidad'] = 'Clientes'
        context['lista_url'] = self.success_url
        context['action'] = 'edit'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class ClienteDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'cliente/eliminar.html'
    success_url = reverse_lazy('administrador:cliente_lista')
    permission_required = 'administrador.delete_cliente'
    url_redirect = success_url

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
        context['titulo'] = 'Eliminar Cliente'
        context['entidad'] = 'Clientes'
        context['lista_url'] = self.success_url
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class ClienteSuperCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/crear_super.html'
    success_url = reverse_lazy('perfil:login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = ClienteForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(self.success_url)
                self.object = None
                context = self.get_context_data(**kwargs)
                context['form'] = form
                return render(request, self.template_name, context)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['texto'] = 'Cree su perfil de usuario para iniciar la compra'
        context['super_url'] = self.success_url
        context['action'] = 'add'
        return context


class ClienteSuperUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/editar_super.html'
    success_url = reverse_lazy('administrador:super_lista')
    # permission_required = 'administrador.change_cliente'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            print(request.POST)
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
        print(self.object)
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Perfil'
        context['action'] = 'edit'
        context['texto'] = 'Editar Perfil de Usuario'
        context['lista_url'] = self.success_url
        return context

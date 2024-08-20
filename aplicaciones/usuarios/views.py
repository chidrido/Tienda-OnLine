from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from aplicaciones.administrador.forms import ClienteForm
from aplicaciones.administrador.mixins import ValidatePermissionRequiredMixin
from aplicaciones.administrador.models import Cliente, Venta
from aplicaciones.usuarios.forms import UsuarioForm
from aplicaciones.usuarios.models import Usuario


class UsuarioListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuario/lista.html'
    permission_required = 'usuario.view_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'busca_datos':
                data = []
                for i in Usuario.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # devuelve un diccionario
        context['titulo'] = 'Listado de Usuarios'
        context['entidad'] = 'Usuarios'
        context['lista_url'] = reverse_lazy('usuario:usuario_lista')
        context['crear_url'] = reverse_lazy('usuario:usuario_crear')
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class UsuarioCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/crear.html'
    success_url = reverse_lazy('usuario:usuario_lista')
    permission_required = 'usuario.add_usuario'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'añadir':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Usuario'
        context['entidad'] = 'Usuario'
        context['lista_url'] = self.success_url
        context['action'] = 'añadir'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class UsuarioUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/crear.html'
    success_url = reverse_lazy('usuario:usuario_lista')
    permission_required = 'usuario.change_usuario'
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
        context['titulo'] = 'Editar Usuarios'
        context['entidad'] = 'Usuarios'
        context['lista_url'] = self.success_url
        context['action'] = 'edit'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class UsuarioDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuario/eliminar.html'
    success_url = reverse_lazy('usuario:usuario_lista')
    permission_required = 'usuario.change_usuario'
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
        context['titulo'] = 'Eliminar Usuario'
        context['entidad'] = 'Usuario'
        context['lista_url'] = self.success_url
        context['action'] = 'delete'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class MiView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('administrador:panel_control'))


# class UsuarioPerfilView(LoginRequiredMixin, UpdateView):
#     model = Cliente
#     form_class = ClienteForm
#     template_name = 'usuario/editar_super.html'
#     success_url = reverse_lazy('administrador:super_lista')
#
#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_object(self, queryset=None):
#         return self.request.user
#     #
#     # def post(self, request, *args, **kwargs):
#     #     data = {}
#     #     try:
#     #         print(request.POST)
#     #
#     #         # action = request.POST['action']
#     #         # if action == 'edit':
#     #         #     form = self.get_form()
#     #         #     data = form.save()
#     #         # else:
#     #         #     data['error'] = 'No ha ingresado a ninguna opción'
#     #     except Exception as e:
#     #         data['error'] = str(e)
#     #     return JsonResponse(data)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['titulo'] = 'Editar Perfil'
#         context['entidad'] = 'Perfil'
#         # context['texto'] = 'Cree su perfil de usuario para iniciar la compra'
#         context['lista_url'] = self.success_url
#         return context

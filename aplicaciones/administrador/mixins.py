from crum import get_current_request
from django.shortcuts import redirect
from datetime import datetime
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context


class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('inicio')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tiene permiso para ingresar a este módulo')
        return HttpResponseRedirect(self.get_url_redirect())

    # def get_url_redirect(self):
    #     if self.url_redirect is None:
    #         return reverse_lazy('inicio')
    #     return self.url_redirect
    #
    # def dispatch(self, request, *args, **kwargs):
    #     request = get_current_request()
    #     if 'group' in request.session:
    #         group = request.session['group']
    #         # group = Group.objects.get(pk=1)
    #         if group.permissions.filter(codename=self.permission_required):
    #             return super().dispatch(request, *args, **kwargs)
    #     messages.error(request, 'No tiene permiso para ingresar a este módulo')
    #     return HttpResponseRedirect(self.get_url_redirect())
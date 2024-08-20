import json
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa

from aplicaciones.administrador.forms import VentaForm, ClienteForm
from aplicaciones.administrador.mixins import ValidatePermissionRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from aplicaciones.administrador.models import Venta, Producto, DetVenta, Cliente
from configuracion import settings


class VentaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'ventas/lista.html'
    permission_required = 'aplicaciones.view_venta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'busca_datos':
                data = []
                for i in Venta.objects.filter(pedido_checkbox=True):
                    data.append(i.toJSON())
            elif action == 'no_hechos':
                data = []
                for i in Venta.objects.filter(pedido_checkbox=True):
                    data.append(i.toJSON())
            elif action == 'hechos':
                data = []
                for i in Venta.objects.filter(pedido_checkbox=False):
                    data.append(i.toJSON())
            elif action == 'todos':
                data = []
                for i in Venta.objects.all():
                    data.append(i.toJSON())
                print(data)
            elif action == 'busqueda_detalles_producto':
                data = []
                for i in DetVenta.objects.filter(venta_id=request.POST['id']):
                    item = i.toJSON()
                    item['mensaje'] = i.mensaje
                    data.append(item)
            elif action == 'checkbox_pedidos':
                print(request.POST)
                id_venta = request.POST['id']
                estado = request.POST['checked']
                if estado == 'true':
                    estado = True
                else:
                    estado = False
                Venta.objects.filter(id=id_venta).update(pedido_checkbox=estado)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Pedidos'
        context['crear_url'] = reverse_lazy('administrador:venta_crear')
        context['lista_url'] = reverse_lazy('administrador:venta_lista')
        context['entidad'] = 'Pedidos'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class VentaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'ventas/crear.html'
    success_url = reverse_lazy('administrador:venta_lista')
    permission_required = 'aplicaciones.add_venta'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(request.POST)
            if action == 'busca_productos':
                data = []
                term = request.POST['term']
                productos = Producto.objects.filter()
                if len(term):
                    productos = productos.filter(nombre__icontains=term)
                for i in productos[0:10]:
                    item = i.toJSON()
                    item['value'] = i.nombre                # opción para input
                    # item['text'] = i.nombre               # opción para select2
                    data.append(item)
            elif action == 'busca_productos_select':
                data = []
                terms = request.POST['term']
                data.append({'id': terms, 'text': terms})
                productos = Producto.objects.filter(nombre__icontains=terms)
                for i in productos[0:10]:
                    item = i.toJSON()
                    # item['value'] = i.nombre            # opción para input
                    item['text'] = i.nombre               # opción para select2
                    data.append(item)
            elif action == 'busca_productos_por_codigo':
                data = []
                term = request.POST['term']
                data.append({'id': term, 'text': term})
                productos = Producto.objects.filter(codigo=term)
                for i in productos[0:10]:
                    item = i.toJSON()
                    # item['value'] = i.nombre              # opción para input
                    item['text'] = i.codigo                 # opción para select2
                    data.append(item)
            elif action == 'buscar_clientes':
                data = []
                cliente = Cliente.objects.filter(first_name__icontains=request.POST['term'])[0:10]
                for i in cliente:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'crear_cliente':
                print(request.POST)
                frmCliente = ClienteForm(request.POST)
                data = frmCliente.save()
            elif action == 'add':
                with transaction.atomic():
                    ventas = json.loads(request.POST['ventas'])
                    venta = Venta()
                    venta.date_joined = ventas['date_joined']
                    venta.cliente_id = ventas['cliente']
                    venta.subtotal = float(ventas['subtotal'])
                    venta.iva = float(ventas['iva'])
                    venta.total = float(ventas['total'])
                    venta.save()
                    for i in ventas['productos']:
                        det = DetVenta()
                        det.venta_id = venta.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.precio = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': venta.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creación de una Venta'
        context['entidad'] = 'Pedidos'
        context['lista_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['frmCliente'] = ClienteForm()
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class VentaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Venta
    form_class = VentaForm
    template_name = 'ventas/crear.html'
    success_url = reverse_lazy('administrador:venta_lista')
    permission_required = 'aplicaciones.change_venta'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'busca_productos':
                data = []
                term = request.POST['term']
                productos = Producto.objects.filter()
                if len(term):
                    productos = productos.filter(nombre__icontains=term)
                for i in productos[0:10]:
                    item = i.toJSON()
                    item['value'] = i.nombre            # opción para input
                    # item['text'] = i.nombre           # opción para select2
                    data.append(item)
            elif action == 'busca_productos_select':
                data = []
                terms = request.POST['term']
                data.append({'id': terms, 'text': terms})
                productos = Producto.objects.filter(nombre__icontains=terms)
                for i in productos[0:10]:
                    item = i.toJSON()
                    # item['value'] = i.nombre            # opción para input
                    item['text'] = i.nombre           # opción para select2
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    ventas = json.loads(request.POST['ventas'])
                    # venta = Venta.objects.get(pk=self.get_object().id)            Cualquiera de estas dos maneras funciona
                    venta = self.get_object()
                    venta.date_joined = ventas['date_joined']
                    venta.cliente_id = ventas['cliente']
                    venta.subtotal = float(ventas['subtotal'])
                    venta.iva = float(ventas['iva'])
                    venta.total = float(ventas['total'])
                    venta.save()
                    for i in venta.detventa_set.all():
                        i.delete()
                    for i in ventas['productos']:
                        det = DetVenta()
                        det.venta_id = venta.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.precio = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': venta.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_productos_detalles(self):
        data = []
        try:
            for i in DetVenta.objects.filter(venta_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edición de una Venta'
        context['entidad'] = 'Pedidos'
        context['lista_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_productos_detalles())
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class VentaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Venta
    template_name = 'ventas/eliminar.html'
    success_url = reverse_lazy('administrador:venta_lista')
    permission_required = 'aplicaciones.delete_venta'
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
        context['titulo'] = 'Eliminación de un pedido'
        context['entidad'] = 'Pedidos'
        context['lista_url'] = self.success_url
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class VentaFacturaPdfView(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('ventas/factura.html')
            context = {
                'venta': Venta.objects.get(pk=self.kwargs['pk']),
                'comp': {
                    'nombre': 'Famisuper',
                    'direccion': 'Calle Manuel Gonzalez Rodriguez, 14 . Santiponce(Sevilla)',
                    'teléfono': '955997472',
                    'email': 'famisuper@outlook.com',
                }
            }
            html = template.render(context)

            response = HttpResponse(content_type='application/pdf')

            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                # link_callback=self.link_callback,
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('administrador:venta_factura'))

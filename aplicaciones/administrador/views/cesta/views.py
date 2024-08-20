import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from datetime import datetime

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView
from xhtml2pdf import pisa

from aplicaciones.administrador.models import Cesta, Cliente, DetVenta, Venta
from configuracion import settings
from aplicaciones.usuarios.models import Usuario
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.template.loader import render_to_string, get_template


class CestaListView(LoginRequiredMixin, ListView):
    model = Cesta
    template_name = 'cesta/lista_cesta.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):  # el método 'dispatch' redirecciona
        return super().dispatch(request, *args, **kwargs)

    # envía email al finalizar la compra
    def enviar_email(self, user):
        data = []
        try:
            print(user)
            # URL = settings.DOMINIO if not settings.DEBUG else self.request.META['HTTP_HOST']
            #
            # user.token = uuid.uuid4()
            # user.save()
            var_email = ''
            var_nombre = ''
            user = Usuario.objects.filter(id=user)
            for i in user:
                item = i.toJSON()
                var_email = item['email']
                var_nombre = item['first_name']
                data.append(item)
            print(var_nombre)

            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            email_to = var_email
            mensaje = MIMEMultipart()
            mensaje['From'] = settings.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = 'Confirmación de compra'

            context = render_to_string('cesta/enviar_emailCesta.html', {
                'user': var_nombre,
                # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                'link_resetpwd': '',
                # 'link_home': 'http://{}'.format(URL)
                'link_home': ''
            })
            mensaje.attach(MIMEText(context, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())

        except Exception as e:
            data['error'] = str(e)
        return data

    # calcula los subtotales de la tabla con diccionario
    def calcula_subtotal(self, diccionario):
        var_cuartos = diccionario['cuartos']
        if var_cuartos == '':
            var_cuartos = int(1)
        elif var_cuartos == 'cuarto':
            var_cuartos = float(0.25)
        elif var_cuartos == 'medio':
            var_cuartos = float(0.50)
        elif var_cuartos == 'unidad':
            var_cuartos = int(1)
        precio = diccionario['id_producto'].get('pvp')
        cantidad = diccionario['cant']
        subtotal = (float(precio) * int(cantidad)) * var_cuartos
        return subtotal

    # calcula la cuenta total
    def calcula_total(self):
        id_cliente = self.request.user.id
        var_total = 0
        total = 0
        for i in Cesta.objects.filter(id_cliente=id_cliente).filter(id_producto__activo=True):
            diccionario = i.toJSON()
            precio = diccionario['id_producto'].get('pvp')
            cant = diccionario['cant']
            cuartos = diccionario['cuartos']
            if cuartos is None:
                cuartos = int(1)
            elif cuartos == '':
                cuartos = int(1)
            elif cuartos == 'cuarto':
                cuartos = float(0.25)
            elif cuartos == 'medio':
                cuartos = float(0.50)
            elif cuartos == 'unidad':
                cuartos = int(1)
            subtotal_fila = (float(precio) * int(cant)) * cuartos
            subtotal = round(subtotal_fila, 2)
            var_total += subtotal
            total = var_total
        return "{0:.2f}".format(total)

    def calcula(self, id_cliente, id_producto, precio, cant):
        cuenta = {}
        Cesta.objects.filter(id_cliente=id_cliente).filter(id=id_producto).update(cant=cant)
        var_cuartos = Cesta.objects.filter(id_cliente=id_cliente).filter(id=id_producto).values('cuartos')
        for i in var_cuartos:
            cuartos = i['cuartos']
            if cuartos == '':
                subtotal_fila = float(precio) * int(cant)
                subtotal = "{0:.2f}".format(subtotal_fila)
                cuenta['cuenta_subtotal'] = subtotal
                return cuenta
            else:
                if cuartos == 'cuarto':
                    cuartos = float(0.25)
                elif cuartos == 'medio':
                    cuartos = float(0.5)
                elif cuartos == 'unidad':
                    cuartos = 1
                subtotal_fila = (float(precio) * int(cant)) * cuartos
                subtotal = round(subtotal_fila, 2)
                cuenta['cuenta_subtotal'] = "{0:.2f}".format(subtotal)
                return cuenta

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            id_cliente = request.user.id
            if action == 'busca_datos_cesta':
                data = []
                for i in Cesta.objects.filter(id_cliente=id_cliente).filter(id_producto__activo=True):
                    datos = {}
                    diccionario = i.toJSON()
                    datos['id'] = diccionario['id']
                    datos['id_prod'] = diccionario['id_producto'].get('id_producto_id')
                    datos['imagen'] = diccionario['id_producto'].get('imagen')
                    datos['cat'] = diccionario['id_producto'].get('cat')
                    datos['subcat'] = diccionario['id_producto'].get('subcat')
                    datos['nombre'] = diccionario['id_producto'].get('nombre')
                    datos['pvp'] = diccionario['id_producto'].get('pvp')
                    datos['cant'] = diccionario['cant']
                    datos['id_cliente'] = diccionario['id_cliente']
                    datos['cuartos'] = diccionario['id_producto'].get('cuartos')
                    datos['lista_cuartos'] = diccionario['cuartos']
                    subtotal = self.calcula_subtotal(diccionario)  # llama a la función calcula
                    datos['subtotal'] = subtotal
                    data.append(datos)
            elif request.POST['action'] == 'accion_cant':
                precio = request.POST['data[precio]']
                cant = request.POST['data[cantidad]']
                id_producto = request.POST['data[id_prod]']
                datos = self.calcula(id_cliente, id_producto, precio, cant)
                datos['total'] = self.calcula_total()
                data = {'cuenta': datos}
            elif request.POST['action'] == 'accion_cuartos':
                print(request.POST)
                data = []
                id_cesta = request.POST['data[id_prod]']
                cuartos = request.POST['data[cuartos]']
                Cesta.objects.filter(id=id_cesta).update(cuartos=cuartos)
                if cuartos == '':
                    cuartos = 'cuarto'
                precio = request.POST['data[precio]']
                cant = request.POST['data[cantidad]']
                if cuartos == 'cuarto':
                    cuartos = float(0.25)
                elif cuartos == 'medio':
                    cuartos = float(0.5)
                elif cuartos == 'unidad':
                    cuartos = 1
                cuenta = {}
                print('cantidad: ', cant)
                subtotal_fila = (float(precio) * int(cant)) * cuartos
                subtotal = "{0:.2f}".format(subtotal_fila)
                cuenta['cuenta_subtotal'] = subtotal
                var_total = float(self.calcula_total())
                total = "{0:.2f}".format(var_total)
                cuenta['total'] = total
                data = {'cuenta': cuenta}
            elif request.POST['action'] == 'accion_guardar':
                print(request.POST)
                mensaje = request.POST['mensaje']
                print('id_cliente:', id_cliente)
                date_joined = datetime.today().strftime('%Y-%m-%d')
                print('date_joined:', date_joined)
                iva = 0
                # envio de correo
                # data = self.enviar_email(id_cliente)
                cuenta_total = self.calcula_total()
                print('cuenta_total:', cuenta_total)
                with transaction.atomic():
                    venta = Venta()
                    venta.date_joined = date_joined
                    venta.cliente_id = id_cliente
                    venta.subtotal = float(cuenta_total)
                    venta.iva = float(iva)
                    venta.total = float(cuenta_total)
                    if venta.total >= 25:
                        venta.save()
                        for i in Cesta.objects.filter(id_cliente=id_cliente).filter(id_producto__activo=True):
                            diccionario_prod = i.toJSON()
                            print(diccionario_prod)
                            det = DetVenta()
                            det.venta_id = venta.id
                            det.mensaje = mensaje
                            det.prod_id = diccionario_prod['id_producto'].get('id')
                            det.cant = diccionario_prod['cant']
                            det.precio = float(diccionario_prod['id_producto'].get('pvp'))
                            total = self.calcula_subtotal(diccionario_prod)
                            det.subtotal = "{0:.2f}".format(total)
                            var_cuartos = diccionario_prod['cuartos']
                            if var_cuartos is None:
                                var_cuartos = ""
                            elif var_cuartos == '':
                                var_cuartos = ""
                            elif var_cuartos == 'cuarto':
                                var_cuartos = '1/4 K'
                            elif var_cuartos == 'medio':
                                var_cuartos = '1/2 K'
                            elif var_cuartos == 'unidad':
                                var_cuartos = '1 K'
                            det.cuartos = var_cuartos
                            print(det)
                            det.save()
                        Cesta.objects.filter(id_cliente=id_cliente).delete()
                        data = {'mensaje': 'correcto'}
                    else:
                        data = {'mensaje': 'error'}
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cesta de Compra'
        context['entidad'] = 'Cesta'
        cliente_id = self.request.user.id
        # halla el total de la cuenta
        total_var = self.calcula_total()
        if total_var is None:
            context['total'] = 0
        else:
            context['total'] = total_var
        # halla los datos del cliente
        nombre_lista = Cliente.objects.filter(usuario_ptr_id=cliente_id)
        data_cliente = []
        nombre = ''
        apellidos = ''
        direccion = ''
        poblacion = ''
        telefono = ''
        email = ''
        for i in nombre_lista:
            data_cliente.append(i.toJSON())
        for i in data_cliente:
            nombre = i['first_name']
            apellidos = i['last_name']
            direccion = i['direccion']
            poblacion = i['localidad']
            telefono = i['telefono']
            email = i['email']
        context['nombre'] = nombre
        context['apellidos'] = apellidos
        context['direccion'] = direccion
        context['poblacion'] = poblacion
        context['telefono'] = telefono
        context['email'] = email
        return context


class CestaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cesta
    template_name = 'cesta/eliminar.html'
    success_url = reverse_lazy('administrador:cesta_lista')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        id_cliente = request.user.id
        try:
            if action == 'elimina_id':
                Cesta.objects.filter(id_cliente=id_cliente).filter(id=request.POST['id']).delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lista_url'] = reverse_lazy('administrador:cesta_lista')
        return context


class CestaFacturaPdfView(View):

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
            template = get_template('cesta/factura.html')
            context = {
                'venta': Venta.objects.get(pk=self.kwargs['pk']),
                'comp': {
                    'nombre': 'Famisuper',
                    'direccion': 'Calle Manuel Gonzalez Rodriguez, 14 . Santiponce(Sevilla)',
                    'teléfono': '955997472',
                    'email': 'famisuper@outlook.com',
                    # 'icon': '{}{}'.format(settings.STATIC_URL, 'img/logo.png'),
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
        return HttpResponseRedirect(reverse_lazy('administrador:cesta_factura'))


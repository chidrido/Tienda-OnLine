import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from aplicaciones.administrador.forms import ImportarCSVForm
from aplicaciones.administrador.mixins import ValidatePermissionRequiredMixin
from aplicaciones.administrador.models import Importar, Venta, Producto, Categoria, SubCategoria


class ImportarCSVListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Importar
    template_name = 'importar_csv/lista.html'
    # permission_required = 'aplicaciones.view_categoria'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'busca_datos':
                data = []
                for i in Importar.objects.all():
                    data.append(i.toJSON())
            elif action == 'checkbox_importar':
                categoria = ''
                subcategoria = ''
                codigo = request.POST['codigo']
                nombre = request.POST['nombre']
                cat = request.POST['categoria']
                var_categoria = Categoria.objects.filter(nombre__icontains=cat).values('id')
                for i in var_categoria:
                    categoria = i['id']
                subcat = request.POST['subcategoria']
                var_subcategoria = SubCategoria.objects.filter(nombre__icontains=subcat).values('id')
                for i in var_subcategoria:
                    subcategoria = i['id']
                imagen = request.POST['imagen']
                pvp = request.POST['pvp']
                stock = request.POST['stock']
                with transaction.atomic():
                    prod = Producto()
                    prod.codigo = codigo
                    prod.nombre = nombre
                    prod.cat_id = categoria
                    prod.subcat_id = subcategoria
                    imagen = imagen.replace('/media/', "")
                    prod.imagen = imagen
                    prod.pvp = float(pvp)
                    prod.stock = stock
                    prod.save()
                Importar.objects.filter(codigo=codigo).delete()
            elif action == 'importar_csv':
                resultados = []
                with open('C:/Users/chidr/OneDrive/Desktop/famisuper/famisuper/aplicaciones/administrador/static/CSV/Archivo_csv.csv', newline='') as File:
                    lectura = csv.DictReader(File, delimiter=';')
                    for fila in lectura:
                        resultados.append(fila)
                        print(fila)
                    for i in resultados:
                        var_cod = i['Cod.Barras']
                        cod = var_cod.strip()
                        print(cod)
                        var_nombre = i['ArticulosWeb']
                        var_categoria = i['Categoria']
                        if var_categoria == 'Alimentacion':
                            var = Categoria.objects.filter(nombre__icontains='Alimentación').values('id')
                            for k in var:
                                var_categoria = k['id']
                        elif var_categoria == 'Bebida':
                            var = Categoria.objects.filter(nombre__icontains='Bebida').values('id')
                            for k in var:
                                var_categoria = k['id']
                        elif var_categoria == 'Congelados':
                            var = Categoria.objects.filter(nombre__icontains='Congelados').values('id')
                            for k in var:
                                var_categoria = k['id']
                        elif var_categoria == 'Camara':
                            var = Categoria.objects.filter(nombre__icontains='Congelados').values('id')
                            print('categoria_id:', var)
                            for k in var:
                                var_categoria = k['id']
                        elif var_categoria == 'Drogueria':
                            var = Categoria.objects.filter(nombre__icontains='Droguería').values('id')
                            for k in var:
                                var_categoria = k['id']
                        var_pvp = i['PVP']
                        var_stock = i['Stock']
                        comprueba = Producto.objects.filter(codigo=cod).exists()
                        if comprueba:
                            Producto.objects.filter(codigo=cod).update(pvp=var_pvp)
                        else:
                            with transaction.atomic():
                                prod = Importar()
                                prod.codigo = var_cod.strip()
                                print(prod.codigo)
                                prod.nombre = var_nombre
                                print(prod.nombre)
                                prod.imagen = 'imagenes/empty.png'
                                print(prod.imagen)
                                prod.cat_id = var_categoria
                                print(prod.cat_id)
                                prod.subcat_id = 1
                                print(prod.subcat_id)
                                prod.pvp = float(var_pvp)
                                print(prod.pvp)
                                prod.stock = var_stock
                                print(prod.stock)
                                prod.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # devuelve un diccionario
        context['titulo'] = 'Listado a Importar'
        context['entidad'] = 'Importar CSV'
        context['lista_url'] = reverse_lazy('administrador:importar_lista')
        context['crear_url'] = reverse_lazy('administrador:importar_lista')
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class ImportarCSVUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Importar
    form_class = ImportarCSVForm
    template_name = 'importar_csv/editar.html'
    success_url = reverse_lazy('administrador:importar_lista')
    # permission_required = 'aplicaciones.change_categoria'
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
        context['titulo'] = 'Editar Importación'
        context['entidad'] = 'Importar CSV'
        context['lista_url'] = self.success_url
        context['action'] = 'edit'
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context


class ImportarCSVDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Importar
    template_name = 'importar_csv/eliminar.html'
    success_url = reverse_lazy('administrador:importar_lista')
    # permission_required = 'aplicaciones.delete_categoria'
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
        context['titulo'] = 'Eliminar producto Importado'
        context['entidad'] = 'Importar CSV'
        context['lista_url'] = self.success_url
        context['pendientes'] = len(Venta.objects.filter(pedido_checkbox=True))
        return context

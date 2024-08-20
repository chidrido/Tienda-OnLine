from django.db import transaction
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from aplicaciones.administrador.models import Producto, Categoria, SubCategoria, Cesta, Favoritos, DetVenta
from datetime import datetime
from django.db.models import Sum, DecimalField


class SuperListView(ListView):
    template_name = 'super/lista.html'
    model = Producto

    def get_queryset(self):
        # devuelve los productos filtrados por categorías y subcategorías
        if 'pk' in self.kwargs:
            var = self.kwargs['pk']
            if var.isnumeric():
                return Producto.objects.filter(cat_id=var).filter(activo=True)
            elif not var.isnumeric():
                subcate_id = SubCategoria.objects.filter(nombre=var).values('id')
                var_subcat_id = ''
                for i in subcate_id:
                    var_subcat_id = i['id']
                return Producto.objects.filter(subcat_id=var_subcat_id).filter(activo=True)

        # esta parte se encarga del buscador
        query = self.request.GET.get('buscarProductoSuper')
        if query:
            object_list = self.model.objects.filter(nombre__icontains=query).filter(activo=True)
            return object_list
        else:
            object_list = self.model.objects.all()[0:12]
            return object_list

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
            subtotal_fila = (float(precio) * int(cant))*cuartos
            subtotal = round(subtotal_fila, 2)
            var_total += subtotal
            total = var_total
        return "{0:.2f}".format(total)

    # Calcula los productos más vendidos
    def ventas_productos(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for p in Producto.objects.all():
                total = DetVenta.objects.filter(venta__date_joined__year=year, venta__date_joined__month=month, prod__id=p.id).aggregate(
                    r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                if total > 0:
                    data.append({
                        'codigo': p.codigo,
                        'nombre': p.nombre,
                        'cat': p.cat.nombre,
                        'subcat': p.subcat.nombre,
                        'total': float(total)
                    })
        except:
            pass
        return data

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            id_cliente = request.user.id
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(nombre__contains=request.POST['term']).filter(activo=True):
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'mirar_producto':
                print(request.POST)
                if request.POST:
                    data = []
                    productos = Producto.objects.filter(id=request.POST.get('id'))  # obtiene el objeto producto
                    for i in productos:  # itera y guarda en la variable data
                        item = i.toJSON()
                        print(item)
                        data.append(item)
            elif action == 'busca_id':
                id_producto = request.POST['id']
                comprueba = Cesta.objects.filter(id_cliente=id_cliente).filter(id_producto=id_producto)
                if comprueba:  # si el producto existe
                    comprueba_cant = Cesta.objects.filter(id_cliente=id_cliente).filter(id_producto_id=id_producto).values('cant')
                    cant = 0
                    for i in comprueba_cant:
                        cant = i['cant']
                        cant += 1
                    Cesta.objects.filter(id_cliente=id_cliente).filter(id_producto=id_producto).update(cant=cant)
                else:
                    with transaction.atomic():
                        ces = Cesta()
                        ces.id_cliente = id_cliente
                        ces.id_producto_id = id_producto
                        ces.cuartos = ''
                        comp_cuarto = Producto.objects.filter(id=id_producto).filter(cuartos=True)
                        if comp_cuarto:
                            ces.cuartos = 'unidad'
                            ces.cuartos_checkbox = True
                        ces.cant = 1
                        ces.save()
            elif action == 'borra_prod':
                Cesta.objects.filter(id_cliente=self.request.user.id).filter(id=request.POST['id']).delete()
            elif action == 'añadir_favoritos':
                id_producto = request.POST['id']
                comprueba = Favoritos.objects.filter(id_cliente=id_cliente).filter(id_producto=id_producto)
                if not comprueba:
                    with transaction.atomic():
                        fav = Favoritos()
                        fav.id_producto_id = id_producto
                        fav.id_cliente_id = id_cliente
                        fav.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)  # con safe=False para serializarlo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'famisuper'
        context['categorias'] = Categoria.objects.all()
        context['subcategorias'] = SubCategoria.objects.all()
        context['ofertas'] = Producto.objects.filter(oferta_checkbox=True)[0:3]
        context['lista_favoritos'] = self.ventas_productos()
        # añade la cantidad total de productos
        cant_dic = Cesta.objects.filter(id_cliente=self.request.user.id).values('cant')
        cant = 0
        for i in cant_dic:
            cant = cant + i['cant']
        context['cantidad'] = cant
        # añade el total de cuenta, total del producto y los datos de los productos de la cesta en el modal barra
        client = self.request.user.id
        data = []
        for i in Cesta.objects.filter(id_cliente=client).filter(id_producto__activo=True):
            datos = {}
            diccionario = i.toJSON()
            datos['id'] = diccionario['id']
            datos['imagen'] = diccionario['id_producto'].get('imagen')
            datos['nombre'] = diccionario['id_producto'].get('nombre')
            datos['id_cliente'] = diccionario['id_cliente']
            datos['pvp'] = diccionario['id_producto'].get('pvp')
            datos['cant'] = diccionario['cant']
            datos['cuartos'] = diccionario['cuartos']
            cuartos = diccionario['cuartos']
            if cuartos is None:
                cuartos = int(1)
            elif cuartos == '':
                print('None')
                cuartos = int(1)
            elif cuartos == 'cuarto':
                cuartos = float(0.25)
            elif cuartos == 'medio':
                cuartos = float(0.50)
            elif cuartos == 'unidad':
                cuartos = int(1)
            precio = diccionario['id_producto'].get('pvp')
            cantidad = diccionario['cant']
            subtotal = (float(precio) * int(cantidad))*cuartos
            var_subtotal = "{0:.2f}".format(subtotal)
            datos['subtotal'] = var_subtotal
            data.append(datos)
        object_cesta = Cesta.objects.filter(id_cliente=self.request.user.id).filter(id_producto__activo=True)
        context['lista_cesta'] = zip(data, object_cesta)
        total = self.calcula_total()
        context['total'] = total

        # usa pk para filtrar las subcategorías de la categoría seleccionada
        if 'pk' in self.kwargs:
            var = self.kwargs['pk']
            if var.isnumeric():
                context['subcategorias'] = SubCategoria.objects.filter(cat_id=var)
            elif not var.isnumeric():
                subcate_id = SubCategoria.objects.filter(nombre=var).values('cat_id')
                var_subcat_id = ''
                for i in subcate_id:
                    var_subcat_id = i['cat_id']
                context['subcategorias'] = SubCategoria.objects.filter(cat_id=var_subcat_id)
        return context

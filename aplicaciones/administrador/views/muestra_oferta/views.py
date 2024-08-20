from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from aplicaciones.administrador.models import Categoria, Producto, Venta, DetVenta, Cesta
from aplicaciones.usuarios.models import Usuario


class MuestraOfertasListView(ListView):
    template_name = 'muestra_oferta/muestra_oferta.html'
    model = Producto

    def get(self, request, *args, **kwargs):
        context = {}
        context['alimentacion_cat'] = Producto.objects.filter(cat_id=1).filter(oferta_checkbox=True)
        context['bebidas_cat'] = Producto.objects.filter(cat_id=5).filter(oferta_checkbox=True)
        context['congelados_cat'] = Producto.objects.filter(cat_id=4).filter(oferta_checkbox=True)
        context['drogueria_cat'] = Producto.objects.filter(cat_id=3).filter(oferta_checkbox=True)
        context['fruteria_cat'] = Producto.objects.filter(cat_id=2).filter(oferta_checkbox=True)
        context['refrigerados_cat'] = Producto.objects.filter(cat_id=6).filter(oferta_checkbox=True)
        context['categorias'] = Categoria.objects.filter().exclude(id=2)
        context['todo_oferta'] = Producto.objects.filter(oferta_checkbox=True)[0:15]
        context['oferta_cat_titulo'] = 'Ofertas'
        context['oferta_slides_titulo'] = 'Super Ofertas de Frutas'
        return render(request, self.template_name, context)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.POST == 'POST':
                print(request.POST)
                if request.POST:
                    data = []
                    productos = Producto.objects.filter(id=request.POST.get('id'))  # obtiene el objeto producto
                    for i in productos:  # itera y guarda en la variable data
                        item = i.toJSON()
                        data.append(item)
                if Usuario.is_authenticated:
                    with transaction.atomic():
                        item_nombre = item['nombre']  # contiene el nombre del producto seleccionado
                        print(item_nombre)
                        ident_cli = request.user.id  # contiene el id del cliente
                        comprueba = Cesta.objects.filter(id_cliente=ident_cli).filter(
                            nombre=item_nombre)  # comprueba si el producto ya existe en la cesta
                        if comprueba:  # si el producto existe
                            comprueba_cant = Cesta.objects.filter(id_cliente=ident_cli).filter(
                                nombre=item_nombre).values('cant')  # obtiene la cantidad
                            cant = 0
                            for i in comprueba_cant:  # incremeta la cantidad
                                cant = i['cant']
                            cant += 1
                            Cesta.objects.filter(id_cliente=ident_cli).filter(nombre=item_nombre).update(cant=cant)
                        else:  # si el producto no existe en la cesta
                            ces = Cesta()
                            ident_cli = request.user.id
                            ces.id_cliente = ident_cli
                            ces.nombre = item['nombre']
                            ces.imagen = item['imagen']
                            ces.cant = 1
                            ces.precio = item['pvp']
                            ces.subtotal = item['pvp']
                            ces.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)  # con safe=False para serializarlo

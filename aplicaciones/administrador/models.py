from django.contrib.auth.models import User
from django.db import models
from django.forms import model_to_dict
from datetime import datetime
from aplicaciones.usuarios.models import Usuario
from configuracion.settings import MEDIA_URL, STATIC_URL


class Categoria(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)  # convierte los objetos json a tipo diccionario
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nombre']


class SubCategoria(models.Model):
    cat = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría')
    nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)  # convierte los objetos json a tipo diccionario
        return item

    class Meta:
        verbose_name = 'Subcategoria'
        verbose_name_plural = 'Subcategorias'
        ordering = ['nombre']


class Producto(models.Model):
    codigo = models.CharField(max_length=20, verbose_name='Codigo', unique=True)
    nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría')
    subcat = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, verbose_name='Subcategoría')
    imagen = models.ImageField(upload_to='productos_img/', verbose_name='Imagen')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    valoracion = models.IntegerField(default=0, null=True, blank=True, verbose_name='Valoración')
    oferta_checkbox = models.BooleanField(default=False, null=True, blank=True, verbose_name='ckeckoferta')     # asigna como oferta
    especial = models.BooleanField(default=False, null=True, blank=True, verbose_name='ckeckespecial')           # asigna sección especial(En este caso Ayala)
    cuartos = models.BooleanField(default=False, null=True, blank=True, verbose_name='checkcuartos')              #activa/desactiva el prodcuto
    activo = models.BooleanField(default=True, null=True, blank=True, verbose_name='ckeckactivar')              #activa/desactiva el prodcuto

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.cat.toJSON()
        item['subcat'] = self.subcat.toJSON()
        item['imagen'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Importar(models.Model):
    codigo = models.CharField(max_length=20, verbose_name='Codigo', unique=True)
    nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría')
    subcat = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Subcategoría')
    imagen = models.ImageField(upload_to='productos_img/', null=True, blank=True, verbose_name='Imagen')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    importar_checkbox = models.BooleanField(default=False, null=True, blank=True, verbose_name='ckeckimportar')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.cat.toJSON()
        item['subcat'] = self.subcat.toJSON()
        item['imagen'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'productos_img/empty.png')

    class Meta:
        verbose_name = 'Importar'
        verbose_name_plural = 'Importar'
        ordering = ['id']


class Cliente(Usuario):
    direccion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Dirección')
    localidad = models.CharField(max_length=100, null=True, blank=True, verbose_name='Población')
    telefono = models.IntegerField(unique=True, verbose_name='Telefono')

    def __str__(self):
        return self.first_name

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def toJSON(self):
        item = model_to_dict(self)
        item['imagen'] = self.get_imagen()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Cesta(models.Model):
    id_cliente = models.IntegerField(verbose_name='Cliente')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cant = models.IntegerField(default=0, verbose_name='Cantidad')
    cuartos = models.CharField(max_length=20, null=True, blank=True, verbose_name='Tipo Cuartos')
    cuartos_checkbox = models.BooleanField(default=False, null=True, blank=True, verbose_name='ckeckcuartos')

    def __str__(self):
        return self.id_producto

    def toJSON(self):
        item = model_to_dict(self)
        item['id_producto'] = self.id_producto.toJSON()
        return item

    def get_image(self):
        if self.imagen:
            return '{}'.format(self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Cesta'
        verbose_name_plural = 'Cesta'
        ordering = ['id']


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    pedido_checkbox = models.BooleanField(default=True, verbose_name='Check_Pedido')

    def __str__(self):
        return self.cliente.first_name

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detventa_set.all()]
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class DetVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    cuartos = models.CharField(max_length=20, null=True, blank=True, verbose_name='Tipo Cuartos')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    mensaje = models.CharField(max_length=200, null=True, blank=True, verbose_name='Mensaje')

    def __str__(self):
        return self.prod.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['venta'])
        item['prod'] = self.prod.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de venta'
        ordering = ['id']


class Favoritos(models.Model):
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')

    def __str__(self):
        return self.id_producto

    def toJSON(self):
        item = model_to_dict(self)
        item['id_producto'] = self.id_producto.toJSON()
        return item

    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        ordering = ['id']





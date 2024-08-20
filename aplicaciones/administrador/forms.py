from django.forms import *
from datetime import datetime
from aplicaciones.administrador.models import Categoria, Producto, Cliente, Venta, SubCategoria, Cesta, Importar


class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SubCategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = SubCategoria
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Producto
        fields = 'codigo', 'nombre', 'cat', 'subcat', 'pvp', 'stock', 'imagen', 'desc'
        widgets = {
            'codigo': TextInput(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'nombre': TextInput(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'desc': Textarea(
                attrs={
                    'class': 'select2',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }
        exclude = ['valoracion', 'select_cat']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ImportarCSVForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Importar
        fields = 'codigo', 'nombre', 'cat', 'subcat', 'imagen', 'pvp', 'stock', 'desc'

        widgets = {
            'codigo': TextInput(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'nombre': TextInput(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'desc': Textarea(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }
        exclude = ['valoracion']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class GestionaForm(Form):
    categorias = ModelChoiceField(queryset=Categoria.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 80%'
    }))

    subcategorias = ModelChoiceField(queryset=SubCategoria.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 80%'
    }))


class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cliente
        fields = 'first_name', 'last_name', 'direccion', 'localidad', 'telefono', 'email', 'username', 'password'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese su nombre',
                    'autocomplete': 'off',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                    'autocomplete': 'off',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                    'autocomplete': 'off',
                }
            ),
            'localidad': TextInput(
                attrs={
                    'placeholder': 'Ingrese su Localidad',
                    'autocomplete': 'off',
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese su teléfono',
                    'autocomplete': 'off',
                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                    'autocomplete': 'off',
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre de usuario',
                    'autocomplete': 'off',
                }
            ),
            'password': PasswordInput(render_value=True,
                                      attrs={
                                          'placeholder': 'Ingrese una contraseña',
                                          'autocomplete': 'off',
                                      }
                                      ),
        }
        exclude = ['imagen']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TestForm(Form):
    categorias = ModelChoiceField(queryset=Categoria.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    productos = ModelChoiceField(queryset=Producto.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    search = ModelChoiceField(queryset=Producto.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))


class VentaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Venta
        fields = '__all__'
        widgets = {
            'cliente': Select(attrs={
                'class': 'form-select select2',
                # 'style': 'width: 100%'
            }),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'productos': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'

            }),
            'cantidad': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }


class CestaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Cesta
        fields = '__all__'
        widgets = {
            'productos': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'

            }),
            'cantidad': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),

        }


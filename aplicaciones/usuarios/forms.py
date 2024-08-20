from django.forms import ModelForm, TextInput, PasswordInput, SelectMultiple

from aplicaciones.administrador.models import Cliente
from aplicaciones.usuarios.models import Usuario


class UsuarioForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Usuario
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'imagen', 'groups'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Introduce un nombre',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Introduce los apellidos',
                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese el email',
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Introduce un nombre de usuario',
                }
            ),
            'password': PasswordInput(render_value=True,
                attrs={
                    'placeholder': 'Ingrese una contraseña',
                }
            ),
            'groups': SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            })
        }
        exclude = ['user_permissions', 'last-login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                us = form.save(commit=False)
                if us.pk is None:
                    us.set_password(pwd)
                else:
                    usuario = Usuario.objects.get(pk=us.pk)
                    if usuario.password != pwd:
                        us.set_password(pwd)
                us.save()
                us.groups.clear()
                for g in self.cleaned_data['groups']:
                    us.groups.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UsuarioPerfil(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cliente
        fields = 'first_name', 'last_name', 'direccion', 'telefono', 'email', 'username', 'password'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Introduce un nombre',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Introduce los apellidos',
                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese el email',
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Introduce un nombre de usuario',
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Introduce un nombre de usuario',
                }
            ),
            'password': PasswordInput(render_value=True,
                attrs={

                }
            )
        }
        exclude = ['user_permissions', 'last-login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'groups']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                us = form.save(commit=False)
                if us.pk is None:
                    us.set_password(pwd)
                else:
                    usuario = Usuario.objects.get(pk=us.pk)
                    if usuario.password != pwd:
                        us.set_password(pwd)
                us.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

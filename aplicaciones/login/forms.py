from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput
from aplicaciones.administrador.models import Cliente
from aplicaciones.usuarios.models import Usuario


class ReseteoPassWordForm(forms.Form):

    email = forms.CharField(widget=TextInput(attrs={
        'placeholder': 'Introduzca su email',
        'class': 'form.control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        if not Cliente.objects.filter(email=cleaned['email']).exists():
            self._errors['error'] = self._errors.get('error ', self.error_class())
            self._errors['error'].append(' El correo electrónico no existe')
            # raise forms.ValidationError('El correo no existe')
        return cleaned

    def get_cliente(self):
        email = self.cleaned_data.get('email')
        return Usuario.objects.get(email=email)


class CambiarPassWordForm(forms.Form):
    password = forms.CharField(widget=PasswordInput(attrs={
        'placeholder': 'Introduzca su nueva contraseña',
        'class': 'form.control',
        'autocomplete': 'off'
    }))

    confirmarPassword = forms.CharField(widget=PasswordInput(attrs={
        'placeholder': 'Repita la contraseña',
        'class': 'form.control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmarPassword = cleaned['confirmarPassword']
        if password != confirmarPassword:
            self._errors['error'] = self._errors.get('error ', self.error_class())
            self._errors['error'].append('Las contraseñas deben ser iguales')
            # raise forms.ValidationError('Las contraseñas deben ser iguales')
        return cleaned



from django.forms import *


class ReporteForm(Form):

    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control select2',
        'autocomplete': 'off'
    }))

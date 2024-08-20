from django.contrib.auth.views import LogoutView
from django.urls import path

from aplicaciones.login.views import *

app_name = 'perfil'

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset/password/', ReseteoPassWordView.as_view(), name='reset_contraseña'),
    path('change/password/<str:token>/', CambiarPassWordView.as_view(), name='change_contraseña')
    # path('logout/', LogoutRedirectView.as_view(), name='logout')
]

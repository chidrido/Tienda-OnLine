from crum import get_current_request
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _

from configuracion.settings import STATIC_URL, MEDIA_URL


class Usuario(AbstractUser):
    imagen = models.ImageField(upload_to='usuarios_img/', null=True, blank=True, verbose_name='Imagen')
    email = models.EmailField(_('email address'), unique=True)
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)

    def get_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['user_permissions', 'last-login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['imagen'] = self.get_imagen()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass

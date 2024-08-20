import smtplib
from configuracion.wsgi import *
from django.template.loader import render_to_string
from aplicaciones.usuarios.models import Usuario
from configuracion import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviar_email():
    try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print('Conectado...')

        email_to = 'chidrido@hotmail.com'

        # Construimos el mensaje simple
        mensaje = MIMEMultipart()
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = email_to
        mensaje['Subject'] = 'Tienes un correo'

        context = render_to_string('enviar_email.html', {'user': Usuario.objects.get(pk=1)})
        mensaje.attach(MIMEText( context, 'html'))

        mailServer.sendmail(settings.EMAIL_HOST_USER,
                            email_to,
                            mensaje.as_string())

        print('Correo enviado correctamente')
    except Exception as e:
        print(e)


enviar_email()

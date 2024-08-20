# import os.path
# from configuracion.wsgi import *
# from django.template.loader import get_template
# from weasyprint import HTML, CSS
# from configuracion import settings
#
#
# def imprimeTicket():
#     template = get_template("cesta/ticket.html")
#     context = {"nombre": "Coco coco coco"}
#     html_template = template.render(context)
#     css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
#     HTML(string=html_template).write_pdf(target="ticket.pdf", stylesheets=[CSS(css_url)])
#
#
# imprimeTicket()

import urllib
import StringIO
from qrcode import *
from django import template
from django.http import HttpResponse
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
@stringfilter

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def qr(request,part_id):
    qr = QRCode(3, QRErrorCorrectLevel.L)
    qr.addData("https://z.gigafreak.net/admin/pmdb/part/%s/" % part_id)
    qr.make()

    im = qr.makeImage()
    buffer = StringIO.StringIO()
    im.save(buffer,'PNG')
    return HttpResponse(buffer.getvalue(), mimetype="image/png")

def admin(request,part_id):
    redirect('/admin/pmdb/parts/%s/' % part_id)    

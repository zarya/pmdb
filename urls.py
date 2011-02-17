from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^/$',
        'pmdb.views.index'),
    (r'^part/$', 
        'pmdb.views.index'),
    (r'^part/(?P<part_id>\d+)/qr/$', 
        'pmdb.views.qr'),
    (r'^part/(?P<part_id>\d+)/admin/$',
        'pmdb.views.admin'),
    (r'^admin/(.*)',
        admin.site.root),
)

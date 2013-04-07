from django.conf.urls import patterns, include, url
from frontend.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'photoplus.views.home', name='home'),
    # Examples:
    url(r'^about/feedback/', contact),
    url(r'^captcha/', include('captcha.urls')),
    
    url(r'^about/$', about),
    url(r'^albums/$', albums),

    url(r'^$',home),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
)



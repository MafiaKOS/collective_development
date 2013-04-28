from django.conf.urls import patterns, include, url
from frontend.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'photoplus.views.home', name='home'),
    # Examples:
    url(r'^$',home),
    url(r'^page/$',home),
    url(r'^page/(?P<page>\d+)/$',home_page),
    
    url(r'^preview/(?P<idP>\d+)/$', preview),
    url(r'^buy/(?P<idP>\d+)/(?P<resolution>\w+)/$', buy),
    
    url(r'^about/feedback/', contact),
    #url(r'^about/buy/', buy),

    url(r'^captcha/', include('captcha.urls')),
    
    url(r'^about/$', about),
    
    url(r'^albums/(?P<idA>\w+)/$', album),
    url(r'^albums/(?P<idA>\w+)/(?P<page>\d+)/$', album),


    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
)



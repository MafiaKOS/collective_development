from django.conf.urls import patterns, include, url
from frontend.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'photoplus.views.home', name='home'),
    url(r'^about/feedback/', contact),
    url(r'^about/$', about),
    url(r'^albums/$', albums),
	url(r'^photo/(\d+)/$', photo),
	url(r'^buy/(?P<id_get>\d+)/(?P<resolution>\w+)/$', buy),
    url(r'^search-form/$', search_form),
   
    url(r'^$',home),
	url(r'^page/$',home),
	url(r'^page/(?P<page>\d+)/$',home_page),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
)

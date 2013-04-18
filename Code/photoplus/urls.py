


from django.conf.urls   import patterns, include, url
from frontend.views     import *
from django.contrib     import admin

admin.autodiscover()

urlpatterns = patterns('',

#                       FRONTEND URLS
#----------------------------------------------------------
    url(r'^$',home),
    url(r'^page/$',home),
    url(r'^page/(?P<page>\d+)/$',home_page),
    
    url(r'^preview/(?P<idP>\d+)/$', preview),
    url(r'^buy/(?P<idP>\d+)/(?P<resolution>\w+)/$', buy),

    url(r'^about/$', about),
    url(r'^about/feedback/$', feedback), 

    url(r'^albums/(?P<idA>\w+)/$', album),
    url(r'^albums/(?P<idA>\w+)/(?P<page>\d+)/$', album),



#                       ADMIN URLS
#----------------------------------------------------------
    url(r'^admin_tools/', include('admin_tools.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

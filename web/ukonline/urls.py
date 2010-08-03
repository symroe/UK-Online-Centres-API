from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    # Example:
    # (r'^web/', include('web.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', views.centres, name="centres"),
    url(r'^(?P<pk>[\d]+)/(?P<slug>.*)/', views.centre, name="centre"),
)

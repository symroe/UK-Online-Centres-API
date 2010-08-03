from django.conf.urls.defaults import *
from piston.resource import Resource
from web.api.handlers import *
import emitters

all_centres_handler = Resource(AllCentres)
centre_handler = Resource(CentreHandler)
nearest_handler = Resource(NearestCentres)

urlpatterns = patterns('',
    
    url(r'^nearest/(?P<lat>[^/]+)/(?P<lng>[^/]+)/', nearest_handler),
    url(r'^centre/(?P<pk>[^/]+)/', centre_handler),
    url(r'^$', all_centres_handler),
    
    # url(r'^v1/search/(?P<term>[^/]+)/', search_handler),

)




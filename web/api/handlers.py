from piston.handler import BaseHandler

from django.contrib.gis.geos import Point

from ukonline.models import *

class AllCentres(BaseHandler):
    allowed_methods = ('GET',)
    model = Centre

    def read(self, request):
        all_centres = Centre.objects.all().kml()
        
        centres_dict = {}
        
        for centre in all_centres:
            centres_dict[centre.pk] = centre.__dict__
            centres_dict[centre.pk]['kml_str'] = centre.kml
        res =  centres_dict
        return res


class CentreHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Centre

    def read(self, request, pk):
        centre = Centre.objects.kml().get(pk=pk)
        centre.__dict__['kml_str'] = centre.kml
        print centre.__dict__
    
        res =  centre.__dict__
        return [res]

class NearestCentres(BaseHandler):
    allowed_methods = ('GET',)
    model = Centre
    
    def read(self, request, lat, lng):
        area = Point(map(float, (lat, lng)))
        centres_dict = {}        
        for centre in Centre.objects.distance(area).kml().order_by('distance')[:10]:
            centres_dict[centre.pk] = centre.__dict__
            centres_dict[centre.pk]['kml_str'] = centre.kml
        res =  centres_dict
        return res

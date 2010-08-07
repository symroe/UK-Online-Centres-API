import json
import urllib

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
        del centres_dict[centre.pk]['_state']
        del centres_dict[centre.pk]['kml']
    
        res =  centre.__dict__
        return [res]

class NearestCentres(BaseHandler):
    allowed_methods = ('GET',)
    model = Centre
    
    def read(self, request, lat, lng):
        area = Point(map(float, (lat, lng)))
        centers_list = []
        for centre in Centre.objects.distance(area).kml().order_by('distance')[:10]:
            centre_dict = centre.__dict__
            del centre_dict['_state']
            centre_dict['kml_str'] = centre.kml
            centers_list.append(centre_dict)
        res =  centers_list
        return res

class NearestCentresByPostCode(BaseHandler):
    allowed_methods = ('GET',)
    model = Centre
    
    def read(self, request, postcode):
        print postcode
        mapit_url =  "http://mapit.mysociety.org/postcode/%s" % postcode
        mapit = json.load(urllib.urlopen(mapit_url))
        area = Point(map(float, (mapit['wgs84_lon'], mapit['wgs84_lat'])), 0)
        
        centers_list = []
        for centre in Centre.objects.distance(area).kml().order_by('distance')[:10]:
            centre_dict = centre.__dict__
            del centre_dict['_state']
            centre_dict['kml_str'] = centre.kml
            centers_list.append(centre_dict)
        res =  centers_list
        return res

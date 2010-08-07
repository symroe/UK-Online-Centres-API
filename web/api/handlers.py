import json
import urllib
import re

from piston.handler import BaseHandler
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import Point

from ukonline.models import *

POSTAL_ZONES = ('AB', 'AL', 'B' , 'BA', 'BB', 'BD', 'BH', 'BL', 'BN', 'BR',
                'BS', 'BT', 'CA', 'CB', 'CF', 'CH', 'CM', 'CO', 'CR', 'CT',
                'CV', 'CW', 'DA', 'DD', 'DE', 'DG', 'DH', 'DL', 'DN', 'DT',
                'DY', 'E[0-9]' , 'EC', 'EH', 'EN', 'EX', 'FK', 'FY', 'G' , 'GL',
                'GY', 'GU', 'HA', 'HD', 'HG', 'HP', 'HR', 'HS', 'HU', 'HX',
                'IG', 'IM', 'IP', 'IV', 'JE', 'KA', 'KT', 'KW', 'KY', 'L[0-9]' ,
                'LA', 'LD', 'LE', 'LL', 'LN', 'LS', 'LU', 'M' , 'ME', 'MK',
                'ML', 'N[0-9]' , 'NE', 'NG', 'NN', 'NP', 'NR', 'NW', 'OL', 'OX',
                'PA', 'PE', 'PH', 'PL', 'PO', 'PR', 'RG', 'RH', 'RM', 'S[0-9]' ,
                'SA', 'SE', 'SG', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SR',
                'SS', 'ST', 'SW', 'SY', 'TA', 'TD', 'TF', 'TN', 'TQ', 'TR',
                'TS', 'TW', 'UB', 'W[0-9]' , 'WA', 'WC', 'WD', 'WF', 'WN', 'WR',
                'WS', 'WV', 'YO', 'ZE')



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


class Nearest(BaseHandler):
    allowed_methods = ('GET', 'POST')
    model = Centre


    def read(self, request, text):
        lookup = text.upper()
        if lookup.startswith('UKONLINE'):
            lookup = lookup[8:].strip()
        
        print lookup
        centres = None
        
        if re.match("|".join(POSTAL_ZONES), lookup):
            try:
                # postcode lookup
                mapit_url =  "http://mapit.mysociety.org/postcode/partial/%s" % lookup
                mapit = json.load(urllib.urlopen(mapit_url))
                area = Point(map(float, (mapit['wgs84_lon'], mapit['wgs84_lat'])), 0)
                centres = Centre.objects.distance(area).kml().order_by('distance')[:10]
            except:
                pass
        if not centres:
            kwargs = {
                'town__icontains' : lookup,
                # 'county__search' : lookup,
            }
            centres = Centre.objects.filter(town__icontains=lookup) | Centre.objects.filter(county__icontains=lookup)
            centres = centres.kml()[:10]
        
        centers_list = []
        for centre in centres:
            centre_dict = centre.__dict__
            del centre_dict['_state']
            centre_dict['kml_str'] = centre.kml
            centers_list.append(centre_dict)
        res =  centers_list
        return res

    def create(self, request):
        return self.read(request, request.POST['text'])

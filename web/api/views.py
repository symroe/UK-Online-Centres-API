import re
import json
import urllib
from django.contrib.gis.geos import Point

from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string

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


def sms(request, lookup):
    lookup = lookup.upper()
    if lookup.startswith('UKONLINE'):
        lookup = lookup[8:].strip()
    
    centres = None
    
    if re.match("|".join(POSTAL_ZONES), lookup):
        try:
            # postcode lookup
            mapit_url =  "http://mapit.mysociety.org/postcode/partial/%s" % lookup
            mapit = json.load(urllib.urlopen(mapit_url))
            area = Point(map(float, (mapit['wgs84_lon'], mapit['wgs84_lat'])), 0)
            centres = Centre.objects.distance(area).kml().order_by('distance')
        except Exception, e:
            print e
            pass
    if not centres:
        centres = Centre.objects.filter(town__icontains=lookup) | Centre.objects.filter(county__icontains=lookup)
        centres = centres.kml()
    print centres
    centers_list = []
    for centre in centres:
        centre_dict = centre.__dict__
        del centre_dict['_state']
        centre_dict['kml_str'] = centre.kml
        centers_list.append(centre_dict)
    res =  centers_list

    try:
        return HttpResponse(res[0]['sms'])
    except Exception, e:
        print e
        return HttpResponse("Sorry, nothing found")

# Scraper code here
from django.core.management.base import BaseCommand, CommandError

import urllib2
import re
import json

from django.contrib.gis.geos import Point

from ukonline import models

class Command(BaseCommand):
    
    def handle(self, **options):
        # Do a few different searches, as we only get results within a specific
        # distance (I don't know what that is)
        searches = (
            'edinbrough', 
            'london', 
            'norwich', 
            'cardiff', 
            'exiter', 
            'burmingham',
            )
        for search in searches:
            start = 0
            more_centres = True
            while more_centres:
                print search, start
                page = urllib2.urlopen(
                    "http://www.ukonlinecentres.com/centresearch/?q=%s&start=%s" % (search, start)).read()
        
                x = re.search("var centres ([^;]+)", page)
                try:
                    for centre in json.loads(x.group(0)[14:]): 
                        centre_object = None
                        print centre.get('name'), centre.get('client_id')
                        try:
                            centre_object = models.centre.objects.get(
                                client_id=centre.get('client_id'),
                                )
                            print "Existing object"
                        except models.centre.DoesNotExist, e:
                            print "New object", e
                            centre_object = models.centre()

                            centre_object = models.centre()
                            centre_object.name = centre.get('name')
                            centre_object.website = centre.get('url')
                            centre_object.fax = centre.get('fax')
                            centre_object.phone = centre.get('telephone')
                            centre_object.email = centre.get('email')
                            centre_object.addr2 = centre.get('addr2')
                            centre_object.client_id = centre.get('client_id')
                            centre_object.county = centre.get('county')
                            centre_object.isgold = centre.get('isgold')
                            centre_object.lat = centre.get('Latitude')
                            centre_object.lng = centre.get('Longitude')
                            centre_object.pc = centre.get('pc')
                            centre_object.street = centre.get('street')
                            centre_object.town = centre.get('town')
                            centre_object.location = Point(map(float, (centre.get('Longitude'), centre.get('Latitude'))))
                            centre_object.save()
                    start = start + 1
                
                except Exception, e:
                    print e
                    more_centres = False
# Scraper code here
from django.core.management.base import BaseCommand, CommandError

import urllib2
import re
import json
import csv

from django.contrib.gis.geos import Point

from ukonline import models

class Command(BaseCommand):
    
    def handle(self, **options):
        # Centres
        all_centres = csv.DictReader(open('ukonline/fixtures/centre.csv'))
        for centre in all_centres:
            try:
                C = models.Centre.objects.get(pk=centre['client_id'])
            except:
                C = models.Centre()
            C.__dict__.update(centre)
            if centre.get('longitude') and centre.get('latitude'):
                C.location = Point(map(float, (centre.get('longitude'), centre.get('latitude'))))
            C.save()
        
        # JulyData (don't ask)
        all_july_data = csv.DictReader(open('ukonline/fixtures/july_data.csv', 'rU'))
        print all_july_data
        for july in all_july_data:
            try:
                C = models.Centre.objects.get(pk=july['centre_id'])
                try:
                    J = models.JulyData.objects.get(pk=C)
                except:
                    J = models.JulyData(pk=C)
                J.__dict__.update(july)
                J.save()

            except Exception, e:
                pass
                # print e
                # print july['centre_id']
                # print "No centre"
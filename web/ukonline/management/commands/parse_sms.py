# Scraper code here
from django.core.management.base import BaseCommand, CommandError

import urllib2
import re
import json
import csv

from ukonline import models

class Command(BaseCommand):
    
    def handle(self, **options):
        all_sms = csv.DictReader(open('ukonline/fixtures/sms.csv'))
        for sms in all_sms:
            print sms
            try:
                C = models.Centre.objects.get(pk=sms['client_id'])
                C.sms = sms['text']
                C.save()
            except:
                raise

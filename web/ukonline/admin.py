from django.contrib.gis import admin as geo_admin
from models import *

class CentreAdmin(geo_admin.GeoModelAdmin):    
    search_fields = ['name',]


geo_admin.site.register(Centre, CentreAdmin)
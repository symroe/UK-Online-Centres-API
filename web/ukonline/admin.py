from django.contrib.gis import admin as geo_admin
from models import *

class CentreAdmin(geo_admin.GeoModelAdmin):    
    search_fields = ['town', 'county']
    list_display = ['client_id', 'name', 'targetaudience', 'town',]
    list_filter = ['targetaudience',]


geo_admin.site.register(Centre, CentreAdmin)
geo_admin.site.register(JulyData)
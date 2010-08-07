from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.gis.db import models as geo_models
from django.template.defaultfilters import slugify

class Centre(geo_models.Model):

    client_id = models.IntegerField(blank=True, null=True, unique=True, primary_key=True)
    name = models.CharField(blank=True, max_length=800)
    website = models.URLField(blank=True, verify_exists=False, null=True)
    fax = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    addr2 = models.TextField(blank=True, null=True)
    county = models.TextField(blank=True, null=True)
    isgold = models.BooleanField(default=False)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    pc = models.CharField(blank=True, max_length=14, null=True)
    street = models.TextField(blank=True, null=True)
    town = models.TextField(blank=True, null=True)
    location = geo_models.PointField(null=True, blank=True)
    regionid = models.TextField(blank=True, null=True)
    membershipstatus = models.TextField(blank=True, null=True)
    sectortype = models.TextField(blank=True, null=True)
    centretype = models.TextField(blank=True, null=True)
    targetaudience = models.TextField(blank=True, null=True)
    mondayopenfrom = models.TextField(blank=True, null=True)
    mondayopento = models.TextField(blank=True, null=True)
    tuesdayopenfrom = models.TextField(blank=True, null=True)
    tuesdayopento = models.TextField(blank=True, null=True)
    wednesdayopenfrom = models.TextField(blank=True, null=True)
    wednesdayopento = models.TextField(blank=True, null=True)
    thursdayopenfrom = models.TextField(blank=True, null=True)
    thursdayopento = models.TextField(blank=True, null=True)
    fridayopenfrom = models.TextField(blank=True, null=True)
    fridayopento = models.TextField(blank=True, null=True)
    saturdayopenfrom = models.TextField(blank=True, null=True)
    satudayopento = models.TextField(blank=True, null=True)
    sundayopenfrom = models.TextField(blank=True, null=True)
    sundayopento = models.TextField(blank=True, null=True)
    genopenhourcomments = models.TextField(blank=True, null=True)
    accessfacilitiesdesc = models.TextField(blank=True, null=True)
    crechefacilities = models.TextField(blank=True, null=True)
    crechefacilitiesdesc = models.TextField(blank=True, null=True)
    cafecateringfacilities = models.TextField(blank=True, null=True)
    cateringdesc = models.TextField(blank=True, null=True)
    parkingfacilities = models.TextField(blank=True, null=True)
    parkingfacilitiesdesc = models.TextField(blank=True, null=True)
    desconfcentrelocation = models.TextField(blank=True, null=True)
    charges = models.TextField(blank=True, null=True)
    penportrait = models.TextField(blank=True, null=True)
    numworkstations = models.TextField(blank=True, null=True)

    objects = geo_models.GeoManager()
    
    
    def __unicode__(self):
        return self.name
    
    # @models.permalink
    def get_absolute_url(self):
        print 'assd'
        print slugify(self.name)
        print reverse('centre', kwargs={ 'pk' : self.pk, 'slug' : slugify(self.name) })
        return reverse('centre', kwargs={ 'pk': self.pk, 'slug' : slugify(self.name) })

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
    lat = models.FloatField()
    lng = models.FloatField()
    pc = models.CharField(blank=True, max_length=14, null=True)
    street = models.TextField(blank=True, null=True)
    town = models.TextField(blank=True, null=True)
    location = geo_models.PointField(null=True, blank=True)

    objects = geo_models.GeoManager()
    
    
    def __unicode__(self):
        return self.name
    
    # @models.permalink
    def get_absolute_url(self):
        print 'assd'
        print slugify(self.name)
        print reverse('centre', kwargs={ 'pk' : self.pk, 'slug' : slugify(self.name) })
        return reverse('centre', kwargs={ 'pk': self.pk, 'slug' : slugify(self.name) })

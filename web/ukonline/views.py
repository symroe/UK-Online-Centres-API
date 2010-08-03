from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core import serializers

from models import Centre

def centres(request):
    """
    All centres
    """
    all_centres = Centre.objects.all()
    print all_centres[0].get_absolute_url()
    return render_to_response("centres.html",
                              {'centres': all_centres, })
    

def centre(request, pk, slug):
    """
    Single centre
    """
    
    c = get_object_or_404(Centre, pk=pk)
    field_names = c._meta.get_all_field_names()
    field_values = [getattr(c, n) for n in field_names]
    c_fields = dict(zip(field_names, field_values))
    
    return render_to_response(
        "centre.html",
        {
            'centre': c, 
            'centre_fields': c_fields, 
        })
    
    
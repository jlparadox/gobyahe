from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.staticfiles import *
from .models import Category, Itinerary
from .forms import ItineraryForm
from helpers.helper_functions import to_select, map_to_key, instance_dict

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    category_list = Category.objects.all().order_by('name')
    itinerary_list = Itinerary.objects.all().order_by('-pub_date')[:5]
    context_dict = {'categories': category_list, 'itinerary_list': itinerary_list}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'xplor/index.html', context_dict)

def itinerary_add(request):
    if request.method == 'POST':
        form = ItineraryForm(request.POST)

        if form.is_valid():
            k = form.save()

            data = instance_dict(k)
            data['method'] = 'add'

            dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
            return HttpResponse(json.dumps(data, default=dthandler), mimetype="application/json")
    else:
        form = ItineraryForm()

    return render(request, 'itinerary/add.html', {'form': form})

def register_success(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    return render(request, 'xplor/success.html')
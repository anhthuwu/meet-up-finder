from .models import Event, Location
from django.contrib.auth.models import User
from .forms import PostForm
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt, csrf_protect  # Add this
from django.core import serializers

from dotenv import load_dotenv
from json import dumps, loads
import os
import requests
load_dotenv()
result = []


def index(request):
    context = {}
    return render_index(request, context)


def list_requested(request):
    if request.method == "POST":
        id = request.POST.get('q')
        object_list = Event.objects.filter(id=id)
        location_info = object_list
        printAll = False
    else:
        location_info = Event.objects.all()
        printAll = True
    context = {"object_list": location_info, "printAll": printAll}
    return render_index(request, context, location_info)


def list_myevent(request):
    ev = Event.objects.filter(addedTOMyEvent=True)
    context = {"object_list": ev, "printAll": False}
    return render_index(request, context)


def post_clicked(request):
    form = PostForm(request.POST)
    postForm_enabled = True
    sucessfully_posted = False
    invalid_location_toast = ""
    # if no data is entered yet, the form is clean (as opposed to displaying validation error messages)
    if not form.data:
        form = PostForm()
    elif form.is_valid():
        try:
            APIKEY = ""
            if os.getenv("APIKEY"):
                APIKEY = os.getenv("APIKEY")
            result = find_place(form.cleaned_data['location'], APIKEY)[0]
            location = result["name"] + "\n" + result["formatted_address"]
            e = Event(name=form.cleaned_data['name'], location=location,
                      date=form.cleaned_data['date'], time=form.cleaned_data['time'],
                      host=form.cleaned_data['host'], rating=form.cleaned_data['rating'],
                      description=form.cleaned_data['description'],
                      lng=result["geometry"]["location"]["lng"],
                      lat=result["geometry"]["location"]["lat"])
            e.save()
            postForm_enabled = False
            sucessfully_posted = True
        except:
            invalid_location_toast = "The location is not valid. Please check again!!"
            postForm_enabled = True
            sucessfully_posted = False
    context = {"postForm_enabled": postForm_enabled, 'form': form,
               'sucessfully_posted': sucessfully_posted, "invalid_location_toast": invalid_location_toast}
    return render_index(request, context)


def list_clicked(request):
    context = {"object_list_all": Event.objects.all(), "all": True}
    location_info = Event.objects.all()
    return render_index(request, context, location_info)


def find_place(location, APIKEY):
    location = location.replace(" ", "%20")
    url = """https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key={}""".format(
        location, APIKEY)
    response = requests.get(url)
    response = loads(response.text)
    if response['status'] != "OK":
        return []

    north = 38.096569
    south = 37.992552
    west = -78.561004
    east = -78.428636
    candidates = response['candidates']
    new_candidates = []
    for c in candidates:
        if south <= c['geometry']['location']['lat'] <= north \
                and west <= c['geometry']['location']['lng'] <= east:
            new_candidates.append(c)
    if new_candidates:
        return new_candidates
    else:
        return []

import math
def find_events(lat, lng, dis):
    result = []
    for ev in Event.objects.all():
        R = 6371000 # metres
        φ1 = lat * math.pi/180 # φ, λ in radians
        φ2 = ev.lat * math.pi/180
        Δφ = (ev.lat-lat) * math.pi/180
        Δλ = (ev.lng-lng) * math.pi/180

        a = math.sin(Δφ/2) * math.sin(Δφ/2) + \
                math.cos(φ1) * math.cos(φ2) * \
                math.sin(Δλ/2) * math.sin(Δλ/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        d = R * c # in metres
        print(d, dis)
        if d < dis:
            result.append(ev)
    return result


@csrf_exempt
def addToEvent(request):
    id = loads(request.body.decode('utf-8'))['event_id']
    ev = Event.objects.filter(Q(id__contains=id)).get()
    if ev.addedTOMyEvent:
        ev.addedTOMyEvent = False
    else:
        ev.addedTOMyEvent = True

    ev.save()
    return render_index(request, {})


@csrf_exempt
def find_near_me(request):
    context = {"nearme": True}
    APIKEY = ""
    try:
        search_input_place = loads(
            request.body.decode('utf-8'))['search_input_place']
        if os.getenv("APIKEY"):
            APIKEY = os.getenv("APIKEY")
        search_result = find_place(search_input_place, APIKEY)
        u = User.objects.get(username=request.user)
        l = Location.objects.get(user=u)
        l.location = search_result[0]["name"] + \
            "\n" + search_result[0]["formatted_address"]
        l.lng = search_result[0]["geometry"]["location"]["lng"]
        l.lat = search_result[0]["geometry"]["location"]["lat"]
        l.save()
    except:
        pass
    try:
        u = User.objects.get(username=request.user)
        l = Location.objects.get(user=u)
        search_input_distance = loads(
            request.body.decode('utf-8'))['search_input_distance']
        l.distance = search_input_distance
        l.save()
    except e:
        print(e)
    finally:
        u = User.objects.get(username=request.user)
        l = Location.objects.get(user=u)
        result = find_events(l.lat, l.lng, l.distance)
        location_info = result + [l]
        context["object_list"] = result
        context["printAll"] = False
        context["default_distance"] = l.distance
        return render_index(request, context, location_info)


def render_index(request, context, location_info=None):
    APIKEY = ""
    context["map_data"] = {}
    if os.getenv("APIKEY"):
        APIKEY = os.getenv("APIKEY")
    if location_info and APIKEY:
        context["map_data"] = serializers.serialize('json', location_info)

    context["object_drop"] = Event.objects.all()
    context["APIKEY"] = APIKEY

    # assign user a location
    try:
        u = User.objects.get(username=request.user)
        try:
            context["user_location"] = u.location.location
        except:
            # new user, create location
            loc = Location(user=u)
            loc.save()
            context["user_location"] = u.location.location
    except:
        # home page
        pass
    return render(request, 'index.html', context=context)

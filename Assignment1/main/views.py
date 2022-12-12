# views.py
import requests
from django.contrib.gis.geos import Point, Polygon
from django.core.mail.backends import console
from django.http import JsonResponse, request
from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from django.contrib.auth.decorators import login_required
import json
import overpy


# Create your views here.
def register_request(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = request.POST.get('username')
			user_profile = Profile(user=user, username=username)
			user_profile.save()
			save_trip = Profile(user=user, username=username)
			save_trip.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = UserCreationForm()
	return render(request=request, template_name="registration/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, "You are now logged in as {username}.")
				return redirect("main:map")
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login.html", context={"login_form":form})

@login_required
def update_database(request):

    saveLoc = request.POST.get("locations", None)

    try:

        # my_coords = [float(coord) for coord in locations.split(", ")]
        my_profile = request.user.profile
        my_profile.locations = saveLoc
        my_profile.save()

        message = f"Updated {request.user.username} with {f'POINT({saveLoc})'}"

        return JsonResponse({"message": message}, status=200)
    except:
        return JsonResponse({"message": saveLoc}, status=400)



@login_required
def logout_request(request):
	logout(request)
	messages.info(request, "Successfully logged out!")
	return redirect("main:home")



@login_required
def nearby_attractions(request):
	try:
		#create overpass object
		api = overpy.Overpass()

		#get coords of map box
		bounding_box = request.POST.get("bbox", None)
		print("BBOX: ", bounding_box)

		# changing the bounding box to have correct coords for the map box
		if bounding_box:
			bbox = bounding_box.split(",")

			shuffled_bbox = [bbox[1], bbox[0], bbox[3], bbox[2]]
			mod_boundingbox = [float(item) for item in shuffled_bbox]
			bounding_box = mod_boundingbox

		#query to get all tourism attractions within bounding box area
		result = api.query(f"""
        [out:json];
        (

            node["tourism"="attraction"]{tuple(bounding_box)};
            way["tourism"="attraction"]{tuple(bounding_box)};
            relation["tourism"="attraction"]{tuple(bounding_box)};

        );
        out body;
        >;
        out skel qt;
        """)

		print("hola!")

		#if query has no results
		if len(result.nodes) == 0:
			return JsonResponse({"message": "No attractions found!"})


		#array for list of features for each result
		geojson_result = {

			"type": "FeatureCollection",
			"features": [],
		}

		nodes_in_way = []

		for way in result.ways:
			print("hello")
			geojson_feature = {

				"type": "Feature",
				"id": "",
				"geometry": "",
				"properties": {}
			}

			poly = []
			for node in way.nodes:
				#record nodes in a 'way' and adds them to associated array

				#make poly out of nodes in way
				nodes_in_way.append(node.id)
				poly.append([float(node.lon), float(node.lat)])

				try:
					poly = Polygon(poly)
				except:
					continue

				geojson_feature["id"] = f"way_{way.id}"
				geojson_feature["geometry"] = json.loads(poly.centroid.geojson)
				geojson_feature["properties"] = {}

				for k, v in way.tags.items():
					geojson_feature["properties"][k] = v
				print(geojson_feature)

				geojson_result["features"].append(
					geojson_feature)  # adding all the information of the mosque to the geojson object
				print(geojson_result)

			for node in result.nodes:
				#skip nodes in way as they have already been processed
				if node.id in nodes_in_way:
					continue

				geojson_feature = {
					"type": "Feature",
					"id": "",
					"geometry": "",
					"properties": {}
				}
				point = Point([float(node.lon), float(node.lat)])
				geojson_feature["id"] = f"node_{node.id}"
				geojson_feature["geometry"] = json.loads(point.geojson)
				geojson_feature["properties"] = {}
				for k, v in node.tags.items():
					geojson_feature["properties"][k] = v
				geojson_result["features"].append(geojson_feature)

		return JsonResponse(geojson_result, status=200)
	# return JsonResponse({"message":"yay"}, status=200)
	except Exception as e:
		return JsonResponse({"message": f"Error: {e}."}, status=400)

@login_required
def view_saved(request):
	userFilter = request.user.username;

	loc_query = Profile.objects.values('locations').filter(username=userFilter).values_list('locations', flat=True)
	location = loc_query[0]

	context = {
		"locationData": location
	}

	return render(request, 'savedMap.html', context)


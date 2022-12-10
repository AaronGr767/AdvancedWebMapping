# views.py
import requests
from django.contrib.gis.geos import Point
from django.core.mail.backends import console
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from django.contrib.auth.decorators import login_required
import json;
import overpy;

# from rest_framework.permissions import AllowAny
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import UserSerializer,RegisterSerializer
# from django.contrib.auth.models import User
# from rest_framework.authentication import TokenAuthentication
# from rest_framework import generics

# Create your views here.
def register_request(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = request.POST.get('username')
			user_profile = Profile(user=user, username=username)
			user_profile.save()
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

    my_location = request.POST.get("point", None)
    if not my_location:
        return JsonResponse({"message": "No location found."}, status=400)

    try:
        my_coords = [float(coord) for coord in my_location.split(", ")]
        my_profile = request.user.profile
        my_profile.last_location = Point(my_coords)
        my_profile.save()

        message = f"Updated {request.user.username} with {f'POINT({my_location})'}"

        return JsonResponse({"message": message}, status=200)
    except:
        return JsonResponse({"message": "No profile found."}, status=400)

@login_required
def logout_request(request):
	logout(request)
	messages.info(request, "Successfully logged out!")
	return redirect("main:home")

@login_required
def map_content(request):
	overpass_url = "http://overpass-api.de/api/interpreter"
	overpass_query = """
	[out:json][timeout:25];
	{{geocodeArea:Dublin}}->.searchArea;
	(
	  node["amenity"="bar"](area.searchArea);
	  way["amenity"="bar"](area.searchArea);
	  relation["amenity"="bar"](area.searchArea);
	);
	out body;
	>;
	out skel qt;
	"""
	response = requests.get(overpass_url,
                        params={'data': overpass_query})
	data = response.json()
	console.log(data);

# Class based view to Get User Details using Token Authentication
# class UserDetailAPI(APIView):
#   authentication_classes = (TokenAuthentication,)
#   permission_classes = (AllowAny,)
#   def get(self,request,*args,**kwargs):
#     user = User.objects.get(id=request.user.id)
#     serializer = UserSerializer(user)
#     return Response(serializer.data)
#
# #Class based view to register user
# class RegisterUserAPIView(generics.CreateAPIView):
#   permission_classes = (AllowAny,)
#   serializer_class = RegisterSerializer
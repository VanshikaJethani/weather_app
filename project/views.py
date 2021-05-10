import requests
from django.shortcuts import render ,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse_lazy
from .models import City
from .forms import CityForm


def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=fa4e5808ff3c0398cd0e96194231ccfd"

    err_msg = ""
    message = ""
    message_class = ""

    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data["name"]
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r["cod"] == 200:
                    form.save()
                else:
                    err_msg = "City does not exist"
            else:
                err_msg = "City already exists in database"

        if err_msg:
            message = err_msg
            message_class = "failed"
        else:
            message = "City added successfully"
            message_class = "success"

    form = CityForm()
    weather_data = []

    cities = City.objects.all()

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            "city": city.name,
            "temperature": r["main"]["temp"],
            "pressure": r["main"]["pressure"],
            "humidity": r["main"]["humidity"],
            "description": r["weather"][0]["description"],
            "icon": r["weather"][0]["icon"],
            "speed": r["wind"]["speed"],
        }

        weather_data.append(city_weather)
        # print(weather_data)

    context = {
        "weather_data": weather_data,
        "form": form,
        "message": message,
        "message_class": message_class,
    }
    return render(request, "project/weather.html", context)

def delete_city(request , city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')

def about(request) :
    return render(request,'project/about.html')

def help(request):
    return render(request,'project/help.html')
from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

def index(request):

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate

    form = CityForm()

    cities = City.objects.all() #return all the cities in the database

    weather_data = []

    for city in cities:

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=122bbb36f374c2428a4717c58a1e65b4'

        try:
            city_weather = requests.get(url.format(city.name)).json() #request the API data and convert the JSON to Python data types
            
            weather = {
                'id' : city.id,
                'city' : city_weather['name'],
                'temperature' : city_weather['main']['temp'],
                'humidity': city_weather['main']['humidity'],
                'wind': city_weather['wind']['speed'],
                'description' : city_weather['weather'][0]['description'],
                'icon' : city_weather['weather'][0]['icon'],
            }

            weather_data.append(weather) #add the data for the current city into our list
        except KeyError:
            weather={
                    'id': city.id,
                    'city': "invalid city",

            }
            weather_data.append(weather)

        else:
            pass
    
    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/index.html', context) #returns the index.html template

def delete(request, city_id):
    city = City.objects.get(pk=city_id)
    city.delete()

    return redirect('/')
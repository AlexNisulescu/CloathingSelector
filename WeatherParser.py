import json

file = open("weather.json", "r")
data = json.load(file)
cityName=data['name']
temperature=data['main']['temp']
humidity=data['main']['humidity']
wind=data['wind']['speed']
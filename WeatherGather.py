import urllib.error
import urllib.request
import urllib.parse
import sys
import json

cityname = sys.argv[1]
url = "http://api.openweathermap.org/data/2.5/weather?q=" + cityname + "&appid=6159a870c03b130d2571733f23ffcbb6&units=metric"
response = urllib.request.urlopen(url)
webContent = response.read()    
file=open("E:\\Facultate\\Inteligenta artificiala\\weather.json", "w")
json_object = json.loads(webContent.decode('utf-8'))
json_formatted_str = json.dumps(json_object, indent=4) 
file.write(json_formatted_str)
file.close

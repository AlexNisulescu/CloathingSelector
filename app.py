import sys
from flask import Flask, request, jsonify
from flask import render_template
sys.path.append('./modules')
import WeatherGather
import WeatherParser
import OutfitFinder
import csvReader

app = Flask(__name__)



@app.route('/', methods=["GET","POST"])
def index():
	if request.method == 'POST':
		data = request.form['city_name']
		try:
			WeatherGather.send_API(data)
			cityName,temperature,humidity,wind=WeatherParser.read_JSON()
			hat,top,pants,shoes=OutfitFinder.HC(float(temperature),float(humidity),float(wind))
			cap=hat
			haina=top
			incaltaminte=shoes
			pantaloni=pants
			hat=csvReader.find_image(hat)
			top=csvReader.find_image(top)
			pants=csvReader.find_image(pants)
			shoes=csvReader.find_image(shoes)
		except:
			cityName=""
			data=""
			temperature=""
			humidity=""
			wind=""
			hat=""
			top=""
			pants=""
			shoes=""
			cap=""
			haina=""
			pantaloni=""
			incaltaminte=""
	else:
		cityName=""
		data=""
		temperature=""
		humidity=""
		wind=""
		hat=""
		top=""
		pants=""
		shoes=""
		cap=""
		haina=""
		pantaloni=""
		incaltaminte=""
	return render_template('index.html',city=cityName,temp=str(temperature)+"°C",umiditate=str(humidity)+
		"%",wind=str(wind)+" km/h",hat=hat,top=top,pants=pants,shoes=shoes,cap=cap,incaltaminte=incaltaminte,pantaloni=pantaloni,haina=haina)




if __name__ == '__main__':
    app.run(debug=True)

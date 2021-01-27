from flask import Flask, request, jsonify
from flask import render_template
import WeatherGather
import WeatherParser

app = Flask(__name__)



@app.route('/', methods=["GET","POST"])
def index():
	if request.method == 'POST':
		data = request.form['city_name']
		try:
			WeatherGather.send_API(data)
			cityName,temperature,humidity,wind=WeatherParser.read_JSON()
		except:
			cityName=""
			data=""
			temperature=""
			humidity=""
			wind=""
	else:
		cityName=""
		data=""
		temperature=""
		humidity=""
		wind=""
	return render_template('index.html',city=cityName,temp=temperature,umiditate=humidity,wind=wind)




if __name__ == '__main__':
    app.run(debug=True)

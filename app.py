from flask import Flask, request, jsonify
from flask import render_template
from flask_mysqldb import MySQL
import MySQLdb 
import os

import WeatherGather
import WeatherParser

app = Flask(__name__)



@app.route('/', methods=["GET","POST"])
def index():
	if request.method == 'POST':
		data = request.form['city_name']
		WeatherGather.send_API(data)
		temperature,humidity,wind=WeatherParser.read_JSON()
	else:
		data=""
	return render_template('index.html',city=data,temp=temperature,umiditate=humidity,wind=wind)




if __name__ == '__main__':
    app.run(debug=True)

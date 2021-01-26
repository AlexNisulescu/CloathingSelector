from flask import Flask, request, jsonify
from flask import render_template
from flask_mysqldb import MySQL
import MySQLdb 
import os
app = Flask(__name__)




@app.route('/', methods=["GET","POST"])
def index():
	if request.method == 'POST':
		data = request.form['city_name']
	else:
		data=""
	return render_template('index.html',data=data,len=len(data))




if __name__ == '__main__':
    app.run(debug=True)

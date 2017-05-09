from flask import render_template, request
from app import app
from .implplag import pattcomp

@app.route('/')
def search():
	return render_template('index.html')

@app.route('/results',methods=['POST'])
def results():
	s = pattcomp(request.form['pdf1'],request.form['pdf2'],request.form['activity'])
	return render_template('results.html',orders=s['orders'],filename1=s['filename1'],filename2=s['filename2'],pattern=s['comp'])

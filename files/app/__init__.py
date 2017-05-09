from flask import Flask
from flask_bootstrap import Bootstrap
#from fuzzywuzzy import fuzz
app = Flask(__name__)
Bootstrap(app)
from app import views

'''
def fuzzcomp(i, j):
	try:
		return fuzz.partial_ratio(i,j)
	except TypeError:
		return 0

app.jinja_env.globals.update(fuzzcomp=fuzzcomp)
'''

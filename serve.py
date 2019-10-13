from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def landingPage(name=None):
	return render_template('index.html', name=name)


@app.route('/map') # build url with params
def mapPage(name=None):
	return render_template('map.html', name=name)

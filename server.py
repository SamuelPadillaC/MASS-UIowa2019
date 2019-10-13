from flask import Flask, render_template, request
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import json
import twitter_credentials
import requests
import json
from urllib.parse import quote
import requests
from mapbox import Uploader

#Azure credentials is in the same folder
from Azure_Credentials import *



app = Flask(__name__)
# Mapbox token from env
app.config.from_envvar('APP_CONFIG_FILE', silent=True)
MAPBOX_ACCESS_TOKEN = app.config['MAPBOX_ACCESS_TOKEN']



# HTTP ROUTES

@app.route('/')
def landingPage(name=None):
	return render_template('index.html', name=name)

@app.route('/createcm', methods=['GET'])
def foo():
	print(request.args.get('summary'))
	(request.args.get('change'))
	return

@app.route('/map') # build url with params
def mapbox_js():

	# 0. Parse url get data
	keywordInput = request.args.get('keyword')

	# 1. Fetch tweets from twitter api
	# Authenticate using config.py and connect to Twitter Streaming API.
	hash_tag_list = [keywordInput]
	fetched_tweets_filename = "tweets.json"
	twitter_streamer = TwitterStreamer()
	twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

	#formatter
	formatForML('tweets.json', 'formattedData.json')

	# 2. Request to azure - positive or negative analysis
	calculate_sentiment('formattedData.json', 'predicted.json')

	geoConverter('predicted.json', 'myoutput.geojson')
	# 4. Send data file to mapbox api
	service = Uploader()
	from time import sleep
	from random import randint
	mapid = getfixture('myoutput.geojson')# 'uploads-test'
	with open('myoutput.geojson', 'rb')as src:
		upload_resp = service.upload(src, mapid)
		if(upload_resp.status_code):
			print(upload_resp.status_code)

	return render_template('map.html', ACCESS_KEY=MAPBOX_ACCESS_TOKEN)





# ML FUNCTION POSITIVITY
def calculate_sentiment (json_file, output_file):
	payload = {'documents': []}
	location = {'documents': []}

	f = open(json_file, "r")

	for data_line in f:
		if data_line != '\n':
			data = json.loads(data_line)

			dummy_dict = {}
			for element in data:
				if "id" in element:
					dummy_dict["id"] = data[element]

				if "text" in element:
					dummy_dict["text"] = data[element]

				if "lang" in element:
					dummy_dict["lang"] = data[element]

				if "loc" in element:
					location["documents"].append({"loc": data[element]})

				payload["documents"].append(dummy_dict)

	# sending POST request and saving the response as response object
	r = requests.post(url=URL, headers=headers, json=payload)

	# extracting data in json format
	data_received = r.json()

	# opening the output_file
	O = open(output_file, 'a')

	for received in data_received["documents"]:
		output_dummy_dic = {}

		if "id" in received:
			output_dummy_dic["id"] = received["id"]
		if "score" in received:
			output_dummy_dic["positivity"] = received["score"]

		output_dummy_dic["text"] = payload["documents"][data_received["documents"].index(received)]["text"]
		output_dummy_dic["lang"] = payload["documents"][data_received["documents"].index(received)]["lang"]
		output_dummy_dic["loc"] = location["documents"][data_received["documents"].index(received)]["loc"]
		output_dummy_dic["coordinates"] = geocodeAPI(location["documents"][data_received["documents"].index(received)]["loc"])
		print('aaloha')
		json.dump(output_dummy_dic, O)
		# json.dump('\n', O)
		print('aaaaaaaaloha')

	return output_file


def geocodeAPI(tweetLocation):
	# api-endpoint
	URL = "https://maps.googleapis.com/maps/api/geocode/json"
	key = "AIzaSyBPXIxdqJoKmT6lWdf6vswfV6reCwam0sM"
	# defining a params dict for the parameters to be sent to the API
	PARAMS = {'address':tweetLocation, 'key':key}
	# sending get request and saving the response as response object
	r = requests.get(url = URL, params = PARAMS)
	# extracting data in json format
	data = r.json()
	# extracting latitude, longitude and formatted address
	# of the first matching location
	latitude = data['results'][0]['geometry']['location']['lat']
	longitude = data['results'][0]['geometry']['location']['lng']
	formatted_address = data['results'][0]['formatted_address']
	# printing the output
	return [latitude, longitude]


def formatForML(input_name, output_name):

	f = open(input_name, "r")

	for line in f:
		if line != '\n':
			data = json.loads(line)

	#dictionary to be saved in JSON at the end
		mydict = {}

		#iterate over attributes
		for element in data:
			if "id_str" in element and len(element) == 6:
				mydict["id"] = data["id_str"]

			#if "text" in element and len(element) == 4:
			#	mydict["text"] = data["text"]

			if "user" in element and len(element) == 4:
				for a in data[element]:
					if "location" in a:
						mydict["loc"] = data[element][a]

			if "location" in element and len(element) == 4:
				mydict["location"] = data["location"]

			if "lang" in element and len(element) == 4:
					mydict["lang"] = data["lang"]

			#open the output file in append mode and write json
		with open(output_data_path, 'a') as f:
			json.dump(mydict, f)


	resultingJSON = json.loads(output_name)
	return resultingJSON


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
	"""
	Class for streaming and processing live tweets.
	"""
	def __init__(self):
		pass

	def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
		# This handles Twitter authetification and the connection to Twitter Streaming API
		listener = StdOutListener(fetched_tweets_filename)
		auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
		auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
		stream = Stream(auth, listener)

		# This line filter Twitter Streams to capture data by the keywords:
		stream.filter(track=hash_tag_list)



# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):

	def __init__(self, fetched_tweets_filename, time_limit=15):
		self.start_time = time.time()
		self.limit = time_limit
		self.fetched_tweets_filename = fetched_tweets_filename
		super(StdOutListener, self).__init__()

	def on_data(self, raw_data):
		if (time.time() - self.start_time) < self.limit:
			try:
				with open(self.fetched_tweets_filename, 'a') as tf:
					# parsing data
						# mydata = []
						# parsedRoute = json.loads(raw_data)
						# dataLocation = parsedRoute["user"]["location"]
						# if (dataLocation is not None):
						# 	print("New post with location found at: ", dataLocation)
						# 	newObj = {
						# 			"lang": parsedRoute["user"]["lang"],
						# 			"id_str": parsedRoute["user"]["id"],
						# 			"text": parsedRoute["text"],
						# 			"location": dataLocation,
						# 		}
						# 	print('aa')

						#json.dump(newObj, tf)
					tf.write(raw_data)
				return True
				print('aaaa')
			except Exception as e:
				print("Error on_data %s" % str(e))
				return True
			return True
		else:
			return False

	def on_error(self, status):
		print(status)


def geoConverter (in_file, out_file):
	f = open(input_data_path, "r")

	for line in f:
		if line != '\n':
			data = json.loads(line)
			mydict = {}
			for element in data:
				if "id" in element:
					mydict["id"] = data["id"]
				if "text" in element:
					mydict["text"] = data["text"]
				if "lang" in element:
					mydict["lang"] = data["lang"]
				if "loc" in element:
					mydict["loc"] = data["loc"]
				if "positivity" in element:
					p = data["positivity"]
					mydict["positivity"] = data["positivity"]
					if (p < 0.25):
						mydict["positivity"] = 1
					elif (p >= 0.25 and p < 0.5):
						mydict["positivity"] = 2
					elif (p >= 0.5 and p < 0.75):
						mydict["positivity"] = 3
					elif (p >= 0.75 and p < 1.0):
						mydict["positivity"] = 4

				if "coordinates" in element:
					mydict["coordinates"] = data["coordinates"]

			geojson = {
				"type": "Feature",
				"geometry": {
					"type": "Point",
					"coordinates": [mydict["coordinates"][0], mydict["coordinates"][1]]
					},
				"properties": {
					"id": mydict["id"],
					"text": mydict["text"],
					"lang": mydict["lang"],
					"loc": mydict["loc"],
					"positivity": mydict["positivity"]
				}
			}

		output = open(out_file, 'w')
		json.dump(geojson, output)

	return

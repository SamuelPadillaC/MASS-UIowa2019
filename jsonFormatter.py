import json

def formatForML(input_data_path, output_data_path):

	f = open(input_data_path, "r")

	for line in f:
		if line != '\n':
			data = json.loads(line)

	#dictionary to be saved in JSON at the end
		mydict = {}

		#iterate over attributes
		for element in data:
			if "id_str" in element and len(element) == 6:
				mydict["id"] = data["id_str"]

			if "text" in element and len(element) == 4:
				mydict["text"] = data["text"]

			if "user" in element and len(element) == 4:
				#print(element)
				for a in data[element]:
					if "location" in a:
						mydict["loc"] = data[element][a]

			if "lang" in element and len(element) == 4:
					mydict["lang"] = data["lang"]

			#open the output file in append mode and write json
		with open(output_data_path, 'a') as f:
			json.dump(mydict, f)

	
	resultingJSON = json.loads(output_data_path)
	return resultingJSON

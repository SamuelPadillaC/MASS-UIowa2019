import json

#dictionary to be saved in JSON at the end
mydict = {}

#change the jason file name
data_path = "DIRECTORY/FILE_NAME"
output_file = "DIRECTORY/OUTPUT_FILE"

with open(data_path) as data_file:
	data = json.load(data_file)

#iterate over attributes
for element in data:
	if 'id' in element:
		#save the id value to dictionary
		mydict["id"] = data['id']

	if "text" in element:
		mydict["text"] = data["text"]

	if "user" in element:
		for a in element:
			if "location" in a:
				mydict["loc"] = element["location"]

	if "quoted_status" in element:
		for b in element:
			if "lang" in b:
				mydict["lang"] = element["lang"]

	#open the output file in append mode and write json
	with open(output_file, 'a') as f:
		json.dump(mydict, f)

	


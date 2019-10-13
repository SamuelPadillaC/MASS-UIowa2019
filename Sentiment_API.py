import requests
import json
#Azure credentials is in the same folder
from Azure_Credentials import *
from jsonFormatter import *


def Calculate_Sentiment (json_file, output_file):
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

      json.dump(output_dummy_dic, O)
      json.dump('\n', O)


  return output_file

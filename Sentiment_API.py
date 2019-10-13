import requests
import json
#Azure credentials is in the same folder
from Azure_Credentials import *

# define the data to be analyzed
payload = {
  "documents": [
    {
      "language": "en",
      "id": "1",
      "text": "Hello world. I fucking hate my fucking life fuck this shit."
    },
    {
      "language": "fr",
      "id": "2",
      "text": "Bonjour tout le monde"
    },
    {
      "language": "es",
      "id": "3",
      "text": "La carretera estaba atascada. Había mucho tráfico el día de ayer."
    }
  ]
}

# sending POST request and saving the response as response object 
r = requests.post(url=URL, headers=headers, json=payload)

# extracting data in json format 
data = r.json()

print (data)
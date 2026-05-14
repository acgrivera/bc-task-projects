import json
import requests
"""
extracts from json file
required parameterL
    filename: string
"""
def extract_from_file(filename):                    #Extract from file
    with open(filename, 'r') as file:
        data = json.load(file)
    return data
extract_from_file("sampleJSON_transaction.json")

def extract_from_api(url):                          #Extract from API
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("API request failed")
    return response.json()

data_from_file = extract_from_file("sampleJSON_transaction.json")
data_from_api = extract_from_api("https://jsonplaceholder.typicode.com/posts")
print(data_from_api)
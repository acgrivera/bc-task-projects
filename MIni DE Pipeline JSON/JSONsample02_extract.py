import json
"""
extracts from json file
required parameterL
    filename: string
"""
def extract_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data
extract_from_file("sampleJSON_transaction.json")

data = extract_from_file("sampleJSON_transaction.json")

for item in data:                   #extract info from JSON
    print(item)
import json
"""
extracts from json file
required parameter
    filename: string
"""
def extract_from_file(filename):                    #conversion to python dictionary
    with open(filename, 'r') as file:
        data = json.load(file)
    return data
extract_from_file("sampleJSON_transaction.json")

print(extract_from_file("sampleJSON_transaction.json")) #print extracted from json file
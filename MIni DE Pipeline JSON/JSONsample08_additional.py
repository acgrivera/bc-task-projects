import json
import requests
import logging

logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True
)


#Fields for validation
required_fields = ["transaction_id", "amount", "currency"]
MAX_TRANSACTION_AMOUNT = 1000000

def load_config():
    with open("config/config.json") as f:
        return json.load(f)

config = load_config()
input_file = config["input_file"]
tax_rate = config["tax_rate"]
taxed_output = config["taxed_output"]
aggregated_output = config["aggregated_output"]

logging.info("Pipeline started")

#Extract from a JSON
def extract_from_file(filename): 
    try:
        with open(filename, 'r') as file:
            data = json.load(file)

            #Check if empty
            if not data or not isinstance(data, (list,dict)):
                logging.warning("Input file is empty")
                return []
            return data
    except(json.JSONDecodeError, FileNotFoundError):
        logging.error(f"Error: {filename}")
        return []
    
#def extract_from_api(url):                          #Extract from API
#    response = requests.get(url)
#   if response.status_code != 200:
#       raise Exception("API request failed")
#   return response.json()
data_from_file = extract_from_file(input_file)
#data_from_api = extract_from_api("https://jsonplaceholder.typicode.com/posts")
#print(data_from_api)

logging.info(f"Extracted {len(data_from_file)} records")

#Validate Schema
def validate_schema(record):                        #validate schema
    for field in required_fields:
        if field not in record:
            return False
    return True

#Filter the valid schema    
def filter_valid_schema(records):
    valid_records=[]
    for record in records:
        if validate_schema(record):
            valid_records.append(record)
    return valid_records

#Cleaning records
def clean_record(record):                          
    try:
        tx_id = record.get("transaction_id")
        raw_amount = record.get("amount")
        raw_currency = record.get("currency")               

        if tx_id is None or raw_amount is None or raw_currency is None:
            return None  
        
        amount = float(str(raw_amount).strip().replace(",", ""))            #Cleans leading/trailing spaces and eliminates commas
    
        if amount > MAX_TRANSACTION_AMOUNT:
            logging.warning(f"Abnormally Large Transaction: {raw_amount}")
            return None      
    
        currency = str(raw_currency).strip().upper()                        #Cleans leading/trailing spaces and converts any lowercase to uppercase

        return {
            "transaction_id":tx_id,
            "amount":amount,
            "currency":currency,
            "tax":amount*tax_rate
        }
    except(ValueError, TypeError):
        return None
    
#Remove Duplicates
def deduplicate_records(records):
    seen_ids = set()
    unique = []
    
    for record in records:
        if record is None:
            print("skipped: record is None")
            continue

        tx_id = record.get('transaction_id')
        
        if tx_id is not None and tx_id not in seen_ids:
            seen_ids.add(record["transaction_id"])
            unique.append(record)
            
    return unique

if data_from_file is None:
    print("Empty/Invalid File.")
    exit()                                                               #terminate if empty/invalid
else:
    valid_records = filter_valid_schema(data_from_file)
    cleaned_records = [clean_record(record) for record in valid_records]
    unique_records = deduplicate_records(cleaned_records)

logging.info(f"Cleaned {len(cleaned_records)} records")
logging.info(f"Deduplicated {len(unique_records)} records")

#Record Aggregation
def aggregate_by_currency(records):
    totals = {}

    for record in records:
        currency = record["currency"]
        totals[currency] = totals.get(currency,0) + record["amount"]
    return totals

aggregated_records = aggregate_by_currency(unique_records)

#File Creation
def dump_json(data,filename):
    with open(filename,'w') as file:
        json.dump(data,file,indent=4)
dump_json(unique_records,taxed_output)
dump_json(aggregated_records,aggregated_output)

logging.info("Pipeline Done. Files have been exported successfully.")
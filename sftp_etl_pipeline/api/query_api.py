import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

DBSR_API = os.getenv("TEST_API")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
HEADER = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}

def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def fetch_data_from_sql_file(sql_file_path, json_filename):
    query = read_sql_file(sql_file_path)
    return fetch_data_and_save(query, json_filename)

def fetch_data_and_save(query, json_filename):
    payload = { "query": query }
    try:
        response = requests.post(DBSR_API, headers=HEADER, json=payload)
        response.raise_for_status()
        data = response.json().get("results", [])
        
        json_output_dir = os.getenv("JSON_OUTPUT_DIR")
        os.makedirs(json_output_dir, exist_ok=True)
        json_file_path = os.path.join(json_output_dir, f"{json_filename}.json")

        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        print(f"Saved JSON data to {json_file_path}")
        return json_file_path

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

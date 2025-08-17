import os
import json
import requests
from datetime import datetime

API_URL = "https://example.com/api/endpoint"
USERNAME = "your_username"
PASSWORD = "your_password"
TOKEN_FOLDER = "tokens"

def fetch_and_save_token():
    payload = {
        "input_token_state": {
            "TOKEN_TYPE": "CREDENTIALS",
            "USERNAME": USERNAME,
            "PASSWORD": PASSWORD
        },
        "output_token_state": {
            "TOKEN_TYPE": "JWT"
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        print("🔍 Raw response text:", response.text)
        print("Content-Type:", response.headers.get("Content-Type"))

        try:
            data = response.json()
        except ValueError:
            print("❌ Response is not valid JSON")
            return

        if not isinstance(data, dict):
            print(f"❌ Expected dict, got {type(data).__name__}: {data}")
            return

        token = data.get("token") or data.get("access_token") or data.get("jwt")
        if not token:
            print("❌ Token not found in response:", data)
            return

        os.makedirs(TOKEN_FOLDER, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(TOKEN_FOLDER, f"jwt_token_{timestamp}.txt")

        with open(file_path, "w") as f:
            f.write(token)

        print(f"✅ Token saved to: {file_path}")

    except requests.RequestException as e:
        print(f"❌ Failed to fetch token: {e}")

if __name__ == "__main__":
    fetch_and_save_token()


import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

DBSR_API = os.getenv("TEST_API")

# Function to get the latest token from tokens folder
def get_latest_token():
    TOKEN_FOLDER = "tokens"
    try:
        files = [f for f in os.listdir(TOKEN_FOLDER) if f.startswith("jwt_token_")]
        if not files:
            print("❌ No token files found.")
            return None
        files.sort(reverse=True)  # newest first
        latest_file = os.path.join(TOKEN_FOLDER, files[0])
        with open(latest_file, "r") as f:
            token = f.read().strip()
        print(f"✅ Loaded token from: {latest_file}")
        return token
    except Exception as e:
        print(f"❌ Error reading token: {e}")
        return None

# Get token dynamically
BEARER_TOKEN = get_latest_token()

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

        print(f"✅ Saved JSON data to {json_file_path}")
        return json_file_path

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None

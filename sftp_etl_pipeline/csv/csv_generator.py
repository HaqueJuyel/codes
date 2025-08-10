# import csv
# import json
# import os

# def generate_csv_from_json(json_file_path, csv_filename):
#     if not os.path.exists(json_file_path):
#         print(f"JSON file not found: {json_file_path}")
#         return

#     with open(json_file_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)

#     if not data:
#         print(f"No data to write for {csv_filename}")
#         return

#     keys = data[0].keys() if isinstance(data, list) else data.keys()
#     csv_output_dir = os.getenv("CSV_OUTPUT_DIR")
#     os.makedirs(csv_output_dir, exist_ok=True)
#     csv_file_path = os.path.join(csv_output_dir, f"{csv_filename}.csv")

#     with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=keys)
#         writer.writeheader()
#         writer.writerows(data)

#     print(f"CSV file {csv_file_path} generated successfully.")
#     return csv_file_path

import csv
import json
import os

def generate_csv_from_json(json_file_path, csv_filename):
    if not os.path.exists(json_file_path):
        print(f"❌ JSON file not found: {json_file_path}")
        return None

    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Must be a non-empty list of dicts
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        print(f"❌ Invalid JSON format in {json_file_path}. Expected a list of dictionaries.")
        return None

    if not data:
        print(f"⚠ No data to write for {csv_filename}")
        return None

    keys = list(data[0].keys())  # Use first row's keys
    csv_output_dir = os.getenv("CSV_OUTPUT_DIR")
    os.makedirs(csv_output_dir, exist_ok=True)
    csv_file_path = os.path.join(csv_output_dir, f"{csv_filename}.csv")

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ CSV file {csv_file_path} generated successfully.")
    return csv_file_path

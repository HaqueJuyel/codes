from api import query_api as qa
from csv import csv_generator as cg
from sftp import sftp_uploader as sftp
import os

SQL_DIR = os.getenv("SQL_DIR")

# List of SQL files to process
csvs = {
    "test1": "query1.sql",
    "test2": "query2.sql"
}

def generate_all_csv():
    for filename, sql_file in csvs.items():
        sql_file_path = os.path.join(SQL_DIR, sql_file)

        # Step 1: Fetch and save JSON
        json_file_path = qa.fetch_data_from_sql_file(sql_file_path, filename)
        if not json_file_path:
            continue

        # Step 2: Convert JSON to CSV
        csv_file_path = cg.generate_csv_from_json(json_file_path, filename)
        if not csv_file_path:
            continue

        # Step 3: Upload to SFTP
        sftp.upload_to_sftp(r"D:\sftp\csv_output")

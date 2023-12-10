import csv
import os
import requests
import json

def download_ifsc_csv(url, destination):
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {destination}")
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")

def find_row_by_ifsc(ifsc_code, csv_file_path):
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)

        header = next(csv_reader, None)
        if not header:
            print("CSV file is empty.")
            return None

        # index of the 'IFSC' column
        ifsc_index = header.index('IFSC')

        for row in csv_reader:
            if row and row[ifsc_index] == ifsc_code:
                return dict(zip(header, row))

    return None

def get_details(ifsc_code):
    csv_url = "https://github.com/razorpay/ifsc/releases/latest/download/IFSC.csv"
    csv_file_path = 'IFSC.csv'

    # Download the CSV file if not already downloaded
    if not os.path.exists(csv_file_path):
        download_ifsc_csv(csv_url, csv_file_path)

    result_row = find_row_by_ifsc(ifsc_code, csv_file_path)

    if result_row:
        return json.dumps(result_row, indent=2)
    else:
        return json.dumps({"error": f"IFSC code {ifsc_code} not found in the CSV file."}, indent=2)

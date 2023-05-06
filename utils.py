import csv
import os
import re


def save_data_as_csv(data: list, headers:list):
    # Check if file exists and has data
    file_exists = os.path.exists('data.csv')
    file_has_data = os.stat('data.csv').st_size != 0 if file_exists else False

    # If file exists and has data, append new rows to the end
    # Otherwise, create a new file with a header row
    with open('data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_has_data:
            writer.writerow(headers)
        for row in data:
            writer.writerow(row)

def is_hashtag(text):
    pattern = r'\B#\w*[a-zA-Z]+\w*'
    match = re.search(pattern, text)
    if match:
        return True

def string_to_int(number_str):
    return int(number_str.replace(',', ''))
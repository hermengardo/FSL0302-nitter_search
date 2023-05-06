import csv
import os
import re


def save_dict_as_csv(data: dict, filename: str) -> None:
    headers = list(data.keys())
    rows = [list(row) for row in zip(*data.items())] if data else []
    
    # Check if file exists and has data
    file_exists = os.path.exists(filename)
    file_has_data = os.stat(filename).st_size != 0 if file_exists else False

    # If file exists and has data, append new rows to the end
    # Otherwise, create a new file with a header row
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_has_data:
            writer.writerow(headers)
        for row in rows:
            writer.writerow(row)

def is_hashtag(text: str) -> bool:
    pattern = r'\B#\w*[a-zA-Z]+\w*'
    match = re.search(pattern, text)
    if match:
        return True

def string_to_int(number_str) -> int:
    return int(number_str.replace(',', ''))
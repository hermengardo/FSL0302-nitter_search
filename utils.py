import csv
import os
import re
import urllib.parse

def save_dict_as_csv(data_dict: dict, file_path: str):
    print('Saving...')
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(data_dict.keys())
        max_len = max(len(v) if isinstance(v, list) else 1 for v in data_dict.values())
        for i in range(max_len):
            row = []
            for v in data_dict.values():
                if isinstance(v, list):
                    row.append(v[i] if i < len(v) else "")
                else:
                    row.append(v)
            writer.writerow(row)


def is_hashtag(text: str) -> bool:
    pattern = r'\B#\w*[a-zA-Z]+\w*'
    match = re.search(pattern, text)
    if match:
        return True


def string_to_int(number_str:str) -> int:
    return int(number_str.replace(',', ''))


def encode_string(input_string:str) -> str:
    return urllib.parse.quote(input_string, safe='/')
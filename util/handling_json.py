import json
from pprint import pprint
import os

def print_from_json(file_name):
    with open(file_name, 'r', encoding='UTF-8') as f:
        json_data = json.load(f)
    pprint(json.dumps(json_data, indent="\t",ensure_ascii=False))

def encoding_format_converter(file_name):
    with open(file_name, 'r', encoding='UTF-8') as f1:
        json_data = json.load(f1)
    with open(file_name, 'w', encoding='UTF-8') as json_writter:
        json.dump(json_data, json_writter, indent=4,ensure_ascii=False)
    pprint(json_data)


if __name__ == '__main__':
    directory = "C:\\project\\code\\ai_company_evaluatuion\\ai portfolio\\crawling_data"
    for file_name in os.walk(directory).__next__()[2]:
        file_path = os.path.join(directory,file_name)
        encoding_format_converter(file_path)

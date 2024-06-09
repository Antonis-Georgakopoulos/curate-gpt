import os
import json
import uuid
from collections import defaultdict

def load_json_files(folder_path):
    json_files = [pos_json for pos_json in os.listdir(folder_path) if pos_json.endswith('.json')]
    data = []
    for file in json_files:
        with open(os.path.join(folder_path, file), 'r') as f:
            data.append((file, json.load(f)))
    return data

def save_json_file(folder_path, file_name, data):
    with open(os.path.join(folder_path, file_name), 'w') as f:
        json.dump(data, f, indent=4)

def make_id_unique(item):
    if 'id' in item:
        item['id'] = f"{item['id']}_{uuid.uuid4()}"
    return item

def process_json_files(folder_path, save_new=False):
    data = load_json_files(folder_path)
    id_count = defaultdict(int)
    
    # Count all IDs
    for _, json_data in data:
        for item in json_data:
            if 'id' in item:
                id_count[item['id']] += 1
    
    # Make IDs unique where necessary
    for file_name, json_data in data:
        for item in json_data:
            if 'id' in item and id_count[item['id']] > 1:
                item = make_id_unique(item)
        
        new_file_name = file_name if not save_new else f"updated_{file_name}"
        save_json_file(folder_path, new_file_name, json_data)
        print(f"Processed file: {new_file_name}")

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder containing JSON files: ")
    save_new_files = input("Do you want to save updated files with new names? (yes/no): ").lower() == 'yes'
    process_json_files(folder_path, save_new_files)

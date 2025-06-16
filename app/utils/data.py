import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '../../data/employees.json')

def load_employees():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_employees(employees):
    with open(DATA_FILE, 'w') as f:
        json.dump(employees, f, indent=4) 
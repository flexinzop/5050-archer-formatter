# src/archer_formatter/read_csv.py

import pandas as pd

def read_file(csv_path):
    try:
        df = pd.read_csv(csv_path, sep=';')
        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
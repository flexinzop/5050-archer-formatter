import pandas as pd

def read_file(csv_path):
    return pd.read_csv(csv_path, sep=';')
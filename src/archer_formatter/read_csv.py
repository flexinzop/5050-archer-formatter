# src/archer_formatter/read_csv.py

import pandas as pd
from archer_formatter.utils import logger

def read_file(csv_path):
    try:
        df = pd.read_csv(csv_path, sep=';')
        return df
    except FileNotFoundError as e:
        logger.error(f"File not found: {csv_path}")
        raise
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        raise
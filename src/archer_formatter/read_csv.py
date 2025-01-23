# src/archer_formatter/read_csv.py
import glob
import xml.etree.ElementTree as ET
from pathlib import Path

def read_file(xml_files):
    # try:
    #     df = pd.read_csv(csv_path, sep=';')
    #     return df
    # except Exception as e:
    #     print(f"Error reading file: {e}")
    #     return None
    try:
        xml_files = archer_xml_folder.glob("*.xml")

        for file in xml_files:
            print(f"Processing file: {file}")

            tree = ET.parse(file)
            root = tree.getroot()

            # Nested list

            xml_list = []
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

        
archer_xml_folder = Path("data/xml_data")

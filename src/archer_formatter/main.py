import pandas as pd
import xml.etree.ElementTree as ET
import sys

from src.archer_formatter import convert_to_xml
from src.archer_formatter.read_csv import read_file
from src.archer_formatter.sanitize_csv import sanitize_file
from src.archer_formatter.convert_to_xml import convert_file
from archer_formatter.apply_rules import apply_rules
from src.archer_formatter.apply_rules import create_json_handler

#----------------------------------------------------------------#
#             The main entry point of application.               #
#                                                                #
#     Desc: Script para converter arquivos CSV                   #
#     em XML mantendo o padrão elencado pelo BACEN CADOC 5050    #
#     Author: Samuel Pimenta                                     #
#     Company: Athena Soluções Inteligentes                      #
#     Data: 01/10/24                                             #
#                                                                #
#----------------------------------------------------------------#



def main():
    if len(sys.argv) != 3:
        print("Usage: python -m src.archer_formatter.main <csv_file_path> <output_folder_path>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    output_folder_path = sys.argv[2]

    # Read the CSV file
    df = read_file(csv_file_path)

    # Sanitize the data
    df = sanitize_file(df)

    # Apply business rules
    df = apply_rules(df)

    # Convert to XML
    convert_to_xml(df, output_folder_path)

if __name__ == "__main__":
    main()
import pandas as pd
import xml.etree.ElementTree as ET
import sys

from read_csv import read_file
from sanitize_csv import sanitize_file
from convert_to_xml import convert_file
from apply_rules import create_json_handler

#----------------------------------------------------------------#
#                                                                #
#     Desc: Script para converter arquivos CSV                   #
#     em XML mantendo o padrão elencado pelo BACEN CADOC 5050    #
#     Author: Samuel Pimenta                                     #
#     Company: Athena Soluções Inteligentes                      #
#     Data: 01/10/24                                             #
#                                                                #
#----------------------------------------------------------------#

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("Usage: python main.py <csv_file_path> <output_folder_path>")
        sys.exit(1)
    
    # Get CSV file path and output folder from arguments
    csv_file_path = sys.argv[1]
    output_folder_path = sys.argv[2]

    # Read the CSV file
    df = read_file(csv_file_path)
    
    # Apply sanitization and rules
    create_json_handler(df)
    
    # Convert and save the XML file in the specified output folder
    convert_file(df, output_folder_path)
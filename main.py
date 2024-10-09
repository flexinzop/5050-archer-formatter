import pandas as pd
import xml.etree.ElementTree as ET

from src.archer_formatter.read_csv import read_file
from src.archer_formatter.sanitize_csv import sanitize_file
from src.archer_formatter.convert_to_xml import convert_file
from src.archer_formatter.apply_rules import create_json_handler

#----------------------------------------------------------------#
#                                                                #
#     Desc: Script para converter arquivos CSV                   #
#     em XML mantendo o padrão elencado pelo BACEN CADOC 5050    #                                                  
#     Author: Samuel Pimenta & Pedro Brito                       #                                        
#     Company: Athena Soluções Inteligentes                      #
#     Data: 01/10/24                                             #
#                                                                #
#----------------------------------------------------------------#

if __name__ == "__main__":

    df = read_file("data/base.csv")
    convert_file(df)
    create_json_handler(df)

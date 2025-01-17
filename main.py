import pandas as pd
import xml.etree.ElementTree as ET

from src.archer_formatter.read_csv import read_file
from src.archer_formatter.convert_to_xml import convert_file
from src.archer_formatter.apply_rules import create_json_handler
from src.archer_formatter.sanitize_csv import check_mandatory_fields


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

    class Taskflow:
        def __init__(self, csv_path):
            self.csv_path = csv_path
            self.df = None

        def execute(self):
            # Reading the csv file
            print("Reading the csv file...")
            self.df = read_file(self.csv_path)

            # Creating the json handler
            print("Creating the json handler...")
            create_json_handler(self.df)

            # Checking the mandatory fields
            print("Checking the mandatory fields...")
            if not check_mandatory_fields(self.df):
                print("There is missing mandatory fields in the csv file... Exiting")
                return  # Interrompe o fluxo se faltarem campos obrigatórios

            # Converting the file to xml
            print("Converting the file to xml...")
            convert_file(self.df)
            print("The operation has been completed successfully!")


    flow = Taskflow("data/base.csv")
    flow.execute()

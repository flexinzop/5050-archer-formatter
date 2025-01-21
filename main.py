import pandas as pd
import xml.etree.ElementTree as ET
import logging

from src.archer_formatter.read_csv import read_file
from src.archer_formatter.convert_to_xml import convert_file
from src.archer_formatter.apply_rules import create_json_handler
from src.archer_formatter.sanitize_csv import check_mandatory_fields
from src.archer_formatter.sanitize_csv import check_empty_columns

from src.archer_formatter.logger import init_logger

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
            # Initializing the logger
            self.logger = init_logger()

        def execute(self):
            self.logger.info("Starting the execution...")
            try:
                # Merge the files within data folder
                self.logger.info(f"Reading csv files from {self.csv_path}...")
                self.logger.info(f"Trying to merge csv files...")
                



                self.logger.info(f"Reading the csv file {self.csv_path}...")
                # Reading the csv file
                print("Reading the csv file...")
                self.df = read_file(self.csv_path)
                self.logger.info("The csv file has been read successfully!")
            except Exception as e:
                self.logger.error(f"Error reading the csv file: {e}")
                print(f"Error reading the csv file: {e}")
                raise e
            
            # Checking the empty columns
            print("Checking the empty columns...")
            if check_empty_columns(self.df):
                self.logger.error("There are empty columns in the csv file... Exiting")
                return  # Return if empty columns

            # Creating the json handler
            print("Creating the json handler...")
            create_json_handler(self.df)

            # Checking the mandatory fields
            print("Checking the mandatory fields...")
            if not check_mandatory_fields(self.df):
                self.logger.error("There is missing mandatory fields in the csv file... Exiting")
                return  # Return if missing mandatory fields

            # Converting the file to xml
            print("Converting the file to xml...")
            convert_file(self.df)
            print("The operation has been completed successfully!")

    flow = Taskflow("data/base.csv")
    flow.execute()
#----------------------------------------------------------------#
#                                                                #
#     Desc: Script para converter arquivos CSV                   #
#     em XML mantendo o padrão elencado pelo BACEN CADOC 5050    #                                                  
#     Author: Samuel Pimenta                                     #                                        
#     Company: Athena Soluções Inteligentes                      #
#     Data: 01/10/24                                             #
#                                                                #
#----------------------------------------------------------------#

import logging
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from archer_formatter.read_xml_file import read_file
from archer_formatter.convert_to_5050 import process_all_xmls, create_cadoc_template
from archer_formatter.logger import init_logger
# from archer_formatter.validation import validation_rules

filtered_records = []

class Taskflow:
    def __init__(self, xml_path):
        self.xml_path = xml_path
        self.logger = init_logger()

    def execute(self):
        self.logger.info("Starting the execution...")

        try:
            # Read xml files
            self.logger.info(f"Reading XML files from {self.xml_path}...")
            xml_files_data = read_file(self.xml_path)

            if not xml_files_data:
                self.logger.error("No XML files found or failed to process files.")
                return

            self.logger.info("XML files have been read successfully!")

            # Process XML files in order to extract field definitions
            self.logger.info("Processing XML files and extracting field definitions...\n")
            field_mappings, records_data = process_all_xmls(self.xml_path)

            if not records_data:
                self.logger.warning("No records found in the XML files.")
                return
            self.logger.info(f"Extracted {len(records_data)} records from XML files.")

            # Validate the XML
            self.logger.info("Processing XML files and extracting field definitions...\n")
            field_mappings, records_data = process_all_xmls(self.xml_path)
            
            for record in records_data:
                try:
                    valor_risco = float(str(record.get("N_Risco", "0")).replace(",", "").strip())
                    
                    if valor_risco > 1000000:
                        filtered_records.append(record)  # Mantém o registro válido
                        print(f"✅ Registro {record.get('idEvento', 'N/A')} incluído no XML (N_Risco: {valor_risco})")
                    else:
                        self.logger.warning(f"⚠️ Registro {record.get('idEvento', 'N/A')} descartado (N_Risco: {valor_risco})")

                except ValueError:
                    self.logger.error(f"❌ Erro ao converter N_Risco para número no registro {record.get('idEvento', 'N/A')}")

            if not filtered_records:
                self.logger.warning("⚠️ Nenhum registro válido encontrado para geração do XML.")
            else:
                self.logger.info(f"✅ {len(filtered_records)} registros válidos serão incluídos no XML.")
                create_cadoc_template(filtered_records)
            
            # Generate XML based on CADOC 5050 template
            # self.logger.info("Generating the CADOC 5050 XML output...")
            # create_cadoc_template(records_data)

            self.logger.info("XML successfully generated and saved as 'output.xml'!")

        except Exception as e:
            self.logger.error(f"An error occurred during execution: {e}")
            raise e
            
# 📌 Definimos o caminho do XML APENAS UMA VEZ
xml_folder_path = "data/xml_data/real_data"

# Executar o fluxo de processamento
if __name__ == "__main__":
    flow = Taskflow(xml_folder_path)
    flow.execute()
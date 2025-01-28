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
from archer_formatter.read_xml import read_file
from archer_formatter.xml_parser import parse_eventos_individualizados, parse_sistemas_origem
from archer_formatter.logger import init_logger

if __name__ == "__main__":

    class Taskflow:
        def __init__(self, xml_path):
            self.xml_path = xml_path
            self.logger = init_logger()

        def execute(self):
            self.logger.info("Starting the execution...")
            try:
                # Read XML files from the specified folder
                self.logger.info(f"Reading XML files from {self.xml_path}...")
                xml_files_data = read_file(self.xml_path)

                if not xml_files_data:
                    self.logger.error("No XML files found or failed to process files.")
                    return

                self.logger.info("XML files have been read successfully!")

                # Convert XML structure to CADOC 5050 format

                # XML Element parsing
                for xml_file in xml_files_data:
                    root = xml_file.get("root")
                    file_name = xml_file.get("file_name")

                    if root is None:
                        self.logger.error(f"Failed to parse XML for file {file_name}. Skipping...")
                        continue

                    self.logger.info(f"Parsing data for file: {file_name}")

                    # Parseando eventos individualizados
                    eventos = parse_eventos_individualizados(root)
                    self.logger.info(f"Parsed 'eventosIndividualizados': {eventos}")

                    # Parseando sistemas de origem
                    sistemas = parse_sistemas_origem(root)
                    self.logger.info(f"Parsed 'sistemasOrigem': {sistemas}")

                    # Log ou manipulação adicional dos dados parseados
                    self.logger.info(f"Finished parsing for file: {file_name}")
                    self.logger.info("-" * 50)

            except Exception as e:
                self.logger.error(f"An error occurred during the execution: {e}")
                raise e

    flow = Taskflow("data/xml_data")
    flow.execute()

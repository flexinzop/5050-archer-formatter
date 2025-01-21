import glob
import xml.etree.ElementTree as ET
from pathlib import Path

def iterate_xml_files(xml_files):
    xml_files = archer_xml_folder.glob("*.xml")

    for file in xml_files:
        print(f"Processing file: {file}")

        tree = ET.parse(file)
        root = tree.getroot()

        # Implementing only the 'eventosIndividualizados' tag

        eventos = root.find('eventosIndividualizados')  

        # Nested list

        xml_list = []

        # Iterate through the root
        for evento in eventos.findall("evento"):
            id_evento = evento.get("idEvento") # Capture the value of idEvento
            unidade_negocio = evento.get("unidadeNegocio") # Capture the value of unidadeNegocio
            print(id_evento, unidade_negocio)
            
            # Iterate through the children of the event
            
            xml_list.append({
                "evento": {
                    "idEvento": id_evento,
                    "other_fields": {attr: evento.get(attr) for attr in evento.keys() if attr != "idEvento"}
                }
            })

            nested_list = {
                "eventosIndividualizados": xml_list
            }

archer_xml_folder = Path("data/xml_data")

iterate_xml_files(archer_xml_folder)
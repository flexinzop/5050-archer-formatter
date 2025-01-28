import xml.etree.ElementTree as ET
from pathlib import Path

def read_file(xml_folder_path):
    """Lê arquivos XML dentro de uma pasta e retorna o objeto raiz e o nome do arquivo."""
    xml_folder = Path(xml_folder_path)
    xml_files = xml_folder.glob("*.xml")
    xml_data_list = []

    try:
        for file in xml_files:
            print(f"Processing file: {file}")
            tree = ET.parse(file)
            root = tree.getroot()

            # Adiciona o objeto raiz e o nome do arquivo à lista
            xml_data_list.append({
                "root": root,
                "file_name": file.name
            })
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    print(xml_data_list)

read_file("data/xml_data")

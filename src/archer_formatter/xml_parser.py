import glob
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom.minidom import parseString

def parse_eventos_individualizados(root):
    """Processa os subelementos de 'eventosIndividualizados'."""
    eventos = []
    eventos_individualizados = root.find('eventosIndividualizados')
    if eventos_individualizados is not None:
        for evento in eventos_individualizados.findall('evento'):
            evento_data = {key: value for key, value in evento.attrib.items()}
            eventos.append(evento_data)
    return eventos

def parse_sistemas_origem(root):
    """Processa os subelementos de 'sistemasOrigem'."""
    sistemas = []
    sistemas_origem = root.find('sistemasOrigem')
    if sistemas_origem is not None:
        for sistema in sistemas_origem.findall('sistema'):
            sistema_data = {key: value for key, value in sistema.attrib.items()}
            sistemas.append(sistema_data)
    return sistemas

def iterate_xml_files(xml_folder):
    """Itera sobre os arquivos XML em uma pasta e processa os dados."""
    xml_files = xml_folder.glob("*.xml")

    try:
        for file in xml_files:
            print(f"Processing file: {file}")
            tree = ET.parse(file)
            root = tree.getroot()

            # Dados do documento
            documento_data = {key: value for key, value in root.attrib.items()}

            # Processa 'eventosIndividualizados' e 'sistemasOrigem' usando funções específicas
            documento_data['eventosIndividualizados'] = parse_eventos_individualizados(root)
            documento_data['sistemasOrigem'] = parse_sistemas_origem(root)

            # Formata o XML do documento original
            formatted_xml = parseString(ET.tostring(root, encoding="unicode")).toprettyxml(indent="  ")
            print(f"Formatted XML for file {file.name}:\n{formatted_xml}")
            print("-" * 30)
    except Exception as e:
        print(f"Error processing file: {e}")

# Caminho para a pasta com arquivos XML
archer_xml_folder = Path("data/xml_data")

# Itera sobre os arquivos XML na pasta
iterate_xml_files(archer_xml_folder)

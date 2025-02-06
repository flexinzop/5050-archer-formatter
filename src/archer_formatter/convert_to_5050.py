import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom.minidom import parseString
from archer_formatter.hash_file import calculate_hash
import re  # Para limpar tags HTML
from archer_formatter.read_xml_file import read_file, get_field_definitions, mapeamento_cadoc


# Define function to extract text from Field element from Archer XML
def extract_text_from_field(field):
    """Extract all values from XML tags <Field> e <ListValues>."""
    if field.find("ListValues") is not None:
        list_value = field.find("ListValues/ListValue")
        return list_value.attrib.get("displayName", "").strip() if list_value is not None else ""
    
    if field.text:
        return re.sub(r"<.*?>", "", field.text).strip()  # Remove HTML

    return ""  # Return empty if no text is found

def process_all_xmls(xml_folder_path):
    """Read all XML files from folder and get <FieldDefinition> and records."""
    field_mappings = {}  # DICT {arquivo.xml: {campo_Archer: ID}}
    records_data = []  # Lista de registros extraídos

    # Lendo todos os arquivos XML na pasta
    xml_files_data = read_file(xml_folder_path)

    if not xml_files_data:
        print("Nenhum arquivo XML encontrado ou erro ao processar.")
        return {}, []

    for xml_data in xml_files_data:
        root = xml_data["root"]
        file_name = xml_data["file_name"]

        # Obter definições de campos
        field_mappings[file_name] = get_field_definitions(root)

        # 📌 Capturar o ID do FieldDefinition associado ao Tracking_ID
        tracking_id_field_id = None
        for field_def in root.findall(".//FieldDefinition"):
            if field_def.attrib.get("alias") == "Tracking_ID":  # Verifica se é o Tracking_ID
                tracking_id_field_id = field_def.attrib.get("id")
                break  # Só precisamos de um

        if not tracking_id_field_id:
            print(f"⚠️ Nenhum Tracking_ID encontrado no arquivo {file_name}. Pulando arquivo...")
            continue  # Se não encontrar o Tracking_ID, pula esse arquivo

        # 📌 Processar cada <Record>
        for record in root.findall(".//Record"):
            record_data = {}  # Criamos um dicionário para armazenar os campos do registro

            # 📌 Pegar o valor do Tracking_ID no registro
            id_evento = None
            for field in record.findall(".//Field"):
                if field.attrib.get("id") == tracking_id_field_id:
                    id_evento = extract_text_from_field(field)  # Pega o valor do Tracking_ID
                    break  # Já encontramos, podemos sair do loop

            if not id_evento:
                print(f"⚠️ Registro sem Tracking_ID encontrado. Pulando...")
                continue  # Se não tiver Tracking_ID, ignoramos esse registro

            record_data["idEvento"] = id_evento  # 🔹 Atribuímos o Tracking_ID como idEvento

            # 📌 Iterar sobre os outros campos dentro do <Record>
            for field in record.findall(".//Field"):
                field_id = field.attrib.get("id")
                field_value = extract_text_from_field(field)  # Função para extrair valores corretamente

                # Verificar se o ID do campo existe no mapeamento
                if file_name in field_mappings:
                    mapping = field_mappings[file_name]
                    if field_id in mapping.values():  # Se o ID do campo existir no mapeamento
                        field_name = list(mapping.keys())[list(mapping.values()).index(field_id)]
                        record_data[field_name] = field_value  # Associamos o nome correto ao valor

            # 📌 Adicionamos o registro APÓS processar todos os campos
            records_data.append(record_data)

            # Debugging interno para verificar a extração correta do ID
            print(f"📌 Processando registro: idEvento={record_data['idEvento']}")

    # 📌 Debugging final
    print("📌 Debug: Processamento do XML concluído.")
    print(f"📂 Arquivos lidos: {xml_folder_path}")
    print(f"🔎 Registros extraídos: {len(records_data)}")
    
    if not records_data:
        print("⚠️ Nenhum registro foi extraído do XML! Verifique se a estrutura do XML mudou.")

    return field_mappings, records_data

def create_cadoc_template(records_data):
    """Create XML formatted on BACEN 5050 model, consolidate all records from Archer."""

    # Create the root element fixed field data on 'cabeçalho' <documento>
    documento = ET.Element("documento", {"codigoDocumento": "5050", "dataBase": "2025-01", "codigoConglomerado":"C0099999", "tipoRemessa": "I", "cnpj": "99999999", "opcaoPorProvisaoAcumulada": "N"})

    # Create fields on other sections from `mapeamento_cadoc`
    subelementos = {secao: ET.SubElement(documento, secao) for secao in mapeamento_cadoc}

    # Proccess all records and create a new element on the correspondent section
    for record in records_data:
        for secao, campos in mapeamento_cadoc.items():
            atributos = {}

            for cadoc_campo, archer_campo in campos.items():
                if archer_campo in record and record[archer_campo]:  # Verify is the field is present and not empty
                    atributos[cadoc_campo] = record[archer_campo]
            # Create new element inside the correspondent section only if there are attributes
            if atributos:
                ET.SubElement(subelementos[secao], "evento", atributos)
    # Converter para string e formatar o XML
    xml_string = ET.tostring(documento, encoding="utf-8")
    pretty_xml = parseString(xml_string).toprettyxml(indent="  ")  # 2 spaces indentation

    pretty_xml = '<?xml version="1.0" encoding="utf-8"?>\n' + "\n".join(pretty_xml.split("\n")[1:])
    
    data_atual = datetime.now()
    
    data_atual_formatada = data_atual.strftime("%Y-%m-%d")
    
    final_filename = "cadoc-exported" + data_atual_formatada + ".xml"
    
    # Save the formatted XML prettified
    with open(final_filename, "w", encoding="utf-8") as file:
        file.write(pretty_xml)
    print("✅ XML criado e salvo com sucesso em com encoding UTF-8!")

    print(calculate_hash(final_filename))

# Folder with XML files from Archer
xml_folder = "data/xml_data/real_data"
# Process all XML files and get fields and records
field_mappings, records_data = process_all_xmls(xml_folder)

# Call the function to create the XML in CADOC 5050 format
# create_cadoc_template(records_data)
if __name__ == "__main__":
    # Process all XML files and get fields and records
    field_mappings, records_data = process_all_xmls(xml_folder)
    # Debug verify if the values of "Classificar de Evento" are being extracted correctly
    for record in records_data:
        print(f"Registro ID: {record.get('idEvento', 'N/A')}, Classificar de Evento: {record.get('Classificar de Evento', 'N/A')}")
    # Call the function to create the XML in CADOC 5050 format
    create_cadoc_template(records_data)
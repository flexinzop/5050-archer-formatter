import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import re  # Para limpar tags HTML
from read_xml import read_file, get_field_definitions, mapeamento_cadoc

def extract_text_from_field(field_value):
    """Remove tags HTML do valor do campo."""
    clean_text = re.sub(r"<.*?>", "", field_value)  # Remove qualquer tag HTML
    return clean_text.strip()

def process_all_xmls(xml_folder_path):
    """Lê todos os arquivos XML da pasta e captura os <FieldDefinition> e registros de cada um."""
    field_mappings = {}  # Dicionário final {arquivo.xml: {campo_Archer: ID}}
    records_data = []  # Lista de registros extraídos

    # Obter a lista de arquivos processados
    xml_files_data = read_file(xml_folder_path)

    if not xml_files_data:  # Se não houver arquivos, retorna um dicionário vazio
        print("Nenhum arquivo XML encontrado ou erro ao processar.")
        return {}, []

    for xml_data in xml_files_data:
        root = xml_data["root"]
        file_name = xml_data["file_name"]

        # Captura os <FieldDefinition> do arquivo
        field_mappings[file_name] = get_field_definitions(root)

        # Captura os registros <Record> e seus valores <Field>
        for record in root.findall(".//Record"):
            content_id = record.attrib.get("contentId", "")
            record_data = {"idEvento": content_id}  # Usa contentId como idEvento

            for field in record.findall(".//Field"):
                field_id = field.attrib.get("id")
                field_value = field.text.strip() if field.text else ""  # Pega o valor do campo

                # Remove HTML do valor do campo, se houver
                field_value = extract_text_from_field(field_value)

                # Mapeia ID para nome do campo usando field_mappings
                for file_name, mapping in field_mappings.items():
                    if field_id in mapping.values():  # Se o ID está no mapeamento
                        field_name = list(mapping.keys())[list(mapping.values()).index(field_id)]
                        record_data[field_name] = field_value  # Associa o nome do campo ao valor

            records_data.append(record_data)  # Adiciona o registro completo à lista

    return field_mappings, records_data

def create_cadoc_template(records_data):
    """Cria o XML no formato BACEN 5050, consolidando os dados do Archer."""
    
    # Criar o elemento raiz <documento>
    documento = ET.Element("documento", {"codigoDocumento": "5050"})

    # Criar a seção <eventosIndividualizados>
    eventos_individualizados = ET.SubElement(documento, "eventosIndividualizados")

    # Processar cada registro do Archer
    for record in records_data:
        atributos = {}

        for cadoc_campo in mapeamento_cadoc["eventosIndividualizados"]:
            if cadoc_campo in record:  # Verifica se o campo existe no registro
                atributos[cadoc_campo] = record[cadoc_campo]

        # Criar um novo elemento <evento> apenas com os atributos que possuem valor
        if atributos:
            ET.SubElement(eventos_individualizados, "evento", atributos)

    # Converter para string corretamente
    xml_bytes = ET.tostring(documento, encoding="utf-8")
    xml_string = xml_bytes.decode("utf-8")  # Decodifica para string

    # Agora `parseString` recebe uma string válida
    pretty_xml = parseString(xml_string).toprettyxml(indent="  ")

    # Salvar o XML gerado em um arquivo
    with open("output.xml", "w", encoding="utf-8") as file:
        file.write(pretty_xml)

    print("XML criado e salvo com sucesso!")

# Diretório dos arquivos XML
xml_folder = "data/xml_data/real_data"

# Processar todos os arquivos XML e capturar os campos e registros
field_mappings, records_data = process_all_xmls(xml_folder)

# Chamar a função para criar o XML no formato CADOC 5050
create_cadoc_template(records_data)

# Exibir o resultado final
print("Dicionário de mapeamento de campos:")
print(field_mappings)

print("\nLista de registros extraídos:")
print(records_data)

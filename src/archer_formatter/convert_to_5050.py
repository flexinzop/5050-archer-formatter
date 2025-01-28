import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

# xml conversion

# def convert_file(df):
#     root = ET.Element("documento")
#     for _, row in df.iterrows():
#         item = ET.SubElement(root, "Item")
#         for col in df.columns:
#             child = ET.SubElement(item, col)
#             child.text = str(row[col])

#     tree = ET.ElementTree(root)
#     xml_str = ET.tostring(root, encoding='UTF-8')
#     dom = parseString(xml_str)
#     formated_xml = dom.toprettyxml(indent="    ")  # 4 espaços de indentação

#     with open ("output.xml", "w") as f:
#         f.write(formated_xml)

#     print(f"XML file saved to your local folder")
#     return formated_xml

field_names = []

def get_field_definition(xml_file):
    atributos = {}
    # Load XML file
    tree = ET.parse(xml_file) # Change to 'xml_file' variable
    root = tree.getroot()

    # Iterar sobre os elementos <FieldDefinition>
    for field in root.findall(".//FieldDefinition"):
        # Create
        # Obter o valor do atributo 'name'
        # name = field.attrib.get("name")
        # if name:
        #     field_names.append(name)
        # print(f"Field name: {name}")
        alias = field.attrib.get("alias")
        if alias:
            atributos[alias] = ""
    return atributos

def create_cadoc_template():
    
    eventos_attrib = get_field_definition(xml_file)

    # Create the root element
    documento = ET.Element("documento", {"codigoDocumento": "5050"})

    # Create the sub-element
    eventos_individualizados = ET.SubElement(documento, "eventosIndividualizados")

    # Create the child element with the data extracted from the Archer XML Export
    ET.SubElement(eventos_individualizados, "evento", eventos_attrib)
    # Salvar o XML gerado em um arquivo
    tree = ET.ElementTree(eventos_individualizados)
    # Add the first child
    # evento = ET.SubElement(eventos_individualizados, "evento", get_field_definition())

    # Convert to string and format the XML
    pretty_xml = parseString(ET.tostring(documento, encoding="unicode")).toprettyxml(indent="  ")

    # Save to XML
    with open("output.xml", "w", encoding="utf-8") as file:
        file.write(pretty_xml)

    print("XML criado e salvo com sucesso!")

xml_file = 'data/xml_data/real_data/Riscos_Archer.xml'
create_cadoc_template()

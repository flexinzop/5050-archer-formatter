import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

# xml conversion

def convert_file(df):
    root = ET.Element("documento")
    for _, row in df.iterrows():
        item = ET.SubElement(root, "Item")
        for col in df.columns:
            child = ET.SubElement(item, col)
            child.text = str(row[col])

    tree = ET.ElementTree(root)
    xml_str = ET.tostring(root, encoding='UTF-8')
    dom = parseString(xml_str)
    formated_xml = dom.toprettyxml(indent="    ")  # 4 espaços de indentação

    with open ("output.xml", "w") as f:
        f.write(formated_xml)

    print(f"XML file saved to your local folder")
    return formated_xml
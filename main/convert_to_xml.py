import xml.etree.ElementTree as ET

# xml conversion

def convert_file(df):
    root = ET.Element("documento")
    for _, row in df.iterrows():
        item = ET.SubElement(root, "Item")
        for col in df.columns:
            child = ET.SubElement(item, col)
            child.text = str(row[col])

    tree = ET.ElementTree(root)
    tree.write("output.xml", encoding='UTF-8', xml_declaration=True)
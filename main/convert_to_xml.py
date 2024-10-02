import xml.etree.ElementTree as ET

# xml conversion

def convert_file(df, output_folder_path):
    root = ET.Element("documento")
    for _, row in df.iterrows():
        item = ET.SubElement(root, "Item")
        for col in df.columns:
            child = ET.SubElement(item, col)
            child.text = str(row[col])

    tree = ET.ElementTree(root)
    tree.write("output.xml", encoding='UTF-8', xml_declaration=True)
    
    output_file_path = f"{output_folder_path}/output.xml"
    tree = ET.ElementTree(root)
    tree.write(output_file_path)
    print(f"XML file saved to {output_file_path}")
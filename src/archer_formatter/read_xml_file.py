import xml.etree.ElementTree as ET
from pathlib import Path

# Mapeamento de campos por seção no CADOC 5050
mapeamento_cadoc = {
    "eventosIndividualizados": {
        "idEvento": "Tracking_ID",
        "categoriaNivel1": "categoriaNivel1",
        "valorTotalRisco" : "valorTotalRisco",
        "tipoAvaliacao": "tipoAvaliacao",
        "unidadeNegocio": "unidadeNegocio",
        "dataOcorrencia": "dataOcorrencia",
        "totalPerdaEfetiva": "totalPerdaEfetiva",
        "totalRecuperado": "totalRecuperado",
        "naturezaContingencia": "naturezaContingencia",
        "codSistemaOrigem": "codSistemaOrigem",
        "codigoEventoOrigem": "codigoEventoOrigem",
        "idBacen": "idBacen"
    },
    "probabilidadesPerdas": {
        "probabilidade": "",
        "valorRisco": ""
    },
    "contabilizacoes": {
        "dataContabilizacao": "",
        "valorPerdaEfetiva": ""
    },
    "eventosConsolidados": {
        "categoriaNivel1Consol": "",
        "numEventosTotalConsol": "",
        "numEventosSemestreConsol": "",
        "perdaEfetivaTotalConsol": "",
        "perdaEfetivaSemestreConsol": "",
        "provisaoTotalConsol": "Provisão Total",
        "provisaoSemestreConsol": "Provisão no Semestre"
    },
    "sistemasOrigem": {
        "codigoSistema": "Código do Sistema",
        "nomeSistema": "Nome do Sistema"
    },
    "contasSubtitulosInternos": {
        "codigoConta": "Código da Conta",
        "nomeConta": "Nome da Conta"
    }
}

def read_file(xml_folder_path):
    """Lê arquivos XML dentro de uma pasta e retorna uma lista de dicionários com root e nome do arquivo."""
    xml_folder = Path(xml_folder_path)
    xml_files = xml_folder.glob("*.xml")
    xml_data_list = []

    try:
        for file in xml_files:
            print(f"Processing file: {file.name}")
            tree = ET.parse(file)
            root = tree.getroot()

            # Adiciona o objeto raiz e o nome do arquivo à lista
            xml_data_list.append({
                "root": root,
                "file_name": file.name
            })
    except Exception as e:
        print(f"Error reading file {file.name}: {e}")
        return None

    return xml_data_list

def get_field_definitions(root):
    """Extrai os atributos 'alias' e 'id' de <FieldDefinition> e retorna um dicionário."""
    atributos = {}

    for field in root.findall(".//FieldDefinition"):
        alias = field.attrib.get("alias")  # Nome do campo
        id_field = field.attrib.get("id")  # ID do campo

        if alias and id_field:  # Verifica se ambos existem
            atributos[alias] = id_field  # Associa o nome do campo ao ID
    return atributos
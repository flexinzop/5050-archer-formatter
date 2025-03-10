import xml.etree.ElementTree as ET
import codecs
from pathlib import Path


# Mapeamento de campos por seção no CADOC 5050
mapeamento_cadoc = {
    "eventosIndividualizados": {
        "idEvento": "Loss_Event_ID",
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
            print(f"📂 Processando arquivo: {file}")

            # 📌 Abrir o arquivo em modo binário para detectar a codificação
            with open(file, "rb") as f:
                raw_data = f.read()

            # 📌 Tentar detectar a codificação automaticamente
            encoding = "utf-8"  # Assumimos UTF-8 como padrão
            if raw_data[:2] == b'\xff\xfe' or raw_data[:2] == b'\xfe\xff':
                encoding = "utf-16"  # Se tiver BOM, é UTF-16
            
            print(f"📌 Encoding detectado: {encoding}")

            # 📌 Abrir e converter para UTF-8 caso necessário
            with codecs.open(file, "r", encoding=encoding) as f:
                xml_content = f.read()

            # 📌 Criar a árvore XML a partir da string UTF-8 convertida
            root = ET.fromstring(xml_content)

            # Adiciona o objeto raiz e o nome do arquivo à lista
            xml_data_list.append({
                "root": root,
                "file_name": file.name
            })

    except Exception as e:
        print(f"❌ Erro ao ler o arquivo {file}: {e}")
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
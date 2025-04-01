import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom.minidom import parseString
import re  # Para limpar tags HTML
from archer_formatter.read_xml_file import read_file, get_field_definitions, mapeamento_cadoc
from archer_formatter.logger import init_logger
from archer_formatter.utils import formatar_valor_decimal
from archer_formatter.validation import filter_valid_records
from archer_formatter.anexos import anexo1_categoria_n1, mapear_categoria_n1_consolidado
from archer_formatter.validation import converter_unidade_negocio


logger = init_logger()  # Inicializa o logger

# Define campos obrigatórios (evita erro de importação)
required_fields = ["idEvento", "valorTotalRisco", "categoriaNivel1", "categoriaNivel2" "dataOcorrencia", 
                   "totalPerdaEfetiva", "totalRecuperado", 
                   "codSistemaOrigem", "codigoEventoOrigem", "idBacen"]

def extract_text_from_field(field):
    """Extrai valores do XML, removendo HTML se necessário."""
    if field.find("ListValues") is not None:
        list_value = field.find("ListValues/ListValue")
        return list_value.attrib.get("displayName", "").strip() if list_value is not None else ""
    
    if field.text:
        return re.sub(r"<.*?>", "", field.text).strip()  # Remove HTML

    return ""

def process_all_xmls(xml_folder_path):
    """Lê todos os XMLs na pasta e processa os registros."""
    field_mappings = {}
    records_data = []

    xml_files_data = read_file(xml_folder_path)
    if not xml_files_data:
        print("Nenhum arquivo XML encontrado.")
        return {}, []

    for xml_data in xml_files_data:
        root = xml_data["root"]
        file_name = xml_data["file_name"]

        # Captura <FieldDefinition>
        field_mappings[file_name] = get_field_definitions(root)

        # Captura o ID do Tracking_ID
        tracking_id_field_id = None
        for field_def in root.findall(".//FieldDefinition"):
            if field_def.attrib.get("alias") == "Loss_Event_ID":
                tracking_id_field_id = field_def.attrib.get("id")
                break

        if not tracking_id_field_id:
            print(f"⚠️ Nenhum Tracking_ID encontrado no arquivo {file_name}. Pulando...")
            continue

        for record in root.findall(".//Record"):
            record_data = {}
            tracking_id = None

            for field in record.findall(".//Field"):
                field_id = field.attrib.get("id")
                field_value = extract_text_from_field(field)

                for file_name, mapping in field_mappings.items():
                    if field_id in mapping.values():  
                        field_name = list(mapping.keys())[list(mapping.values()).index(field_id)]
                        record_data[field_name] = field_value

                        if field_name == "Loss_Event_ID":  # 📌 Se for o campo Tracking_ID, armazenamos
                            tracking_id = field_value

            # Garantir que os campos `naturezaContingencia` e `tipoAvaliacao` estejam sempre no dicionário
            # e garantir que idEvento receba o Tracking_ID corretamente
            record_data["idEvento"] = tracking_id if tracking_id else "N/A"
            record_data["naturezaContingencia"] = record_data.get("naturezaContingencia", "N/A")
            record_data["tipoAvaliacao"] = record_data.get("tipoAvaliacao", "N/A")
            # record_data["categoriaNivel2"] = record_data.get("Classificar_Evento", "N/A")
            classificar_evento = record_data.get("Classificar_Evento", "N/A")
            categorias = classificar_evento.split(":")  

            record_data["categoriaNivel1"] = categorias[0] if len(categorias) > 0 else "N/A"
            record_data["categoriaNivel2"] = categorias[1] if len(categorias) > 1 else "N/A"
            
            records_data.append(record_data)


    return field_mappings, records_data

def substituir_categoria_n1_consol(xml_string):
    """
    Substitui os valores numéricos de <categoriaNivel1Consol> pelos seus equivalentes textuais
    conforme o dicionário 'anexo1_categoria_n1'.
    """
    def substituir_match(match):
        valor_numerico = match.group(1)  # Captura o valor da tag categoriaNivel1Consol
        valor_texto = anexo1_categoria_n1.get(valor_numerico, "Desconhecido")  # Busca no dicionário
        return f'categoriaNivel1Consol="{valor_texto}"'  # Retorna a substituição correta

    # Regex para encontrar o atributo categoriaNivel1Consol dentro do XML
    padrao_regex = r'categoriaNivel1Consol="(\d+)"'

    # Substituir os valores no XML
    xml_modificado = re.sub(padrao_regex, substituir_match, xml_string)

    return xml_modificado

def create_cadoc_template(records_data, eventos_consolidados):
    """
    Cria o XML final no formato CADOC 5050 consolidando os dados.
    """
    print("Gerando XML no formato CADOC 5050...")

    # Criar o elemento raiz <documento>
    documento = ET.Element("documento", {"codigoDocumento": "5050", "dataBase": "2025-01",
                                          "codigoConglomerado": "C0099999", "tipoRemessa": "I", "cnpj": "99999999",
                                          "opcaoPorProvisaoAcumulada": "N"})

    # Criar os subelementos principais
    eventos_individualizados_xml = ET.SubElement(documento, "eventosIndividualizados")
    eventos_consolidados_xml = ET.SubElement(documento, "eventosConsolidados")

    # Lista de campos permitidos no XML final
    campos_permitidos = [
        "idEvento", "categoriaNivel1" , "categoriaNivel2", "valorTotalRisco",
        "dataOcorrencia", "totalPerdaEfetiva", "totalRecuperado",
        "codSistemaOrigem", "codigoEventoOrigem", "idBacen",
        "naturezaContingencia", "tipoAvaliacao"
    ]

    # Processando eventos individualizados
    for record in records_data:
        atributos = {campo: record[campo] for campo in campos_permitidos if campo in record}  # 🔥 Filtramos os campos permitidos
        # print("Atributos filtrados:", atributos)  # Debug
        # Dentro do loop que processa os registros do XML do Archer:
        texto_unidade_negocio = record.get("catUnidadeNegocio", "")  # Obtém o texto da unidade do XML do Archer
        codigo_unidade_negocio = converter_unidade_negocio(texto_unidade_negocio)  # Converte para número

        atributos["unidadeNegocio"] = codigo_unidade_negocio  # Adiciona ao XML final

        ET.SubElement(eventos_individualizados_xml, "evento", atributos)

    # Adicionando eventos consolidados
    # print(f"Eventos Consolidados Detalhes: {eventos_consolidados}")  # Debug

    for categoria, dados in eventos_consolidados.items():
        classificar_evento = record.get("Classificar_Evento", "N/A")
        categorias = classificar_evento.split(":") # Separador de valores da lista nested
        categoria_nivel_1_consol = mapear_categoria_n1_consolidado(categoria)
        
        # if "categoriaNivel1" not in record:
        #     classificar_evento = record.get("Classificar_Evento", "N/A")
        #     categorias = classificar_evento.split(":") # Separador de valores da lista nested
        #     record["categoriaNivel1"] = categorias[0] if len(categorias) > 0 else "N/A"
            
        categoria_nivel_1_consol = mapear_categoria_n1_consolidado(categoria)  # Mapeia corretamente a categoria consolidada

        # Consolidação dos atributos
        atributos_consolidados = {
            "categoriaNivel1Consol": categoria_nivel_1_consol,
            "numEventosTotalConsol": str(dados["numEventosTotalConsol"]),
            "numEventosSemestreConsol": str(dados["numEventosSemestreConsol"]),
            "perdaEfetivaTotalConsol": formatar_valor_decimal(dados["perdaEfetivaTotalConsol"])[0],
            "perdaEfetivaSemestreConsol": formatar_valor_decimal(dados["perdaEfetivaSemestreConsol"])[0],
            "provisaoTotalConsol": formatar_valor_decimal(dados["provisaoTotalConsol"])[0],
            "provisaoSemestreConsol": formatar_valor_decimal(dados["provisaoSemestreConsol"])[0]
        }

        print(f"✅ Evento Consolidado Adicionado: {atributos_consolidados}")  # Debug para verificar saída correta
        ET.SubElement(eventos_consolidados_xml, "eventoConsolidado", atributos_consolidados)

    # Criando o novo bloco <sistemasOrigem> abaixo de </eventosConsolidados>
    sistemas_origem_xml = ET.SubElement(documento, "sistemasOrigem")
    sistema = ET.SubElement(sistemas_origem_xml, "sistema", {
        "codigoSistema": "Archer01",
        "nomeSistema": "Gerenciamento de Riscos Integrados"
    })

    contas_sub_internos_xml = ET.SubElement(documento, "contasSubtitulosInternos")
    conta = ET.SubElement(contas_sub_internos_xml, "conta", {
        "codigoConta": "10000000001",
        "nomeConta": "Conta1"
    })

    # Converter o XML para string formatada
    xml_string = ET.tostring(documento, encoding="utf-8").decode("utf-8")
    converted_xml = parseString(xml_string).toprettyxml(indent="  ")
    converted_xml = '<?xml version="1.0" encoding="utf-8"?>\n' + "\n".join(converted_xml.split("\n")[1:])

    # Gerar o nome do arquivo com data atual
    data_atual = datetime.now().strftime("%Y-%m-%d")
    final_filename = f"cadoc-exported-{data_atual}.xml"

    with open(final_filename, "w", encoding="utf-8") as file:
        file.write(converted_xml)

    print(f"✅ XML criado e salvo com sucesso como '{final_filename}'!")


# Execução principal
if __name__ == "__main__":
    from main import xml_folder_path
    field_mappings, records_data = process_all_xmls(xml_folder_path)
    filtered_records, eventos_consolidados = filter_valid_records(records_data)
    create_cadoc_template(filtered_records, eventos_consolidados)

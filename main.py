#----------------------------------------------------------------#
#                                                                #
#     Desc: Script para converter arquivos XML                   #
#     para o padrão elencado pelo BACEN CADOC 5050               #                                                  
#     Author: Samuel Pimenta                                     #                                        
#     Company: Athena Soluções Inteligentes                      #
#                                                                #
#----------------------------------------------------------------#

# RUN
# pyinstaller --name=Archer_to_5050 --onefile --add-data "src;src" --hidden-import=xml.etree.ElementTree --hidden-import=xml.dom --hidden-import=xml.dom.minidom main.py

import logging
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from archer_formatter.read_xml_file import read_file
from archer_formatter.convert_to_5050 import process_all_xmls, create_cadoc_template
from archer_formatter.logger import init_logger
from archer_formatter.utils import formatar_valor_decimal, format_date
from archer_formatter.anexos import mapear_categoria_n1, mapear_categoria_n2
from archer_formatter.validation import filter_valid_records
from archer_formatter.hash_file import calculate_hash

class Taskflow:
    def __init__(self, xml_path):
        self.xml_path = xml_path
        self.logger = init_logger()  # Inicialização do logger

    def execute(self):
        self.logger.info("🔎 Iniciando validação dos registros...")

        # Processamento do XML...
        self.logger.info("✅ Processamento finalizado com sucesso!")
        
        try:
            # Fluxo de execução
            # 1. Ler arquivos XML
            self.logger.info(f"📂 Lendo arquivos XML da pasta: {self.xml_path}...")
            xml_files_data = read_file(self.xml_path)

            if not xml_files_data:
                self.logger.error("❌ Houve uma falha no processamento do XML ou nenhum XML foi encontrado.")
                return

            self.logger.info("✅ O arquivo XML foi processado com sucesso!")

            # 2. Processar os registros do XML
            self.logger.info("📊 Extraindo registros do XML...")
            field_mappings, records_data = process_all_xmls(self.xml_path)

            if not records_data:
                self.logger.warning("⚠️ Nenhum registro encontrado no XML.")
                return
            
            self.logger.info(f"🔎 Extraídos {len(records_data)} registros do arquivo XML.")

            # Remover registros que não contenham todos os campos preenchidos
            # Campos obrigatórios
            complete_records = []
            required_fields = ["idEvento", "categoriaNivel1", "categoriaNivel2", "valorTotalRisco","dataOcorrencia", "totalPerdaEfetiva", "totalRecuperado", "codSistemaOrigem", "codigoEventoOrigem", "idBacen" ]  # Campos obrigatórios

            for record in records_data:
                if all(record.get(field, "").strip() for field in required_fields):
                    complete_records.append(record)
                else:
                    self.logger.warning(f"⚠️ Registro {record.get('idEvento', 'N/A')} descartado por conter campos vazios.")

            # Agora, aplicar a filtragem do valor do risco APENAS nos registros completos
            # 3. Filtrar os registros
            filtered_records = []
            for record in complete_records:
                valor_risco_str = str(record.get("valorTotalRisco", "0")).strip()

                if not valor_risco_str:
                    self.logger.warning(f"⚠️ Registro {record.get('idEvento', 'N/A')} descartado por não conter 'valorTotalRisco' preenchido.")
                    continue  # Pula para o próximo registro

                try:
                    # Converter e obter os dois valores para 'valorTotalRisco'
                    valor_formatado, valor_risco = formatar_valor_decimal(record.get("valorTotalRisco", "0").strip())
                    # Converter e obter os dois valores para 'totalPerdaEfetiva'
                    perda_formatada, perda_float = formatar_valor_decimal(record.get("totalPerdaEfetiva", "0").strip())
                    # Converter e obter os dois valores para 'totalRecuperado'
                    recuperado_formatado, recuperado_float = formatar_valor_decimal(record.get("totalRecuperado", "0").strip())
                    dataOcorrencia_formatada = format_date(record.get("dataOcorrencia", "0").strip())
                    # Mapear categoria textual para código numérico
                    # categoria_texto = record.get("categoriaNivel1", "").strip()
                    if "Classificar_Evento" in record:
                        categorias = record["Classificar_Evento"].split(":")
                        record["categoriaNivel1"] = categorias[0] if len(categorias) > 0 else "N/A"
                        record["categoriaNivel2"] = categorias[1] if len(categorias) > 1 else "N/A"
                    
                    categoria1_texto = record.get("categoriaNivel1", "").strip()
                    categoria1_numerica = mapear_categoria_n1(categoria1_texto)

                    categoria2_texto = record.get("categoriaNivel2", "").strip()
                    categoria2_numerica = mapear_categoria_n2(categoria2_texto)

                    if categoria2_numerica == "0":
                        print(f"⚠️ AVISO: CategoriaNivel2 '{categoria2_texto}' não encontrada no dicionário!")

                    if valor_risco > 1000000:  # Comparação feita com o FLOAT
                        # Insert STRING on XML
                        record["valorTotalRisco"] = valor_formatado #
                        record["totalPerdaEfetiva"] = perda_formatada  # 
                        record["totalRecuperado"] = recuperado_formatado #
                        record["dataOcorrencia"] = dataOcorrencia_formatada #
                        record["categoriaNivel1"] = categoria1_numerica #
                        record["categoriaNivel2"] = categoria2_numerica #

                        filtered_records.append(record)
                        self.logger.info(f"✅ Registro {record.get('idEvento', 'N/A')} incluído no XML (valorTotalRisco: {record['valorTotalRisco']}, totalPerdaEfetiva: {record['totalPerdaEfetiva']})")

                    else:
                        self.logger.warning(f"⚠️ Registro {record.get('idEvento', 'N/A')} descartado (valorTotalRisco: {valor_risco})")

                except ValueError:
                    self.error(f"❌ Erro ao converter valores para número no registro {record.get('idEvento', 'N/A')}")


            if not filtered_records:
                self.logger.warning("⚠️ Nenhum registro válido encontrado após a validação. O XML não será gerado.")
                return

            # Gerar o XML somente com os registros completos e válidos
            self.logger.info("📝 Gerando o XML final...")
            # Chamando a validação e recebendo os dois retornos (eventos individuais e eventos consolidados)
            # 4. Validar os registros
            filtered_records, eventos_consolidados = filter_valid_records(records_data)

            # 5. Criar o XML final
            create_cadoc_template(filtered_records, eventos_consolidados)


        except Exception as e:
            self.logger.error(f"❌ Ocorreu um erro durante a execução: {e}")
            raise e


# Definir o caminho do XML APENAS UMA VEZ
xml_folder_path = "../Data_Feed/5050"

# Executar o fluxo de processamento
if __name__ == "__main__":
    flow = Taskflow(xml_folder_path)
    flow.execute()
    
    # Calcular o hash do arquivo gerado
    data_atual = datetime.now().strftime("%Y-%m-%d")
    final_filename = f"cadoc-exported-{data_atual}.xml"
    file_hash = calculate_hash(final_filename)
    print(f"\n🔍 Hash do arquivo gerado ({final_filename}):")
    print(f"SHA256: {file_hash}")
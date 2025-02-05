from archer_formatter.convert_to_5050 import process_all_xmls, records_data
from archer_formatter.logger import init_logger

logger = init_logger() # Init logger

filtered_records = []

def filter_valid_records(records_data):
    """Validate if the records correspond to the CADOC 5050 rules"""
    
    if not records_data:
        logger.warning("No records found in the XML files.")
        return filtered_records
    
    for record in records_data:
        try:
            valor_risco = float(str(record.get("N_Risco", "0")).replace(",", "").strip())
            
            if valor_risco > 1000000:
                filtered_records.append(record)
                logger.debug(f"Registro {record.get('idEvento', 'N/A')} - N_Risco convertido: {valor_risco}")
            else:
                logger.warning(f"⚠️ Registro {record.get('idEvento', 'N/A')} descartado (N_Risco: {valor_risco})")
        except ValueError:
            logger.error(f"Erro ao converter N_Risco para número no registro {record.get('idEvento', 'N/A')}")
    return filtered_records  # Retorna apenas registros válidos

# def validation_rules(records_data):
#     """Validate if the records correspond to the CADOC 5050 rules"""  
#     if records_data:
#         print("Registros encontrados")
#         logger.info("Registros encontrados")
#         for record in records_data:
#             valor_risco = record.get("N_Risco")  # Evita KeyError
            
#             if valor_risco is None:
#                 print(f"⚠️ Aviso: Registro {record.get('idEvento', 'N/A')} não contém 'N_Risco'.")
#                 msg = f"Registro {record.get('idEvento', 'N/A')} não contém 'N_Risco'."
#                 logger.warning(msg)
#                 continue  # Pula para o próximo registro

#             try:
#                 # 🔹 Converte para número corretamente, removendo espaços e caracteres ocultos
#                 valor_risco = float(str(valor_risco).replace(",", "").strip())

#                 # 🔹 Depuração: Mostrar valores antes da comparação
#                 msg = f"Registro {record.get('idEvento', 'N/A')} - N_Risco convertido: {valor_risco}"
#                 print(f"Registro {record.get('idEvento', 'N/A')} - N_Risco convertido: {valor_risco}")
#                 logger.debug(msg)

#                 if valor_risco < 1000000:
#                     msg = f"Montante menor do que 1000000 para o registro {record.get('idEvento', 'N/A')}"
#                     print(f"Montante menor do que 1000000 para o registro {record.get('idEvento', 'N/A')}")
#                     logger.debug(msg)
#                 elif valor_risco == 1000000:
#                     msg = f"Exatos 1000000 para o registro {record.get('idEvento', 'N/A')}"
#                     print(f"⚠️ Exatos 1000000 para o registro {record.get('idEvento', 'N/A')}")
#                     logger.debug(msg)
#                 else:
#                     msg = f"Montante maior do que 1000000 para o registro {record.get('idEvento', 'N/A')}"
#                     print(f"⚠️ Montante maior do que 1000000 para o registro {record.get('idEvento', 'N/A')}")
#                     logger.debug(msg)
#             except ValueError:
#                 print(f"⚠️ Erro: O campo 'N_Risco' do registro {record.get('idEvento', 'N/A')} não é um número válido: {record['N_Risco']}")
#                 logger.error(f"O campo 'N_Risco' do registro {record.get('idEvento', 'N/A')} não é um número válido: {record['N_Risco']}")  
#     else:           
#         print("Nenhum registro encontrado")
#         logger.error("Nenhum registro encontrado")

def convert_to_num(value):
    try:
        value = float(value.replace(",", "").strip())
        return value
    except ValueError:
        return 0
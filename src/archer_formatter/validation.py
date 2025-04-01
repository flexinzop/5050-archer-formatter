from archer_formatter.logger import init_logger
from archer_formatter.utils import formatar_valor_decimal
from archer_formatter.anexos import unidade_de_negocio

logger = init_logger()  # Init logger

def filter_valid_records(records_data):
    """
    Valida e filtra os registros conforme as regras do BACEN.
    - Remove registros incompletos.
    - Converte 'valorTotalRisco' para o formato decimal correto.
    """

    filtered_records = []
    consolidados = {}
    required_fields = ["idEvento", "valorTotalRisco", "categoriaNivel1", "categoriaNivel2", "naturezaContingencia", "tipoAvaliacao", "dataOcorrencia",
                       "totalPerdaEfetiva", "totalRecuperado", "codSistemaOrigem", "codigoEventoOrigem", "idBacen"]

    if not records_data:
        logger.warning("⚠️ Nenhum registro encontrado para validação.")
        return filtered_records, consolidados

    logger.info("🔎 Iniciando validação dos registros...")

    for record in records_data:
        # Verificar se todos os campos obrigatórios estão preenchidos
        missing_fields = [field for field in required_fields if not record.get(field)]
        
        if missing_fields:
            logger.warning(f"⚠️ Registro {record.get('idEvento', 'N/A')} descartado. Campos ausentes: {missing_fields}")
            continue  # Ignorar registro incompleto

        # Converter e obter os valores numéricos formatados
        valor_formatado, valor_risco = formatar_valor_decimal(record.get("valorTotalRisco", "0").strip())
        perda_formatada, perda_float = formatar_valor_decimal(record.get("totalPerdaEfetiva", "0").strip())

        if valor_risco >= 1000000:  # Eventos individuais
            record["valorTotalRisco"] = valor_formatado
            record["totalPerdaEfetiva"] = perda_formatada
            filtered_records.append(record)
            logger.info(f"✅ Registro {record.get('idEvento', 'N/A')} incluído nos eventos individualizados.")
        
        else:  # Eventos a serem consolidados
            categoria = record.get("categoriaNivel1", "0")  # Pega a categoria ou define "0" se não existir
            perda_efetiva = perda_float
            recuperado = float(record.get("totalRecuperado", "0") or 0)  # Garantir conversão correta
            provisao = float(record.get("provisaoTotalConsol", "0") or 0)  # Garantir conversão correta

            if categoria not in consolidados:
                consolidados[categoria] = {
                    "categoriaNivel1Consol": categoria,
                    "numEventosTotalConsol": 0,
                    "numEventosSemestreConsol": 0,  # Pode ser atualizado com uma regra específica
                    "perdaEfetivaTotalConsol": 0,
                    "perdaEfetivaSemestreConsol": 0,  # Pode ser atualizado com uma regra específica
                    "provisaoTotalConsol": 0,
                    "provisaoSemestreConsol": 0  # Pode ser atualizado com uma regra específica
                }

            # Atualizar valores agregados
            consolidados[categoria]["numEventosTotalConsol"] += 1
            consolidados[categoria]["perdaEfetivaTotalConsol"] += perda_efetiva
            consolidados[categoria]["provisaoTotalConsol"] += provisao
            consolidados[categoria]["totalRecuperado"] = recuperado

            logger.info(f"🔄 Evento consolidado na categoria {categoria} (Total: {consolidados[categoria]['numEventosTotalConsol']})")

    logger.info(f"🔎 Validação concluída. Registros individuais: {len(filtered_records)}, Eventos Consolidados: {len(consolidados)}")

    return filtered_records, consolidados  # Retorna os registros individuais e os consolidados

def converter_unidade_negocio(texto_unidade):
    """Converte a unidade de negócio do Archer (texto) para seu código numérico no dicionário."""
    if not texto_unidade:
        return "N/A"  # Retorna "N/A" se estiver vazio

    # 🔎 Faz a correspondência baseada nos primeiros 12 caracteres (igual categoriaNivel1)
    for numero, nome in unidade_de_negocio.items():
        if texto_unidade[:12].strip().lower() == nome[:12].strip().lower():
            return numero  # Retorna o código numérico associado
    
    return "0"  # Se não encontrar correspondência, retorna 0
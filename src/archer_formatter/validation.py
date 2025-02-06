from archer_formatter.logger import init_logger

logger = init_logger()  # Init logger

def filter_valid_records(records_data):
    """
    Valida e filtra os registros conforme as regras do BACEN.
    - Remove registros incompletos.
    - Converte 'valorTotalRisco' para o formato decimal correto.
    """

    filtered_records = []
    required_fields = ["idEvento", "valorTotalRisco", "categoriaNivel1", "naturezaContingencia", "tipoAvaliacao", "dataOcorrencia", "unidadeNegocio",
                       "totalPerdaEfetiva", "totalRecuperado", "codSistemaOrigem", "codigoEventoOrigem", "idBacen"]

    if not records_data:
        logger.warning("⚠️ Nenhum registro encontrado para validação.")
        return filtered_records  # Retorna lista vazia

    logger.info("🔎 Iniciando validação dos registros...")

    for record in records_data:
        # 📌 Verificar se todos os campos obrigatórios estão preenchidos
        missing_fields = [field for field in required_fields if not record.get(field)]
        
        if missing_fields:
            logger.warning(f"⚠️ Registro {record.get('idEvento', 'N/A')} descartado. Campos ausentes: {missing_fields}")
            continue  # Ignorar registro incompleto

    logger.info(f"🔎 Validação concluída. Registros válidos: {len(filtered_records)}")

    return filtered_records  # Retorna apenas registros válidos
import logging

import logging

def init_logger():
    """Inicializa um logger global para evitar logs duplicados."""
    logger = logging.getLogger("archer_formatter")

    # 🔍 Evita múltiplos handlers no logger
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        # Criar um handler para salvar logs em um arquivo
        handler = logging.FileHandler("archer_5050_formatter.log", mode="w", encoding="utf-8")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Adicionar handler apenas se ainda não existir
        logger.addHandler(handler)
    
    return logger

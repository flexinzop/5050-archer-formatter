anexo1_categoria_n1 = {"1": "Fraudes internas",
                       "2": "Fraudes externas",
                       "3": "Demandas trabalhistas e segurança deficiente do local de trabalho",
                       "4": "Práticas inadequadas relativas a clientes, produtos e serviços",
                       "5": "Danos a ativos físicos próprios ou em uso pela instituição",
                       "6": "Situações que acarretem a interrupção das atividades da instituição",
                       "7": "Falhas em sistemas, processos ou infraestrutura de tecnologia da informação",
                       "8": "Falhas na execução, no cumprimento de prazos ou no gerenciamento das atividades da instituição"
}


anexo2_categoria_n2 = {"11":"Atividade não autorizada",
                       "12":"Roubo e fraude (origem interna)",
                       "21":"Roubo e fraude (origem externa)",
                       "22":"Segurança de sistemas",
                       "31":"Relações de trabalho",
                       "32":"Segurança do local de trabalho",
                        "33":"Diversidade e discriminação",
                        "41":"Adequação de produto a cliente, divulgação de informações sobre produtos e serviços, desrespeito ao dever fiduciário",
                        "42":"Práticas impróprias de negócios e em mercados",
                        "43":"Falhas no produto",
                        "44":"Seleção, patrocínio e exposição",
                        "45":"Atividades de assessoramento",
                        "51":"Desastres e outros eventos",
                        "61":"Interrupção de atividades",
                        "71":"Falhas em sistemas, processos ou infraestrutura de TI",
                        "81":"Captura, execução e manutenção de transações",
                        "82":"Monitoramento e reporte",
                        "83":"Aquisição de clientes e documentação",
                        "84":"Gestão de contas correntes e de não correntistas",
                        "85":"Contrapartes em transações","86":"Representantes e fornecedores"
}

unidade_de_negocio = {"1":"Varejo",
                    "2":"Comercial",
                    "3":"Finanças corporativas",
                    "4":"Negociação e vendas",
                    "5":"Pagamentos e liquidações",
                    "6":"Serviços de agente financeiro",
                    "7":"Administração de ativos",
                    "8":"Corretagem de varejo"
}

def mapear_categoria_n1(valor_texto):
    """
    Converte um valor textual para seu código numérico baseado no dicionário de categorias.
    - Agora compara apenas os **12 primeiros caracteres** para encontrar a correspondência.
    
    Exemplo: 
      - "Fraudes externas - algo mais" → "2"
    
    Se o valor não for encontrado, retorna "0" e registra um aviso.
    """
    valor_texto = valor_texto.lower().strip()[:16]  # Pega só os 12 primeiros caracteres

    for codigo, descricao in anexo1_categoria_n1.items():
        if descricao.lower().strip()[:16] == valor_texto:  # Comparação parcial
            return codigo

    print(f"⚠️ AVISO: Categoria '{valor_texto}' não encontrada no dicionário! Retornando '0'.")
    return "0"  # Código padrão se não encontrar

def mapear_categoria_n2(valor_texto):
    """
    Converte um valor textual de categoriaNivel2 para seu código numérico baseado no dicionário de categorias.
    - Faz a comparação apenas nos **12 primeiros caracteres** para encontrar a correspondência.

    Exemplo: 
      - "Captura, execução e manutenção de transações" → "81"
    
    Se o valor não for encontrado, retorna "0" e registra um aviso.
    """
    valor_texto = valor_texto.lower().strip()[:12]  # Pega só os 12 primeiros caracteres

    for codigo, descricao in anexo2_categoria_n2.items():
        if descricao.lower().strip()[:12] == valor_texto:  # Comparação parcial
            return codigo

    print(f"⚠️ AVISO: Categoria '{valor_texto}' não encontrada no dicionário! Retornando '0'.")
    return "0"  # Código padrão se não encontrar


def mapear_categoria_n1_consolidado(valor_texto):
    """Mapeia a descrição da categoria para seu código numérico apenas para eventos consolidados."""
    if not valor_texto:
        return "0"

    valor_texto = valor_texto.lower().strip()[:12]  # Normaliza e pega os primeiros 12 caracteres

    for codigo, descricao in anexo1_categoria_n1.items():
        if descricao.lower().strip()[:12] == valor_texto:
            return codigo  # Retorna o ID numérico correto

    print(f"⚠️ AVISO: Categoria '{valor_texto}' não encontrada para consolidação! Retornando '0'.")
    return "0"



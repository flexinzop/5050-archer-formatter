def formatar_valor_decimal(valor):
    """
    Converte um número para o formato decimal esperado no XML.
    Retorna:
    - Uma string formatada para o XML ("1200000.00")
    - Um float para operações matemáticas (1200000.00)
    """
    if not isinstance(valor, (int, float, str)):
        raise ValueError("O valor deve ser um número inteiro, float ou string numérica.")

    try:
        # Converter para float
        valor_float = float(valor)

        # Formatar para string com duas casas decimais
        valor_formatado = f"{valor_float:.2f}"  # Exemplo: "1200000.00"

        return valor_formatado, valor_float  # Retorna a string e o float

    except ValueError:
        raise ValueError("O valor fornecido não pode ser convertido para número.")
    
def format_date(date):
    dia, mes, ano = date.split("/")
    return f"{ano}-{mes}-{dia}"

import xml.etree.ElementTree as ET

def parse_eventos_individualizados(root):
    """Processa os subelementos de 'eventosIndividualizados'."""
    eventos = []
    eventos_individualizados = root.find('eventosIndividualizados')
    if eventos_individualizados is not None:
        for evento in eventos_individualizados.findall('evento'):
            evento_data = {key: value for key, value in evento.attrib.items()}
            eventos.append(evento_data)
    return eventos

def parse_sistemas_origem(root):
    """Processa os subelementos de 'sistemasOrigem'."""
    sistemas = []
    sistemas_origem = root.find('sistemasOrigem')
    if sistemas_origem is not None:
        for sistema in sistemas_origem.findall('sistema'):
            sistema_data = {key: value for key, value in sistema.attrib.items()}
            sistemas.append(sistema_data)
    return sistemas
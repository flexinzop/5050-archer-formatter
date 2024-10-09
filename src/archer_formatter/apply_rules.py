# Apply rules to the DataFrame based on CADOC 5050

fields_list = ['codigoDocumento',
               'dataBase',
               'codigoConglomerado',
               'cnpj',
               'tipoRemessa',
               'opcaoPorProvisaoAcumulada',
               'idEvento',
               'categoriaNivel1',
               'totalPerdaEfetiva',
               'totalProvisao',
               'totalRecuperado',
               'fonteRecuperacao',
               'valorTotalRisco',
               'dataOcorrencia',
               'categoriaNivel1Consol',
               'numEventosTotalConsol',
               'perdaEfetivaTotalConsol',
               'codigoSistema',
               'nomeSistema',
               'codigoConta',
               'nomeConta']

def create_json_handler(df):
    df['JSON_handler'] = None
    pass
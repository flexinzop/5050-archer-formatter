import pandas as pd

mandatory_fields = ['codigoDocumento',
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

def check_mandatory_fields(df):
    for field in mandatory_fields:
        if field not in df.columns:
            print("\n ---------------------------- \n")
            print(f"Field {field} not found in file")
            print("\n ---------------------------- \n")

            return False
    return True

def check_empty_columns(df):
    empty_columns = df.columns[df.isnull().all()].tolist()

    if empty_columns:
        print(f'The following columns are empty: {empty_columns}')
        return True
    else:
        print('There are no empty columns in the file.')
        return False
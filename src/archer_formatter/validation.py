from archer_formatter.convert_to_5050 import process_all_xmls, records_data

def validation_rules(records_data):
    """Validate if the records correspond to the CADOC 5050 rules"""
    
    if records_data:
        print("Registros encontrados")
        for record in records_data:
            if record["categoriaNivel1"] <= 1000000:
                print("Montante maior do que: 1000000 para o registro" + record["idEvento"] + record)
            else:
                print("Categoria não")
    else:
        print("Nenhum registro encontrado")
        return
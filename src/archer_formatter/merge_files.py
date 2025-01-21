import pandas as pd

file_path = 'data/base.csv'

df = pd.read_csv(file_path)


def check_empty_columns(df):
    empty_columns = df.columns[df.isnull().all()].tolist()

    if empty_columns:
        print(f'The following columns are empty: {empty_columns}')
        return True
    else:
        print('There are no empty columns in the file.')
        return False
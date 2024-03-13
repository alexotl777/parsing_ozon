'''
Получение данных из json, сформированного парсером (phones_crawl.py)
Последующий подчсет количества каждого элемента и вывод распределения версий ОС по убыванию количества
Сохранение распределения в result_distribution.csv
'''
import json
import pandas as pd

def calculation_of_model_distribution(json_file='os_versions.json', result_file='result_distribution.csv') -> pd.DataFrame:
    '''
    get: 
    имя json-файла, с данными, вытянутыми парсером (phones_crawl.py);
    имя csv-файла для внесения данных распределения

    return: 
    pandas.DataFrame с получившимся распределением версий ОС
    '''

    # Чтение JSON файла
    with open(json_file, 'r') as file:
        json_data = file.read()

        # Преобразование JSON данных в словарь
        data = json.loads(json_data)

    # Преобразование JSON данных в DataFrame
    df = pd.DataFrame(data)

    # Распределение
    distribution = pd.DataFrame(df.value_counts())

    # Сохранение в .csv
    distribution.to_csv(result_file, index=True)

    print(distribution)

    return distribution

if __name__ == '__main__':
    calculation_of_model_distribution()

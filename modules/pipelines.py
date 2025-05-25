import csv
from modules.database import Repository
from modules.index import InvertedIndex
import time

def read_csv_data(data_path):
    data = {}
    with open(data_path, newline='\n', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for id, row in enumerate(reader):
            data[id+1] = row.get('message', '')
    return data

def create_index(data_path, index_path, database_path, encoding, create_db):
    data = read_csv_data(data_path)
    print('Data readed')

    if create_db:
        database = Repository(database_path)
        database.migrate()
        database.add(data)
        print('Database created')

    index = InvertedIndex(encoding)
    start = time.time()
    index.index(data)
    print(f'Documents indexed in {time.time() - start}')
    index.save(index_path)
    print('Index created')


def search(query, index_path, database_path, encoding, documents):
    if documents:
        database = Repository(database_path)
        print('Database loaded')

    index = InvertedIndex(encoding)
    index.load(index_path)
    print('Index loaded')
    result = index.search(query)
    print(f'Results obtained: got {len(result)} documents:')
    if documents:
        for id in result:
            dock = database.get(id)
            print(f'Document id: {id}, document:')
            print(dock)
    else:
        print(*result, sep=' ')

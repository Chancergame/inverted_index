import argparse
import os
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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', '-dp', type=str, help='Input data path')
    parser.add_argument('--create_db', '-cdb', default=True, action=argparse.BooleanOptionalAction, help='Create new document database')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    index_path = os.environ.get('INDEX_PATH')
    database_path = os.environ.get('DATABESE_PATH')
    encoding = os.environ.get('ENCODING')

    if not index_path:
        index_path = os.environ.get('DEFAULT_INDEX_PATH')
        print('Index file path not passed, using default')
    if not database_path:
        database_path = os.environ.get('DEFAULT_DATABESE_PATH')
        print('Database file path not passed, using default')
    if not encoding:
        encoding = os.environ.get('DEFAULT_ENCODING')
        print('Encoding not passed, using none')
        
    if not args.data_path:
        raise Exception('Should pass path to data file')
    
    create_index(args.data_path, index_path, database_path, encoding, args.create_db)
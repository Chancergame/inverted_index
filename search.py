import argparse
import os
from modules.database import Repository
from modules.index import InvertedIndex

def search(query, index_path, database_path, encoding, documents, top):
    if documents:
        database = Repository(database_path)
        print('Database loaded')

    index = InvertedIndex(encoding)
    index.load(index_path)
    print('Index loaded')
    result = index.search(query)
    print(f'Results obtained: got {len(result)} documents, top {top} documents:')
    result = result[:top]
    if documents:
        for id in result:
            dock = database.get(id)
            print(f'\nDocument id: {id}, document:')
            print(dock)
    else:
        print(*result, sep=' ')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--operation', '-o', choices=['create', 'search'], help='Which operation to proceed')
    parser.add_argument('--data_path', '-dp', type=str, help='Input data path')
    parser.add_argument('--create_db', '-cdb', default=True, action=argparse.BooleanOptionalAction, help='Create new document database')
    parser.add_argument('--query', '-q', type=str, help='Search query')
    parser.add_argument('--documents', '-d', default=False, action=argparse.BooleanOptionalAction, help='Print documents from database')
    parser.add_argument('--top', '-t', help='Now namy documents to show')
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
    if not args.top:
        args.top = int(os.environ.get('DEFAULT_TOP'))
        print('Top not passed, using default')
        
    if not args.query:
        raise Exception('Should pass query')

    search(args.query, index_path, database_path, encoding, args.documents, args.top)
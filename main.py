import argparse
import os
from modules.pipelines import create_index, search
from modules.constants import DEFAULT_DATABESE_PATH, DEFAULT_ENCODING, DEFAULT_INDEX_PATH, DEFAULT_TOP

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
        index_path = DEFAULT_INDEX_PATH
        print('Index file path not passed, using default')
    if not database_path:
        database_path = DEFAULT_DATABESE_PATH
        print('Database file path not passed, using default')
    if not encoding:
        encoding = DEFAULT_ENCODING
        print('Encoding not passed, using none')
    if not args.top:
        args.top = DEFAULT_TOP
        print('Top not passed, using default')
        
    if args.operation == 'create':
       
        if not args.data_path:
            raise Exception('Should pass path to data file')
        create_index(args.data_path, index_path, database_path, encoding, args.create_db)
    
    if args.operation == 'search':

        if not args.query:
            raise Exception('Should pass query')

        search(args.query, index_path, database_path, encoding, args.documents, args.top)
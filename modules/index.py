from modules.encoder import *
from modules.preprocess import preprocess
from modules.constants import DEFAULT_INDEX_PATH, ENCODERS
import numpy as np
import pickle
from pathlib import Path
from progress.bar import IncrementalBar
from collections import defaultdict

class InvertedIndex:
    
    def __init__(self, encoding):
        
        if encoding not in ENCODERS.keys():
            encoding = 'none'
        self.encoding = encoding
        self.encoder = ENCODERS[encoding]

        self.inverted_index = defaultdict(set)
        
        
    def load(self, path=DEFAULT_INDEX_PATH):
        path = f'{path}_{self.encoding}.pkl'
        file_path = Path(path)

        self.inverted_index = defaultdict(set)
        
        if file_path.is_file():
            with open(path, 'rb') as f:
                data = pickle.load(f)
                
                if data['encoding'] != self.encoding:
                    enc = data['encoding']
                    print(f'Encoding mismatch: passed {self.encoding}, loaded {enc}, using loaded')
                    self.encoding = enc
                    self.encoder = ENCODERS[enc]

                for term, docks in data['data'].items():
                    self.inverted_index[term] = self.encoder.decode(docks)
        else:
            print('Index with matching encoding does not exists')
            

    def save(self, path=DEFAULT_INDEX_PATH):
        path = f'{path}_{self.encoding}.pkl'
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)
        
        data = {}
        for term, docks in self.inverted_index.items():
            data[term] = self.encoder.encode(docks)

        with open(path, 'wb') as f:
            pickle.dump({
                'encoding': self.encoding,
                'data': data
            }, f)
    
    def index(self, corpse):
        bar = IncrementalBar('Indexing process:', max = len(corpse))
        for id, text in corpse.items():
            tokens = preprocess(text)
            
            for token in tokens:
                self.inverted_index[token].add(id)

            bar.next()
        bar.finish()

    def add(self, id, text):
        tokens = preprocess(text)
            
        for token in tokens:
            self.inverted_index[token].add(id)

    def search(self, query):
        tokens = preprocess(query)
        docks = set()
        
        if not tokens:
            return list(docks)
        
        if tokens[0] in self.inverted_index:
                docks = self.inverted_index[tokens[0]]

        for token in tokens[1:]:
            if token in self.inverted_index:
                docks &= self.inverted_index[token]
            else:
                return []

        return sorted(docks)

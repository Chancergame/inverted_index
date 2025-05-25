import unittest
import tempfile
import shutil
import time
from pathlib import Path
from modules.encoder import DeltaEncoder, GammaEncoder
from modules.index import InvertedIndex
from modules.preprocess import preprocess

class TestEncoders(unittest.TestCase):

    def test_gamma_encoder_roundtrip(self):
        data = {1, 2, 4, 8, 16}
        encoded = GammaEncoder.encode(data)
        decoded = GammaEncoder.decode(encoded)
        self.assertEqual(decoded, data)

    def test_delta_encoder_roundtrip(self):
        data = {1, 2, 4, 8, 16}
        encoded = DeltaEncoder.encode(data)
        decoded = DeltaEncoder.decode(encoded)
        self.assertEqual(decoded, data)

    def test_gamma_encoder_large_numbers(self):
        data = {12345, 67890}
        encoded = GammaEncoder.encode(data)
        decoded = GammaEncoder.decode(encoded)
        self.assertEqual(decoded, data)

    def test_delta_encoder_large_numbers(self):
        data = {12345, 67890}
        encoded = DeltaEncoder.encode(data)
        decoded = DeltaEncoder.decode(encoded)
        self.assertEqual(decoded, data)

class TestInvertedIndex(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.index_path = Path(self.test_dir) / 'test_index'
        self.documents = {
            1: 'Ректор СПбГУ объявил конкурс',
            2: 'МГУ опубликовал приказ ректора',
            3: 'СПбГУ и МГУ лучшие университеты'
        }

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_single_document_indexing(self):
        idx = InvertedIndex('none')
        idx.add(1, 'Тестовый документ')
        self.assertIn('тестовый', idx.inverted_index)

    def test_search_intersection(self):
        idx = InvertedIndex('none')
        idx.index(self.documents)
        results = idx.search('ректор СПбГУ')
        self.assertEqual(results, [1])

    def test_empty_search(self):
        idx = InvertedIndex('none')
        idx.index(self.documents)
        self.assertEqual(idx.search(''), [])

    def test_missing_term_search(self):
        idx = InvertedIndex('none')
        idx.index(self.documents)
        
        results = idx.search("Наруто")
        self.assertEqual(results, [])
    
    def test_partial_missing_term_search(self):
        idx = InvertedIndex('none')
        idx.index(self.documents)
        
        results = idx.search("ректор Саске")
        self.assertEqual(results, [])
    
    def test_keyword_presence(self):
        idx = InvertedIndex('gamma')
        idx.index(self.documents)
        
        self.assertIn('спбгу', idx.inverted_index)
        self.assertIn('мгу', idx.inverted_index)
        self.assertIn('ректор', idx.inverted_index)

    def test_encoding_persistence(self):
        idx = InvertedIndex('gamma')
        idx.index(self.documents)
        idx.save(self.index_path)
        
        new_idx = InvertedIndex('gamma')
        new_idx.load(self.index_path)
        self.assertEqual(new_idx.search('МГУ'), [2, 3])

    def test_encoding_size_comparison(self):
        idx_none = InvertedIndex('none')
        idx_gamma = InvertedIndex('gamma')
        
        idx_none.index(self.documents)
        idx_gamma.index(self.documents)
        
        idx_none.save(self.index_path)
        idx_gamma.save(self.index_path)
        
        size_none = Path(f'{self.index_path}_none.pkl').stat().st_size
        size_gamma = Path(f'{self.index_path}_gamma.pkl').stat().st_size
        self.assertLess(size_gamma, size_none)

class TestPerformance(unittest.TestCase):
    def test_indexing_speed(self):
        docs = {i: f'документ {i}' for i in range(1000)}
        idx = InvertedIndex('none')
        
        start = time.time()
        idx.index(docs)
        duration = time.time() - start
        
        self.assertLess(duration, 80)
    
    def test_search_speed_large_index(self):
        docs = {i: f"документ {i} СПбГУ МГУ" for i in range(1000)}
        docs.update({
            10001: "Ректор СПбГУ объявил новый конкурс",
            10002: "МГУ опубликовал приказ ректора"
        })
        idx = InvertedIndex('none')
        idx.index(docs)
        
        start = time.time()
        results = idx.search("ректор СПбГУ")
        search_time = time.time() - start
        
        self.assertEqual(results, [10001])
        self.assertLess(search_time, 0.5)


if __name__ == '__main__':
    unittest.main()
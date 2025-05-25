from modules.encoder import NoneEncoder, DeltaEncoder, GammaEncoder

DEFAULT_DATABESE_PATH = 'data/database.db'
DEFAULT_ENCODING = 'none'
DEFAULT_INDEX_PATH = 'data/index'
DEFAULT_TOP = 5

ENCODERS = {
    'none': NoneEncoder,
    'delta': DeltaEncoder,
    'gamma': GammaEncoder,
}
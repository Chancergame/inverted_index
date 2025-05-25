from modules.encoder import NoneEncoder, DeltaEncoder, GammaEncoder

DEFAULT_DATABESE_PATH = 'data/database.db'
DEFAULT_ENCODING = 'none'
DEFAULT_INDEX_PATH = 'data/index'

ENCODERS = {
    'none': NoneEncoder,
    'delta': DeltaEncoder,
    'gamma': GammaEncoder,
}
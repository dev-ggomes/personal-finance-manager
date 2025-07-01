import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Caminho absoluto para este ficheiro
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Banco SQLite dentro de data/ (fora do Git)
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'finances.db')

# Engine e sessão
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)
Session = sessionmaker(bind=engine)
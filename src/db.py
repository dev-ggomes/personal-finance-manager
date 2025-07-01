import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Caminho absoluto para a pasta src/
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 2. Sobe um nível e entra na pasta data/
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'finances.db')

# 3. Cria o engine que aponta para o ficheiro SQLite
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)

# 4. Sessões para ORM
Session = sessionmaker(bind=engine)
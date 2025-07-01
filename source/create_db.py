from source.db import engine
from source.models import Base

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print("Base de dados criada em data/finances.db")
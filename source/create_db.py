from db import engine
from models import Base

Base.metadata.create_all(engine)
print("Base de dados criada em data/finances.db")
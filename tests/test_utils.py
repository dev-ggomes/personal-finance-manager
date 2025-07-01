import pytest
from db import engine, Session
from models import Base, Transaction
from utils import add_transaction, get_transactions, update_transaction, delete_transaction
from datetime import date

@pytest.fixture(scope='module')
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_add_and_get(setup_db):
    session = Session()
    txn = add_transaction(session, date.today(), 'income', 'Teste', 100.0, 'Descrição')
    fetched = get_transactions(session)
    assert len(fetched) == 1
    assert fetched[0].id == txn.id


def test_update_and_delete(setup_db):
    session = Session()
    txn = add_transaction(session, date.today(), 'expense', 'Teste2', 50.0)
    updated = update_transaction(session, txn.id, amount=75.0)
    assert updated.amount == 75.0
    assert delete_transaction(session, txn.id) is True
    assert delete_transaction(session, 9999) is False
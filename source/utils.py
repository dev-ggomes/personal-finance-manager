from datetime import date as DateClass
from sqlalchemy.orm import Session as SessionType
from source.models import Transaction


def add_transaction(session: SessionType, date: DateClass, txn_type: str, category: str, amount: float, description: str = None) -> Transaction:
    txn = Transaction(date=date, type=txn_type, category=category, amount=amount, description=description)
    session.add(txn)
    session.commit()
    session.refresh(txn)
    return txn


def get_transactions(session: SessionType, start_date=None, end_date=None, category=None):
    query = session.query(Transaction)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    if category:
        query = query.filter(Transaction.category == category)
    return query.order_by(Transaction.date.desc()).all()


def update_transaction(session: SessionType, txn_id: int, **kwargs) -> Transaction:
    txn = session.query(Transaction).get(txn_id)
    if not txn:
        return None
    for key, val in kwargs.items():
        setattr(txn, key, val)
    session.commit()
    return txn


def delete_transaction(session: SessionType, txn_id: int) -> bool:
    txn = session.query(Transaction).get(txn_id)
    if not txn:
        return False
    session.delete(txn)
    session.commit()
    return True
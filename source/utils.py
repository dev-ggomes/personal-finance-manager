from datetime import date as DateClass
from sqlalchemy.orm import Session as SessionType
from source.models import Transaction
import io
import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime


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

def get_monthly_report(session):
    # carrega todas as transações para um DataFrame
    txns = session.query(Transaction).all()
    df = pd.DataFrame([{
        'date': t.date,
        'type': t.type,
        'amount': t.amount
    } for t in txns])
    if df.empty:
        return None

    df['date'] = pd.to_datetime(df['date'])

    # agrupa por ano-mês e tipo
    df['year_month'] = df['date'].dt.to_period('M').astype(str)
    pivot = df.pivot_table(
        index='year_month', 
        columns='type', 
        values='amount',
        aggfunc='sum', 
        fill_value=0
    )

    # desenha o gráfico
    fig, ax = plt.subplots()
    pivot.plot(kind='bar', ax=ax)
    ax.set_title('Receitas vs Despesas por Mês')
    ax.set_ylabel('€')
    fig.tight_layout()

    # converte a figura para base64
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    plt.close(fig)
    return img_b64
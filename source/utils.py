from datetime import date as DateClass
from sqlalchemy.orm import Session as SessionType
from source.models import Transaction
import io
import base64
import pandas as pd
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
    # 1) Vai buscar todas as transações
    txns = session.query(Transaction).all()

    # 2) Converte para DataFrame
    df = pd.DataFrame([{
        'date': t.date,
        'type': t.type,
        'amount': t.amount
    } for t in txns])
    if df.empty:
        return None
    
    # 3) Extrai ano-mês e agrupa
    df['yeart_month'] = df['date'].apply(lambda d: d.strftime('%Y-%m'))
    grouped = df.pivot_table(
        index='year_month',
        columns='type',
        values='amount',
        aggfunc='sum',
        fill_value=0
    )

    # 4) Gera gráfico de barras
    fig, ax = plt.subplots()
    grouped.plt(kind='bar', ax=ax)
    ax.set_title('Receitas vs Despesas por Mês')
    ax.set_ylabel('Valor (€)')
    ax.legend(title='Tipo')

    # 5) Converte figura para PNG embutido (base64)
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    plt.close(fig)
    return img_b64
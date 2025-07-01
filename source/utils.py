from datetime import date as DateClass
from sqlalchemy.orm import Session as SessionType
from source.models import Transaction, Category
import pandas as pd
import io, base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from source.models import Budget

# Transactions

def add_transaction(session: SessionType, date: DateClass, txn_type: str, category_id: int, amount: float, description: str = None) -> Transaction:
    txn = Transaction(date=date, type=txn_type, category_id=category_id, amount=amount, description=description)
    session.add(txn)
    session.commit()
    session.refresh(txn)
    return txn


def get_transactions(session: SessionType):
    return session.query(Transaction).order_by(Transaction.date.desc()).all()


def delete_transaction(session: SessionType, txn_id: int) -> bool:
    txn = session.query(Transaction).get(txn_id)
    if txn:
        session.delete(txn)
        session.commit()
        return True
    return False

# Categories

def add_category(session: SessionType, name: str) -> Category:
    cat = Category(name=name)
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


def get_categories(session: SessionType):
    return session.query(Category).order_by(Category.name).all()


def delete_category(session: SessionType, cat_id: int) -> bool:
    cat = session.query(Category).get(cat_id)
    if cat:
        session.delete(cat)
        session.commit()
        return True
    return False

# Monthly report (transactions only)

def get_monthly_report(session: SessionType, year_month: str = None) -> str:
    txns = get_transactions(session)
    df = pd.DataFrame([{'date': t.date, 'type': t.type, 'amount': t.amount} for t in txns])
    if df.empty:
        return None

    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.to_period('M').astype(str)
    if year_month:
        df = df[df['year_month'] == year_month]

    pivot = df.pivot_table(
        index='year_month',
        columns='type',
        values='amount',
        aggfunc='sum',
        fill_value=0
    )

    fig, ax = plt.subplots()
    pivot.plot(kind='bar', ax=ax, title='Receitas vs Despesas por Mês')
    ax.set_ylabel('Valor (€)')

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    plt.close(fig)
    return img_b64

def set_budget(session, category_id: int, year_month: str, limit: float) -> Budget:
    bud = session.query(Budget).filter_by(category_id=category_id, year_month=year_month).first()
    if bud:
        bud.limit = limit
    else:
        bud = Budget(category_id=category_id, year_month=year_month, limit=limit)
        session.add(bud)
    session.commit()
    return bud

def get_budgets(session):
    return session.query(Budget).order_by(Budget.year_month.desc()).all()

def delete_budget(session, bud_id: int) -> bool:
    bud = session.query(Budget).get(bud_id)
    if bud:
        session.delete(bud)
        session.commit()
        return True
    return False
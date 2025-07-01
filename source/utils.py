from datetime import date as DateClass
from sqlalchemy.orm import Session as SessionType
from source.models import Transaction, Category, Budget
import pandas as pd, io, base64, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

# Transações
def add_transaction(session: SessionType, date, txn_type, category_id, amount, description=None):
    txn = Transaction(date=date, type=txn_type, category_id=category_id, amount=amount, description=description)
    session.add(txn); session.commit(); session.refresh(txn); return txn

def get_transactions(session: SessionType):
    return session.query(Transaction).order_by(Transaction.date.desc()).all()

def delete_transaction(session: SessionType, txn_id: int):
    txn = session.query(Transaction).get(txn_id)
    if txn: session.delete(txn); session.commit(); return True
    return False

# Categorias
def add_category(session: SessionType, name: str):
    cat = Category(name=name)
    session.add(cat); session.commit(); session.refresh(cat); return cat

def get_categories(session: SessionType):
    return session.query(Category).order_by(Category.name).all()

def delete_category(session: SessionType, cat_id: int):
    cat = session.query(Category).get(cat_id)
    if cat: session.delete(cat); session.commit(); return True
    return False

# Orçamentos
def set_budget(session: SessionType, category_id: int, year_month: str, limit: float):
    bud = session.query(Budget).filter_by(category_id=category_id, year_month=year_month).first()
    if bud:
        bud.limit = limit
    else:
        bud = Budget(category_id=category_id, year_month=year_month, limit=limit)
        session.add(bud)
    session.commit()
    return bud

def get_budgets(session: SessionType):
    return session.query(Budget).order_by(Budget.year_month.desc()).all()

def delete_budget(session: SessionType, bud_id: int):
    bud = session.query(Budget).get(bud_id)
    if bud: session.delete(bud); session.commit(); return True
    return False

# Relatório mensal com orçamentos
def get_monthly_report(session: SessionType, year_month: str = None):
    txns = get_transactions(session)
    df = pd.DataFrame([{'date': t.date, 'category': t.category_rel.name, 'type': t.type, 'amount': t.amount} for t in txns])
    if df.empty: return None
    df['date']=pd.to_datetime(df['date']); df['ym']=df['date'].dt.to_period('M').astype(str)
    if year_month:
        df = df[df['ym']==year_month]
    pivot = df.pivot_table(index='category', columns='type', values='amount', aggfunc='sum', fill_value=0)
    # gráfico
    fig, ax = plt.subplots(); pivot.plot.bar(ax=ax); ax.set_title(f'Relatório {year_month or pivot.index.name}'); buf=io.BytesIO(); fig.savefig(buf,format='png'); buf.seek(0); img=base64.b64encode(buf.read()).decode(); plt.close(fig)
    # orçamentos
    budgets = session.query(Budget).filter(Budget.year_month==year_month).all() if year_month else get_budgets(session)
    return img, pivot, budgets
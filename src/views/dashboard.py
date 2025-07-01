from flask import Blueprint, render_template, request, redirect, url_for
from db import Session
from utils import add_transaction, get_transactions
from datetime import datetime

bp = Blueprint('dashboard', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    session = Session()
    if request.method == 'POST':
        # Formulário adiciona transação
        date_str = request.form['date']
        txn_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        add_transaction(
            session,
            txn_date,
            request.form['type'],
            request.form['category'],
            float(request.form['amount']),
            request.form['description']
        )
        return redirect(url_for('dashboard.index'))
    
    txns = get_transactions(session)
    return render_template('dashboard.html', transactions=txns)
from flask import Blueprint, render_template, request, redirect, url_for
from source.db import Session
from source.utils import add_transaction, get_transactions, delete_transaction, get_monthly_report, get_categories
from datetime import datetime

bp = Blueprint('dashboard', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    session = Session()
    cats=get_categories(session)
    if request.method == 'POST':
        date_str = request.form['date']
        txn_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        add_transaction(
            session,
            txn_date,
            request.form['type'],
            int(request.form['category_id']),
            float(request.form['amount']),
            request.form.get('description')
        )
        return redirect(url_for('dashboard.index'))

    txns = get_transactions(session)
    return render_template('dashboard.html', transactions=txns, categories=cats)

@bp.route('/delete/<int:txn_id>', methods=['POST'])
def delete(txn_id):
    session = Session()
    delete_transaction(session, txn_id)
    return redirect(url_for('dashboard.index'))

@bp.route('/report')
def report():
    session = Session()
    chart = get_monthly_report(session)
    return render_template('report.html', chart_data=chart)
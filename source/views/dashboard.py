from flask import Blueprint, render_template, request, redirect, url_for
from source.db import Session
from source.utils import add_transaction, get_transactions, get_monthly_report
from datetime import datetime

bp = Blueprint('dashboard', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    session = Session()
    if request.method == 'POST':
        date_str = request.form['date']
        txn_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        add_transaction(
            session,
            txn_date,
            request.form['type'],
            request.form['category'],
            float(request.form['amount']),
            request.form.get('description')
        )
        return redirect(url_for('dashboard.index'))

    txns = get_transactions(session)
    return render_template('dashboard.html', transactions=txns)

@bp.route('/report')
def report():
    session = Session()
    chart = get_monthly_report(session)
    return render_template('report.html', chart_data=chart)
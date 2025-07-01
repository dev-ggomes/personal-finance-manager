from flask import Blueprint, render_template, request, redirect, url_for
from source.db import Session
from source.utils import get_categories, get_budgets, set_budget, delete_budget

bp = Blueprint('budgets', __name__, url_prefix='/budgets')

@bp.route('/', methods=['GET','POST'])
def index():
    session=Session()
    cats=get_categories(session)
    if request.method=='POST':
        ym=request.form['year_month']; lim=float(request.form['limit']);
        set_budget(session, int(request.form['category_id']), ym, lim)
        return redirect(url_for('budgets.index'))
    budgets=get_budgets(session)
    return render_template('budgets.html', budgets=budgets, categories=cats)

@bp.route('/delete/<int:bud_id>', methods=['POST'])
def delete(bud_id):
    session=Session(); delete_budget(session,bud_id)
    return redirect(url_for('budgets.index'))
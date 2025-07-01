from flask import Blueprint, render_template, request, redirect, url_for
from source.db import Session
from source.utils import get_categories, add_category, delete_category

bp = Blueprint('categories', __name__, url_prefix='/categories')

@bp.route('/', methods=['GET', 'POST'])
def index():
    session=Session()
    if request.method=='POST':
        add_category(session, request.form['name'])
        return redirect(url_for('categories.index'))
    cats = get_categories(session)
    return render_template('categories.html', categories=cats)

@bp.route('/delete/<int:cat_id>', methods=['POST'])
def delete(cat_id):
    session=Session(); delete_category(session,cat_id)
    return redirect(url_for('categories.index'))
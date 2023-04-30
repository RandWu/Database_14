from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
import api.sql as sql
import imp, random, os, string
from werkzeug.utils import secure_filename
from flask import current_app
import utilities as u

UPLOAD_FOLDER = 'static/product'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
manager_path1 = r'manager.productManager'

manager = Blueprint('manager', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for(manager_path1))

@manager.route('/productManager', methods=['GET', 'POST'])
@login_required
def productManager():
    scholarship = sql.Scholarships()
    
    if request.method == 'GET' and current_user.role == 'user':
        flash('No permission')
        return redirect(url_for('index'))
        
    if 'delete' in request.values:
        scholarship_id = request.values.get('delete')
        if scholarship.is_omit_okay(scholarship_id):
            scholarship.omit_scholarships(scholarship_id)
        else:
            flash('failed')
    
    elif 'edit' in request.values:
        scholarship_id = request.values.get('edit')
        return redirect(url_for('manager.edit', pid=scholarship_id))
    
    scholarship_data = scholarships_to_display(scholarship)
    return render_template('productManager.html', book_data = scholarship_data, user=current_user.name)

def scholarships_to_display(scholarship: sql.Scholarships) -> list:
    fetch_data = scholarship.get_all_scholarship()
    if not fetch_data:
        return list()
    list_of_dict = [{
            '獎學金編號': i[0],
            '獎學金名稱': i[1],
            '獎學金等級': i[2],
            '獎學金頒發年分': i[3],
            '獎學金頒發單位': i[4]
        } for i in fetch_data]
    return list_of_dict

@manager.route('/add', methods=['GET', 'POST'])
def add():
    current = u.get_current_time().year
    scholarships = sql.Scholarships()

    if request.method == 'POST':
        name = request.values.get('name')
        if not u.check_input(name):
            flash("Invalid Name")
            return redirect(url_for(manager_path1))
        
        rank = request.values.get('rank')
        try:
            rank = int(rank)
        except ValueError:
            flash("Rank is not an number!")
            return redirect(url_for(manager_path1))
        if not u.check_number(rank, ranges=range(1,6)):
            flash("Rank out of range!")
            return redirect(url_for(manager_path1))
        
        year = request.values.get('year')
        try:
            year = int(year)
        except ValueError:
            flash("Year is not a number!")
            return redirect(url_for(manager_path1))
        if not u.check_number(year, range(1990, current + 1)):
            flash("Year out of range!")
            return redirect(url_for(manager_path1))

        issuer = request.values.get('issuer')
        if not u.check_input(issuer):
            flash("Invalid Name")
            return redirect(url_for(manager_path1))
        
        userinput = {
            "name": name,
            "rank": rank,
            "year": year,
            "issuer": issuer
        }

        scholarships.create_scholarship(userinput)

        return redirect(url_for(manager_path1))

    return render_template('productManager.html', current_year = current)

@manager.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    scholarship = sql.Scholarships()
    
    if request.method == 'GET' and current_user.role == 'user':
        flash('No permission')
        return redirect(url_for('bookstore'))

    if request.method == 'POST':
        name = request.values.get('name')
        if not u.check_input(name):
            flash("Invalid Name")
            return redirect(url_for(manager_path1))
        
        rank = request.values.get('rank')
        try:
            rank = int(rank)
        except ValueError:
            flash("Rank is not an number!")
            return redirect(url_for(manager_path1))
        if not u.check_number(rank, ranges=range(1,6)):
            flash("Rank out of range!")
            return redirect(url_for(manager_path1))
        
        year = request.values.get('year')
        try:
            year = int(year)
        except ValueError:
            flash("Year is not a number!")
            return redirect(url_for(manager_path1))
        if not u.check_number(year, range(1990, current + 1)):
            flash("Year out of range!")
            return redirect(url_for(manager_path1))

        issuer = request.values.get('issuer')
        if not u.check_input(issuer):
            flash("Invalid Name")
            return redirect(url_for(manager_path1))
        schid = int(request.values.get('pid'))

        userinput = {
            "id": schid,
            "name": name,
            "rank": rank,
            "year": year,
            "issuer": issuer
        }
        scholarship.update_scholarship(userinput)
        
        return redirect(url_for(manager_path1))

    else:
        i = scholarship.get_scholarship()
        one_scholarship = {
            '獎學金編號': i[0],
            '獎學金名稱': i[1],
            '獎學金等級': i[2],
            '獎學金頒發年分': i[3],
            '獎學金頒發單位': i[4]
        }
        return render_template('edit.html', data=one_scholarship)


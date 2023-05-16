import re
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
    
    if request.method == 'GET' and current_user.role == 'student':
        flash('No permission')
        return redirect(url_for('bookstore.bookstore'))
        
    if 'delete' in request.values:
        scholarship_id = request.values.get('delete')
        if scholarship.is_omit_okay(scholarship_id):
            scholarship.omit_scholarships(scholarship_id)
        else:
            flash('failed')
    
    elif 'edit' in request.values:
        scholarship_id = request.values.get('edit')
        return redirect(url_for('manager.edit', schid=scholarship_id))
    
    scholarship_data = scholarships_to_display(scholarship)
    
    if 'search' in request.values:
        query = request.form['search']
        regex = request.form.get('regex') == 'true'
        results = list()
        if regex and not u.is_pattern_valid(query):
            flash('Invalid Pattern')
        else:
            for scholarship in scholarship_data:
                for value in scholarship.values():
                    if regex:
                        if re.search(query, str(value)):
                            results.append(scholarship)
                            break
                    else:
                        if query in str(value):
                            results.append(scholarship)
                            break
            return render_template('productManager.html', book_data = results, user=current_user.username, current_year = u.get_current_time().year)
    
    return render_template('productManager.html', book_data = scholarship_data, user=current_user.username, current_year = u.get_current_time().year)

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
    current = u.get_current_time().year
    if request.method == 'GET' and current_user.role == 'student':
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
        schid = request.values.get('schid')

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
        schid = request.values.get('schid')
        i = scholarship.get_scholarship(schid)
        one_scholarship = {
            '獎學金編號': i[0],
            '獎學金名稱': i[1],
            '獎學金等級': i[2],
            '獎學金頒發年分': i[3],
            '獎學金頒發單位': i[4]
        }
        return render_template('edit.html', data=one_scholarship)

def sort_records(records):
    # Define status map
    status_map = {0: "Not determined yet", -1: "Rejected", 1: "Accepted"}

    # Sort records by STATUS, with 0 values first, then ascending order
    sorted_records = sorted(records, key=lambda x: (x['狀態'] == 0, x['狀態']))

    # Map status values to meaningful strings
    for record in sorted_records:
        record['狀態'] = status_map.get(record['狀態'], 'Unknown status')

    return sorted_records

@manager.route('/applyManager', methods=['GET', 'POST'])
@login_required
def applyManager():
    scholarships = sql.Scholarships()
    miscs = sql.MISC()
    # get all applied scholarship
    applied = miscs.get_applied_scholarships()
    if len(applied) == 0:
        flash("No scholarship")
        return redirect(url_for(manager_path1))
    display = [{
            '獎學金編號': str(i[0]),
            '學生ID': i[1],
            '申請日期': i[2],
            '狀態': i[3]
        } for i in applied]
    display = sort_records(display)
    if 'viewScholarship' in request.values:
        query = request.values.get('viewScholarship')
        return redirect(url_for('manager.view', cat = "sch", query=query))
    elif 'viewStudent' in request.values:
        query = request.values.get('viewStudent')
        return redirect(url_for('manager.view', cat = "stu", query=query))
    elif request.method == 'POST' and request.form['decision']:
        print(request.form)
        status = int(request.form['decision'])
        userinput = {
            'status': status,
            'schid': int(request.form['schid']),
            'studid': request.form['studid']
        }
        miscs.update_apply(userinput)
    return render_template('applyManager.html', rows=display)

@manager.route('/view', methods=['GET', 'POST'])
@login_required
def view():
    cat = request.values.get('cat')
    query = request.values.get('query')
    one = dict()
    if cat == "sch":
        scholarships = sql.Scholarships()
        scholarship = scholarships.get_scholarship(query)
        if scholarship:
            one = {
                '獎學金編號': scholarship[0],
                '獎學金名稱': scholarship[1],
                '獎學金等級': scholarship[2],
                '頒發年分': scholarship[3],
                '發放者': scholarship[4]
            }
    elif cat == "stu":
        students = sql.Students()
        student = students.get_student(query)[0]
        if student:
            one = {
                '學生編號': student[0],
                '學生名稱': student[1],
                '學生性別': student[2]
            }
    print(one)
    return render_template('view.html', onedict=one)
import utilities as u
from flask import Flask, request, template_rendered, Blueprint
from flask import url_for, redirect, flash
from flask import render_template
from flask_login import login_required, current_user
from datetime import datetime
from base64 import b64encode
from api.sql import Scholarships, Students, MISC

store = Blueprint('bookstore', __name__, template_folder='../templates')

@store.route('/', methods=['GET', 'POST'])
@login_required
def bookstore():
    student = Students()
    scholarships = Scholarships()
    # get the scholarships students applied
    applied = student.fetch_scholarships(current_user.get_id())
    # get all scholarships
    all_scholarships = scholarships.get_all_scholarship()
    display = u.scholarship_to_display(all_scholarships, applied)
    return render_template('bookstore.html',user=current_user.username, role = current_user.role, scholarships= display)

@store.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    user_id = current_user.get_id()
    students = Students()
    if "scholarship_id" in request.values:
        schid = request.form['scholarship_id']
    else:
        return redirect(url_for('bookstore.bookstore'))
    userinput = {
        'schid':schid,
        'studid': user_id,
        'applyDate': u.datetime_format(u.get_current_time())
    }
    students.apply_scholarship(userinput)
    return redirect(url_for('bookstore.bookstore'))
import imp
from flask import render_template, Blueprint, redirect, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import api.sql as sql
import utilities as u

api = Blueprint('api', __name__, template_folder='./templates')

login_manager = LoginManager(api)
login_manager.login_view = 'api.login'
login_manager.login_message = "請先登入"

register_path = r'api.register'
login_path = r'api.login'

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(userid):  
    user = User()
    student = sql.Students()
    user.id = userid
    data = student.get_role(userid)
    try:
        user.role = data[0]
        user.name = data[1]
    except IndexError:
        flash('Unknown exception')
        return redirect(url_for(login_path))
    return user

@api.route('/login', methods=['POST', 'GET'])
def login():
    student = sql.Students()
    
    if request.method == 'POST':
        account = request.form['account']
        # Check username with regex.
        if not u.check_input(account):
            flash("輸入不正確")
            return redirect(url_for(login_path))
        
        password = request.form['password']
        password = u.sha1_hash(password)
        credentials = student.get_student(account)

        try:
            hashed = credentials[1]
            user_id = credentials[3]
            role = credentials[2]

        except IndexError:
            flash('*沒有此帳號')
            return redirect(url_for(login_path))

        if(hashed == password):
            user = User()
            user.id = user_id
            login_user(user)

            if( role == 'user'):
                return redirect(url_for('bookstore.bookstore'))
            else:
                return redirect(url_for('manager.productManager'))
        
        else:
            flash('*密碼錯誤，請再試一次')
            return redirect(url_for(login_path))

    
    return render_template('login.html')

@api.route('/register', methods=['POST', 'GET'])
def register():
    student = sql.Students()
    
    if request.method == 'POST':
        user_account = request.form['account']
        # Check username with regex.
        if not u.check_input(user_account):
            flash("輸入不正確")
            return redirect(url_for(login_path))
        # Get existing student
        exist_account = student.get_all_student()
        # Check return value
        if "list" not in type(exist_account) or "tuple" not in type(exist_account):
            flash("Unknown exception")
            return redirect(url_for(register_path))
        # Get all Student name.
        account_list = [x[1] for x in exist_account]
        # set the birthday datetime
        try:
            formatted_date = u.datetime_format(u.str_to_datetime(str(request.form['date'])))
        except ValueError:
            flash("Unknown exception")
            return redirect(url_for(register_path))
        # Check the role and sex for value forgery attack
        if not (u.constraint("sex", request.form['sex']) and u.constraint("role", request.form['role'])):
            flash('Unknown exception')
            return redirect(url_for(register_path))
        if(user_account in account_list):
            flash('Falied!')
            return redirect(url_for(register_path))
        else:
            password = u.sha1_hash(request.form['password'])
            userinput = { 
                'name': user_account,
                'sex': request.form['sex'],
                'password':password, 
                'role':request.form['role'],
                'date': formatted_date
            }
            student.create_student(userinput)
            return redirect(url_for(login_path))

    return render_template('register.html')

@api.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
from flask import Blueprint , render_template,flash,request , redirect , url_for
from . models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user , login_required , logout_user , current_user

auth = Blueprint('auth',__name__)

@auth.route('/login', methods = ['GET','POST'] )
def login():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')


        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in Successfully!',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password',category='error')
        else:
            flash('User not found ' ,category='error')
            
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    return redirect(url_for('auth.login'))

@auth.route('/signup',  methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
        if user:
            flash('User already exist')

        if password1 != password2:
            flash('Both password doesn\'t match', category='error')
        elif "@" not in email:
            flash('Email doesn\'t contain @ character.',category='error')
        else:
            new_user = User(email = email , name = name, password = generate_password_hash(password1,method='sha256'))

            db.session.add(new_user)
            db.session.commit()


            flash('Account created successfully',category='success')
            return redirect(url_for('views.dashboard'))
    return render_template('signup.html', user = current_user)
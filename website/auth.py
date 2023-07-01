from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, create_app
from flask_login import login_user, login_required, logout_user, current_user
from email_validator import validate_email, EmailNotValidError
import re

from .forms import EmailForm, PasswordForm
from .util import send_email
from .utils.security import ts

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.is_verified:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email not verified. Please check your email to verify your account.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required     #so that user cant logout when they are not logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # pattern to match email addresses with valid TLDs
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 6:
            flash('Email is too short.', category='error')
        elif not re.match(email_pattern, email):
            flash('Invalid email address.', category='error')
        elif len(user_name) < 2:
            flash('Your name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) <7:
            flash('Password must be at lest 7 characters.', category='error')
        else:
            new_user = User(email=email, user_name=user_name, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()

            # login_user(new_user, remember=True) # to authenticate user
            # flash('Account created!', category='success')

            # Generate verification token
            token = ts.dumps(email, salt='email-confirm-key')

            # Send verification email with confirmation link
            subject = "Confirm your email"
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)
            html = render_template('email/activate.html', confirm_url=confirm_url)
            
            send_email(email, subject, html)

            flash('Account created! Please check your email to confirm your email address.', category='success')
            return redirect(url_for('views.home'))

            # add user to database

    return render_template("register.html", user=current_user)

@auth.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)    # Token expiration time: 1 day
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_verified = True
            db.session.commit()
            flash('Email confirmed! You can now log in.', category='success')
        else:
            flash('Invalid token.', category='error')
    except:
        # abort(404)
        flash('The confirmation link is invalid or has expired.', category='error')

    return redirect(url_for('auth.login'))

@auth.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('Invalid email address. Please check your email address and try again.', 'error')
            return render_template('reset.html', form=form, user=current_user)

        subject = "Password reset requested"

        # use the URLSafeTimedSerializer created in `util.py` 
        token = ts.dumps(user.email, salt='recover-key')

        recover_url = url_for(
            'auth.reset_with_token',
            token=token,
            _external=True)

        html = render_template(
            'email/recover.html',
            recover_url=recover_url)

        send_email(user.email, subject, html)

        return redirect(url_for('auth.reset_requested'))
    return render_template('reset.html', form=form, user=current_user)

@auth.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = generate_password_hash(form.new_password.data, method='scrypt')
        user.is_verified = True

        db.session.add(user)
        db.session.commit()

        flash('Your password has been successfully reset. You can now log in using your new password.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_with_token.html', form=form, token=token, user=current_user)

@auth.route('/reset_requested', methods=['GET', 'POST'])
def reset_requested():

    return render_template("reset_requested.html", user=current_user)
from . import user
from .forms import LoginForm, RegistrationForm
from ..classes import User
from .. import login_manager
from flask import render_template, session, redirect, url_for, flash, request, g
from flask_login import current_user, login_user, logout_user, login_required


@user.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@user.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        password=User.generate_password(form.password.data))
        new_user.create_user()
        flash("New user registered.")
        return redirect(url_for('user.login'))
    return render_template('register.html', title='Register', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_found = User.find_user(email=form.email.data)
        if user_found and user_found.verify_password(form.password.data):
            login_user(user_found)
            # session['auth_token'] = user.generate_auth_token(expiration=3600)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Wrong username or password')
        # if user_found is None or not user_found.verify_password(form.password.data):
        #     flash('invalid username or password')
        #     return redirect(url_for('user.login'))
        # login_user(user_found, remember=True)
        # return redirect(url_for('main.index'))

    return render_template('login.html', title='Log In', form=form)


@user.route('/logout')
@login_required
def logout():
    """
    Simply logout the currently logged in user.
    """
    logout_user()
    flash('Logged out')
    return redirect(url_for('main.index'))


@login_manager.user_loader
def load_user(user_id):
    if user_id is None:
        return redirect(url_for('user.login'))
    user_found = User.find_user(user_id=user_id)
    if user_found is not None:
        g.user = user_found
        return user_found
    else:
        return None


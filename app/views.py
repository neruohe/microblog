from flask import render_template, flash, redirect, url_for, session, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from .forms import LoginForm
from .models import User

@app.route('/')
@app.route('/index/')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname':'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname':'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

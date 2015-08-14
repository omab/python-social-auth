from flask import render_template, redirect
from flask.ext.login import login_required, logout_user

from flask_me_example import app


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/done/')
@login_required
def done():
    return render_template('done.html')


@app.route('/logout')
def logout():
    """Logout view"""
    logout_user()
    return redirect('/')

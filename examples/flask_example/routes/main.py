from flask import render_template
from flask.ext.login import login_required

from flask_example import app


@app.route('/')
def main():
    return render_template('home.html')


@login_required
@app.route('/done/')
def done():
    return render_template('done.html')

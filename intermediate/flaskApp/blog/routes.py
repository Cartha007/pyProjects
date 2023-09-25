from blog import app
from flask import render_template, redirect, url_for, flash, request


@app.route('/')
def home():
    return render_template('coming.html')


# Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template('400.html'), 500
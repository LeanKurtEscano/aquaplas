from flask import Flask, Blueprint, render_template, redirect, request, url_for, session, make_response
import mysql.connector

blueprint = Blueprint('blueprint', __name__, template_folder='template')

def make_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@blueprint.route('/')
def index():
    if 'loggedIn' in session:
        response = make_response(render_template('index.html'))
        return make_header(response)

    return redirect(url_for('auth.login'))

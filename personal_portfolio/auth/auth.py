from flask import Flask, Blueprint, render_template, redirect, request, url_for, session, make_response
import mysql.connector
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='template')

db_config = {
    'host':'localhost',
    'database':'db_sarah',
    'user':'root',
    'password':'choulodi321*',
}

def make_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

def connect_db():
    return mysql.connector.connect(**db_config)

@auth.route('/', methods=['POST', 'GET'])
def login():
    wrong_pass = ''
    user_found_error = ''
    
    # If already logged in
    if 'loggedIn' in session:
        response = make_response(redirect(url_for('blueprint.index')))
        return make_header(response)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tb_sarah WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user:
            if check_password_hash(user[9], password): 
                session['loggedIn'] = username
                session['firstname'] = user[1]
                response = make_response(redirect(url_for('blueprint.index')))
                return make_header(response)
            else:  
                wrong_pass = 'Password is incorrect'
        else:  
            user_found_error = 'User is not found'

        response = make_response(render_template('login.html', wrong_pass=wrong_pass, user_found_error=user_found_error))
        cursor.close()
        conn.close()
        return make_header(response)

    response = make_response(render_template('login.html', wrong_pass=wrong_pass))
    return make_header(response)
            
   
@auth.route('/logout')
def logout():
    session.clear()
    response = make_response(redirect(url_for('auth.login')))
    return make_header(response)


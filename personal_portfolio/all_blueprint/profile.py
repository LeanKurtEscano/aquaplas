from flask import  Blueprint, render_template, redirect, request, url_for,session
import mysql.connector

from .util.validation import validate_first_name,validate_middle_name,validate_last_name,validate_age,validate_birthday,validate_contact_number,validate_email

pr = Blueprint('pr',__name__,template_folder="template")

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

from flask import session, redirect, url_for, make_response, render_template

@pr.route('/profile', methods=["GET"])
def get_profile():
  
    if 'loggedIn' not in session or not session['loggedIn']:
     
        return redirect(url_for('auth.login'))
    
   
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    
    
    cursor.execute("SELECT * FROM tb_sarah WHERE id = 1")
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
  
    response = make_response(render_template('profile.html', user=user))
    
   
    response = make_header(response)
    
    return response


from flask import session, redirect, url_for, make_response, render_template, request

@pr.route('/update', methods=["GET", "POST"])
def user_update():
    try:
      
        if 'loggedIn' not in session or not session['loggedIn']:
            return redirect(url_for('auth.login'))
        
        id = 1  

        if request.method == "POST":
           
            form_data = {
                'firstname': request.form.get('firstname', '').strip(),
                'middlename': request.form.get('middlename', '').strip(),
                'lastname': request.form.get('lastname', '').strip(),
                'birthday': request.form.get('birthday', '').strip(),
                'age': request.form.get('age', '').strip(),
                'contact': request.form.get('contact', '').strip(),
                'email': request.form.get('email', '').strip(),
            }

           
            age = int(form_data['age']) if form_data['age'].isdigit() else None

           
            errors = {
                "firstname": validate_first_name(form_data['firstname']),
                "middlename": validate_middle_name(form_data['middlename']),
                "lastname": validate_last_name(form_data['lastname']),
                "birthday": validate_birthday(form_data['birthday'], age) if form_data['birthday'] and age else "Birthday and age are required.",
                "age": validate_age(age) if age is not None else "Age must be a valid number.",
                "contact": validate_contact_number(form_data['contact']),
                "email": validate_email(form_data['email']),
            }

           
            errors = {field: msg for field, msg in errors.items() if msg}

          
            if errors:
                response = make_response(render_template('update.html', form_data=form_data, errors=errors))
                return make_header(response)

           
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            update_query = (
                "UPDATE tb_sarah SET firstname=%s, middlename=%s, lastname=%s, birthday=%s, age=%s, contact=%s, email=%s WHERE id=%s"
            )
            update_values = (
                form_data['firstname'],
                form_data['middlename'],
                form_data['lastname'],
                form_data['birthday'],
                age,
                form_data['contact'],
                form_data['email'],
                id,
            )
            cursor.execute(update_query, update_values)
            conn.commit()
            cursor.close()
            conn.close()

           
            return redirect(url_for('pr.get_profile'))

       
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        select_query = "SELECT * FROM tb_sarah WHERE id = %s"
        cursor.execute(select_query, (id,))
        user_data = cursor.fetchone()


        form_data = {
            'firstname': user_data.get('firstname', '') if user_data else '',
            'middlename': user_data.get('middlename', '') if user_data else '',
            'lastname': user_data.get('lastname', '') if user_data else '',
            'birthday': user_data.get('birthday', '') if user_data else '',
            'age': user_data.get('age', '') if user_data else '',
            'contact': user_data.get('contact', '') if user_data else '',
            'email': user_data.get('email', '') if user_data else '',
        }

        cursor.close()
        conn.close()

       
        response = make_response(render_template('update.html', form_data=form_data, errors={}))
        return make_header(response)

    except Exception as e:
        
        error_message = f"An unexpected error occurred: {str(e)}"
        form_data = {
            'firstname': '',
            'middlename': '',
            'lastname': '',
            'birthday': '',
            'age': '',
            'contact': '',
            'email': ''
        }
        response = make_response(render_template('update.html', form_data=form_data, errors={"general": error_message}))
        return make_header(response)


@pr.route('/update-page', methods=["GET"])
def update_page():
    return redirect(url_for('pr.user_update'))

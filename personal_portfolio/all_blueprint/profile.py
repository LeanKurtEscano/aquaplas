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

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'loggedIn' not in session:
            return redirect(url_for('auth.login'))  
        response = func(*args, **kwargs)
        return make_header(response)
    return wrapper

def connect_db():
    return mysql.connector.connect(**db_config)

@pr.route('/profile', methods=["GET"])
def get_profile():
   
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)  

    cursor.execute("SELECT * FROM tb_sarah WHERE id = 1")
    user = cursor.fetchone()  
    cursor.close()
    conn.close()
  
    return render_template('profile.html', user=user)
    

@pr.route('/update', methods=["GET", "POST"])
def user_update():
    try:
      
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

            # Filter out empty error messages
            errors = {field: msg for field, msg in errors.items() if msg}

            # If there are validation errors, re-render the form with entered data and errors
            if errors:
                return render_template('update.html', form_data=form_data, errors=errors)

            # Perform database update if POST is valid
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
        
        # If no user is found, pass empty defaults to the template
        if not user_data:
            form_data = {
                'firstname': '',
                'middlename': '',
                'lastname': '',
                'birthday': '',
                'age': '',
                'contact': '',
                'email': ''
            }
        else:
            # Map the fetched data to form fields
            form_data = {
                'firstname': user_data.get('firstname', ''),
                'middlename': user_data.get('middlename', ''),
                'lastname': user_data.get('lastname', ''),
                'birthday': user_data.get('birthday', ''),
                'age': user_data.get('age', ''),
                'contact': user_data.get('contact', ''),
                'email': user_data.get('email', '')
            }

        cursor.close()
        conn.close()

        # Render the form template with fetched data
        return render_template('update.html', form_data=form_data, errors={})

    except Exception as e:
        # Handle exceptions and show error in case of failure
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
        return render_template('update.html', form_data=form_data, errors={"general": error_message})


@pr.route('/update-page', methods=["GET"])

def update_page():
    return redirect(url_for('pr.update'))

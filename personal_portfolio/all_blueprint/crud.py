from flask import Blueprint, jsonify, render_template, request, redirect, url_for,session,make_response
import mysql.connector
from .util.validation import validate_first_name,validate_middle_name,validate_last_name,validate_age,validate_birthday,validate_contact_number,validate_email
cr = Blueprint('cr', __name__, template_folder='template')

db_config = {
    'host':'localhost',
    'database':'db_sarah',
    'user':'root',
    'password':'choulodi321*',
}

def connect_db():
    return mysql.connector.connect(**db_config)

def make_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response



@cr.route('/read', methods=['GET'])
def read():
    try:
      
        if 'loggedIn' not in session or not session['loggedIn']:
            return redirect(url_for('auth.login'))

       
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

      
        cursor.execute("SELECT * FROM users_crud")
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        
        response = make_response(render_template('read.html', users=data))
        
        
        response = make_header(response)
        return response

    except mysql.connector.Error as err:
      
       print(f"{err}")




@cr.route('/user-profile/<int:id>', methods=["GET"])
def get_user(id):
    try:
     
        if 'loggedIn' not in session or not session['loggedIn']:
            return redirect(url_for('auth.login'))

        
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

       
        query = "SELECT * FROM users_crud WHERE user_id = %s"
        cursor.execute(query, (id,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

       
        if user:
            response = make_response(render_template('userdetail.html', user=user))
        else:
            response = make_response("User not found", 404)

        
        response = make_header(response)
        return response

    except Exception as e:
        
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)

@cr.route('/render-update/<int:id>', methods=["GET"])
def render_update(id):
    try:
       
        if 'loggedIn' not in session or not session['loggedIn']:
            return redirect(url_for('auth.login'))

      
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        
        select_query = "SELECT * FROM users_crud WHERE user_id = %s"
        cursor.execute(select_query, (id,))
        user_data = cursor.fetchone()

        cursor.close()
        conn.close()

        
        form_data = user_data or {"id": id}
        
      
        response = make_response(render_template("updateuser.html", form_data=form_data, id=id, errors={}))
        
       
        response = make_header(response)
        return response

    except mysql.connector.Error as db_err:
      
        error_message = f"Database error occurred: {db_err}"
        print(error_message)
        response = make_response("Database error occurred", 500)
        response = make_header(response)
        return response

    except Exception as e:
      
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        response = make_response("Internal server error", 500)
        response = make_header(response)
        return response



@cr.route('/update-user/<int:id>', methods=["GET", "POST"])
def update_user(id):
    try:
        # Check if the user is logged in
        if 'loggedIn' not in session or not session['loggedIn']:
            response = make_response(redirect(url_for('auth.login')))
            return make_header(response)

        user_id = id  # ID of the user to update

        if request.method == "POST":
            # Extract submitted form data
            form_data = {
                'id': user_id,
                'firstname': request.form.get('firstname', '').strip(),
                'middlename': request.form.get('middlename', '').strip(),
                'lastname': request.form.get('lastname', '').strip(),
                'birthday': request.form.get('birthday', '').strip(),
                'age': request.form.get('age', '').strip(),
                'contact': request.form.get('contact', '').strip(),
                'email': request.form.get('email', '').strip(),
            }

            # Convert age to integer if it's a valid number
            age = int(form_data['age']) if form_data['age'].isdigit() else None

            # Perform validation
            errors = {
                "firstname": validate_first_name(form_data['firstname']),
                "middlename": validate_middle_name(form_data['middlename']),
                "lastname": validate_last_name(form_data['lastname']),
                "birthday": validate_birthday(form_data['birthday'], age) if form_data['birthday'] and age else "Birthday and age are required.",
                "age": validate_age(age) if age else "Age must be a valid number.",
                "contact": validate_contact_number(form_data['contact']),
                "email": validate_email(form_data['email']),
            }

            # Check if the email is already registered by another user
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            select_query = "SELECT * FROM users_crud WHERE email = %s AND user_id != %s"
            cursor.execute(select_query, (form_data['email'], user_id))
            email_conflict = cursor.fetchone()
            cursor.close()
            conn.close()

            if email_conflict:
                errors['email'] = "This email has already been registered."

            # Filter only errors that have messages
            errors = {field: msg for field, msg in errors.items() if msg}

            if errors:
                # Render with errors
                response = make_response(render_template('updateuser.html', form_data=form_data, errors=errors))
                return make_header(response)

            # Update user information in database
            conn = connect_db()
            cursor = conn.cursor()
            update_query = """
            UPDATE users_crud
            SET firstname = %s, middlename = %s, lastname = %s, birthday = %s, age = %s, contact = %s, email = %s
            WHERE user_id = %s
            """
            cursor.execute(update_query, (
                form_data['firstname'], form_data['middlename'], form_data['lastname'],
                form_data['birthday'], age, form_data['contact'], form_data['email'], user_id
            ))
            conn.commit()
            cursor.close()
            conn.close()

            response = make_response(redirect(url_for('cr.read')))
            return make_header(response)

        # If method is GET, load the existing user data
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        select_query = "SELECT * FROM users_crud WHERE user_id = %s"
        cursor.execute(select_query, (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        # Populate form fields with the current user data
        form_data = {
            'id': user_data['user_id'] if user_data else '',
            'firstname': user_data['firstname'] if user_data else '',
            'middlename': user_data['middlename'] if user_data else '',
            'lastname': user_data['lastname'] if user_data else '',
            'birthday': user_data['birthday'] if user_data else '',
            'age': user_data['age'] if user_data else '',
            'contact': user_data['contact'] if user_data else '',
            'email': user_data['email'] if user_data else ''
        }

        response = make_response(render_template('updateuser.html', form_data=form_data, errors={}))
        return make_header(response)

    except Exception as e:
        # Handle unexpected errors
        error_message = f"An unexpected error occurred: {str(e)}"
        form_data = {
            'id': '',
            'firstname': '',
            'middlename': '',
            'lastname': '',
            'birthday': '',
            'age': '',
            'contact': '',
            'email': ''
        }
        response = make_response(render_template('updateuser.html', form_data=form_data, errors={"general": error_message}))
        return make_header(response)



@cr.route('/render-create',methods=["GET"])
def render_create():
    return redirect(url_for("cr.create"))

@cr.route('/create', methods=['GET', 'POST'])
def create():
    
    if 'loggedIn' not in session or not session['loggedIn']:
        response = make_response(redirect(url_for('auth.login')))
        return make_header(response)  

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
            "age": validate_age(age) if age else "Age must be a valid number.",
            "contact": validate_contact_number(form_data['contact']),
            "email": validate_email(form_data['email']),
        }

      
        errors = {field: msg for field, msg in errors.items() if msg}

       
        if not errors:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users_crud WHERE email = %s", (form_data['email'],))
                if cursor.fetchone():
                    errors['email'] = "Email has already been registered."
                cursor.close()
                conn.close()
            except Exception as e:
                errors['general'] = f"Unexpected database error: {str(e)}"

     
        if errors:
            response = make_response(render_template('create.html', form_data=form_data, errors=errors))
            return make_header(response)

       
        try:
            conn = connect_db()
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO users_crud (firstname, middlename, lastname, birthday, age, contact, email)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                form_data['firstname'], form_data['middlename'], form_data['lastname'],
                form_data['birthday'], age, form_data['contact'], form_data['email']
            ))
            conn.commit()
            cursor.close()
            conn.close()

            response = make_response(redirect(url_for('cr.read')))
            return make_header(response)

        except Exception as e:
            errors['general'] = f"Unexpected error during insertion: {str(e)}"
            response = make_response(render_template('create.html', form_data=form_data, errors=errors))
            return make_header(response)

    
    form_data = {
        'firstname': '',
        'middlename': '',
        'lastname': '',
        'birthday': '',
        'age': '',
        'contact': '',
        'email': '',
    }
    response = make_response(render_template("create.html", form_data=form_data, errors={}))
    return make_header(response)


    
@cr.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    
    if 'loggedIn' not in session or not session['loggedIn']:
        response = make_response(redirect(url_for('auth.login')))
        return make_header(response)

    try:
       
        conn = connect_db()
        cursor = conn.cursor()

  
        delete_query = "DELETE FROM users_crud WHERE user_id = %s"
        cursor.execute(delete_query, (id,))
        conn.commit()

        cursor.close()
        conn.close()

        response = make_response(redirect(url_for('cr.read')))
        return make_header(response)

    except Exception as e:
       
        print(f"An error occurred: {e}")

       
        response = make_response(redirect(url_for('cr.read')))
        return make_header(response)

        
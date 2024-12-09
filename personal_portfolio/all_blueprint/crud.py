from flask import Blueprint, jsonify, render_template, request, redirect, url_for,session
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

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'loggedIn' not in session:
            return redirect(url_for('auth.login'))  
        response = func(*args, **kwargs)
        return make_header(response)
    return wrapper

@cr.route('/read', methods=['GET'])
def read():
    try:
       
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)  
      
        cursor.execute("SELECT * FROM users_crud")
       
        data = cursor.fetchall()
      
        cursor.close()
        conn.close()
      
        return render_template('read.html', users=data)
    except mysql.connector.Error as err:
        print(err)




@cr.route('/user-profile/<int:id>', methods=["GET"])
def get_user(id):
    try:
     
        conn = connect_db()
        cursor = conn.cursor(dictionary=True) 
        
       
        query = "SELECT * FROM users_crud WHERE user_id = %s"
        cursor.execute(query, (id,))
        
      
        user = cursor.fetchone()
        
      
        cursor.close()
        conn.close()
      
        if user:
            return render_template('userdetail.html', user=user)
        else:
            return "User not found", 404
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Internal server error", 500

@cr.route('/render-update/<int:id>', methods=["GET"])
def render_update(id):
  
       
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
        
        
    select_query = "SELECT * FROM users_crud WHERE user_id = %s"
    cursor.execute(select_query, (id,))
    user_data = cursor.fetchone()
        
       
    cursor.close()
    conn.close()
  
    return render_template("updateuser.html", form_data=user_data or {"id": id}, id=id, errors={})
 


    
@cr.route('/update-user/<int:id>', methods=["GET", "POST"])
def update_user(id):
    try:
        user_id = id
        if request.method == "POST":
            # Collect and sanitize form data
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

            # Validate fields
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

            # Filter out empty error messages
            errors = {field: msg for field, msg in errors.items() if msg}

            # If there are validation errors, re-render the form with entered data and errors
            if errors:
                return render_template('updateuser.html', form_data=form_data, errors=errors)

            # Connect to database and execute the update query
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

            # Redirect upon successful update
            return redirect(url_for('cr.read'))

        # If GET request, fetch user data
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        select_query = "SELECT * FROM users_crud WHERE user_id = %s"
        cursor.execute(select_query, (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        # Prepopulate form fields with current data
        form_data = {
            'id': user_data['user_id'],
            'firstname': user_data['firstname'] if user_data else '',
            'middlename': user_data['middlename'] if user_data else '',
            'lastname': user_data['lastname'] if user_data else '',
            'birthday': user_data['birthday'] if user_data else '',
            'age': user_data['age'] if user_data else '',
            'contact': user_data['contact'] if user_data else '',
            'email': user_data['email'] if user_data else ''
        }

        # Render form with prepopulated data
        return render_template('updateuser.html', form_data=form_data, errors={})

    except Exception as e:
        # Handle unexpected errors
        error_message = f"An unexpected error occurred: {str(e)}"
        form_data = {
            'id':'',
            'firstname': '',
            'middlename': '',
            'lastname': '',
            'birthday': '',
            'age': '',
            'contact': '',
            'email': ''
        }
        return render_template('updateuser.html', form_data=form_data, errors={"general": error_message})


@cr.route('/render-create',methods=["GET"])
def render_create():
    return redirect(url_for("cr.create"))

@cr.route('/create', methods=['GET','POST'])
def create():
    
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
       
        errors = {field: msg for field, msg in errors.items() if msg}
        
        if errors:
            return render_template('create.html', form_data=form_data, errors=errors)
   
        conn = connect_db()
        cursor = conn.cursor()

      
        insert_query = """
            INSERT INTO users_crud (firstname, middlename, lastname, birthday, age, contact, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (form_data['firstname'],form_data['middlename'], form_data['lastname'], form_data['birthday'], age, form_data['contact'],form_data['email']))
        conn.commit()
   
        cursor.close()
        conn.close()
        return redirect(url_for('cr.read'))
    
    form_data = {
                'firstname': '',
                'middlename': '',
                'lastname': '',
                'birthday':'',
                'age': '',
                'contact': '',
                'email': '',
            }  
    return render_template("create.html",form_data=form_data, errors = {})
    
    

@cr.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
      
        conn = connect_db()
        cursor = conn.cursor()

      
        delete_query = "DELETE FROM users_crud WHERE user_id = %s"
        cursor.execute(delete_query, (id,))
        conn.commit()

       
        cursor.close()
        conn.close()

       
        return redirect(url_for('cr.read'))
    except Exception as e:
        print(f"An error occurred: {e}")
        return redirect(url_for('cr.read'))
        
from werkzeug.security	import generate_password_hash, check_password_hash
import mysql.connector

db_config = {
    'host':'localhost',
    'database':'db_sarah',
    'user':'root',
    'password':'choulodi321*',
}

def connect_db():
    return mysql.connector.connect(**db_config)

conn = connect_db()
cursor = conn.cursor()

user = {
    'firstname':'Sarah',
    'middlename':'Balmaceda',
    'lastname':'Ramos',
    'birthday':'2004-10-15',
    'age': 20,
    'contact':'09530547660',
    'email':'sarahramos180711@gmail.com',
    'username':'sarah',
    'password':'sarah with h'
}

hashed_password = generate_password_hash(user['password'])

cursor.execute("INSERT INTO tb_sarah (firstname, middlename, lastname, birthday, age, contact, email, username, password) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (user['firstname'], user['middlename'], user['lastname'], user['birthday'], user['age'], user['contact'], user['email'], user['username'], hashed_password))
conn.commit()

cursor.execute("SELECT * FROM tb_sarah")
data = cursor.fetchall()
print(data)

cursor.close()
conn.close()
 
user = 'sarah with h'
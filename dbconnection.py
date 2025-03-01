from dbconnection import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'SmartGrocery123'  

# Database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='usersGrocery'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('signup'))

        connection = create_connection()
        cursor = connection.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("Email already registered.")
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert user into database
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, hashed_password))
        connection.commit()
        flash("Signup successful! You can now log in.")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = create_connection()
        cursor = connection.cursor()

        # Check if email is registered
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            flash("Email not registered. Please sign up.")
            return redirect(url_for('login'))

        # Check if password is correct
        if not check_password_hash(user[3], password):  # Assuming password is the 4th column
            flash("Wrong password. Please try again.")
            return redirect(url_for('login'))

        flash("Login successful!")  # Redirect to a dashboard or home page
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"

if __name__ == '__main__':
    app.run(debug=True)

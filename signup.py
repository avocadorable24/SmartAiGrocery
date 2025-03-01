import mysql.connector
from mysql.connector import Error
from getpass import getpass

# Database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='',
            database='usersGrocery'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Function to sign up a new user
def signup():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = getpass("Enter your password: ")
    confirm_password = getpass("Confirm your password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    connection = create_connection()
    cursor = connection.cursor()

    # Check if email already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        print("Email already registered.")
        return

    # Insert user into database
    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                   (name, email, password))  # Note: You should hash the password in a real application
    connection.commit()
    print("Signup successful! You can now log in.")

    cursor.close()
    connection.close()

if __name__ == '__main__':
    signup()

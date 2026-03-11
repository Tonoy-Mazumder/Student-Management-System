import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="Your username",
        password="Your Database password",
        database="student_management"
    )


import mysql.connector

# Function to connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root", # <-- replace with your MySQL  user
        password="Root",  # <-- replace with your MySQL password
        database="student_management"
    )

# Login function
def login():
    db = get_connection()
    cursor = db.cursor()
    print("===== LOGIN =====")
    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                   (username, password))
    result = cursor.fetchone()
    if result:
        print("\nLogin Successful!\n")
        dashboard()
    else:
        print("\nInvalid username or password\n")

# Dashboard
def dashboard():
    while True:
        print("===== DASHBOARD =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.")

# Add student
def add_student():
    db = get_connection()
    cursor = db.cursor()

    print("\n===== ADD STUDENT =====")
    name = input("Enter name: ")
    course = input("Enter course: ")
    semester = input("Enter semester: ")
    phone = input("Enter phone: ")
    email = input("Enter email: ")

    cursor.execute("""
        INSERT INTO students (name, course, semester, phone, email)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, course, semester, phone, email))

    db.commit()
    print("Student added successfully!\n")

# View students
def view_students():
    db = get_connection()
    cursor = db.cursor()

    print("\n===== STUDENT LIST =====")
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    for row in rows:
        print(row)
    print()

# Update student
def update_student():
    db = get_connection()
    cursor = db.cursor()

    student_id = input("Enter student ID to update: ")

    print("Enter new details:")
    name = input("Name: ")
    course = input("Course: ")
    semester = input("Semester: ")
    phone = input("Phone: ")
    email = input("Email: ")

    cursor.execute("""
        UPDATE students SET
        name=%s, course=%s, semester=%s, phone=%s, email=%s
        WHERE student_id=%s
    """, (name, course, semester, phone, email, student_id))

    db.commit()
    print("Student updated successfully!\n")

# Delete student
def delete_student():
    db = get_connection()
    cursor = db.cursor()

    student_id = input("Enter student ID to delete: ")

    cursor.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
    db.commit()

    print("Student deleted successfully!\n")

# Start the program
login()


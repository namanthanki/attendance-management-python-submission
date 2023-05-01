import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="attendance_management_system"
)
cursor = db.cursor()

# Create main window
root = tk.Tk()
root.title("Attendance Management System")
root.geometry('1280x720')

# Define functions for each module
def faculty_authentication():
    # Create new window for faculty authentication
    auth_window = tk.Toplevel(root)
    auth_window.title("Faculty Authentication")

    # Create variables to store entered username and password
    username = tk.StringVar()
    password = tk.StringVar()

    # Create function to handle login
    def login():
        # Check if entered username and password match a record in the database
        cursor.execute("SELECT * FROM faculties WHERE username=%s AND password=%s", (username.get(), password.get()))
        result = cursor.fetchone()
        if result:
            # Login successful
            messagebox.showinfo("Success", "Login successful!")
            auth_window.destroy()
        else:
            # Login failed
            messagebox.showerror("Error", "Invalid username or password")

    # Create function to handle registration
    def register():
        # Check if entered username already exists in the database
        cursor.execute("SELECT * FROM faculties WHERE username=%s", (username.get(),))
        result = cursor.fetchone()
        if result:
            # Username already exists
            messagebox.showerror("Error", "Username already exists")
        else:
            # Insert new faculty into database
            cursor.execute("INSERT INTO faculties (username, password) VALUES (%s, %s)", (username.get(), password.get()))
            db.commit()
            messagebox.showinfo("Success", "Registration successful!")

    # Create labels and entry fields for username and password
    username_label = tk.Label(auth_window, text="Username")
    username_entry = tk.Entry(auth_window, textvariable=username)
    password_label = tk.Label(auth_window, text="Password")
    password_entry = tk.Entry(auth_window, textvariable=password, show="*")

    # Create buttons for login and register
    login_button = tk.Button(auth_window, text="Login", command=login)
    register_button = tk.Button(auth_window, text="Register", command=register)

    # Pack everything onto auth_window
    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    login_button.pack()
    register_button.pack()

def add_class():
    # Create new window for adding class
    add_class_window = tk.Toplevel(root)
    add_class_window.title("Add Class")

    # Create variables to store entered class information
    class_name = tk.StringVar()
    time_slot = tk.StringVar()

    # Create function to handle adding class
    def add():
        # Insert new class into database
        cursor.execute("INSERT INTO classes (name, time_slot) VALUES (%s, %s)", (class_name.get(), time_slot.get()))
        db.commit()
        messagebox.showinfo("Success", "Class added successfully!")
        add_class_window.destroy()

    # Create labels and entry fields for class information
    class_name_label = tk.Label(add_class_window, text="Class Name")
    class_name_entry = tk.Entry(add_class_window, textvariable=class_name)
    time_slot_label = tk.Label(add_class_window, text="Time Slot")
    time_slot_entry = tk.Entry(add_class_window, textvariable=time_slot)

    # Create button for adding class
    add_button = tk.Button(add_class_window, text="Add Class", command=add)

    # Pack everything onto add_class_window
    class_name_label.pack()
    class_name_entry.pack()
    time_slot_label.pack()
    time_slot_entry.pack()
    add_button.pack()

def add_students():
    # Create new window for adding students
    add_students_window = tk.Toplevel(root)
    add_students_window.title("Add Students")

    # Create variables to store entered student information
    student_name = tk.StringVar()
    enrolment_number = tk.StringVar()
    class_id = tk.IntVar()

    # Create function to handle adding student
    def add():
        # Insert new student into database
        cursor.execute("INSERT INTO students (name, enrolment_number, class_id) VALUES (%s, %s, %s)", (student_name.get(), enrolment_number.get(), class_id.get()))
        db.commit()
        messagebox.showinfo("Success", "Student added successfully!")

    # Create labels and entry fields for student information
    student_name_label = tk.Label(add_students_window, text="Student Name")
    student_name_entry = tk.Entry(add_students_window, textvariable=student_name)
    enrolment_number_label = tk.Label(add_students_window, text="Enrolment Number")
    enrolment_number_entry = tk.Entry(add_students_window, textvariable=enrolment_number)
    
    # Create dropdown menu for selecting class
    cursor.execute("SELECT id, name FROM classes")
    classes = cursor.fetchall()
    
    class_label = tk.Label(add_students_window, text="Class")
    class_dropdown = tk.OptionMenu(add_students_window, class_id, *[c[0] for c in classes])

    # Create button for adding student
    add_button = tk.Button(add_students_window, text="Add Student", command=add)

    # Pack everything onto add_students_window
    student_name_label.pack()
    student_name_entry.pack()
    enrolment_number_label.pack()
    enrolment_number_entry.pack()
    class_label.pack()
    class_dropdown.pack()
    add_button.pack()

def take_attendance():
    # Create new window for taking attendance
    take_attendance_window = tk.Toplevel(root)
    take_attendance_window.title("Take Attendance")

    # Create variable to store selected class
    class_id = tk.IntVar()

    # Create function to handle selecting class
    def select_class():
        # Create new window for selected class
        class_window = tk.Toplevel(take_attendance_window)
        class_window.title("Take Attendance")

        # Get list of students in selected class
        cursor.execute("SELECT id, name FROM students WHERE class_id=%s", (class_id.get(),))
        students = cursor.fetchall()

        # Create variables to store attendance status for each student
        attendance_vars = {}
        for student in students:
            attendance_vars[student[0]] = tk.StringVar(value="present")

        # Create function to handle submitting attendance
        def submit():
            # Insert attendance records into database
            for student_id, attendance_var in attendance_vars.items():
                cursor.execute("INSERT INTO attendances (date, student_id, status) VALUES (CURDATE(), %s, %s)", (student_id, attendance_var.get()))
            db.commit()
            messagebox.showinfo("Success", "Attendance submitted successfully!")
            class_window.destroy()

        # Create labels and dropdown menus for each student
        for student in students:
            student_label = tk.Label(class_window, text=student[1])
            student_dropdown = tk.OptionMenu(class_window, attendance_vars[student[0]], "present", "absent")
            student_label.pack()
            student_dropdown.pack()

        # Create button for submitting attendance
        submit_button = tk.Button(class_window, text="Submit Attendance", command=submit)
        submit_button.pack()

    # Create dropdown menu for selecting class
    cursor.execute("SELECT id, name FROM classes")
    classes = cursor.fetchall()
    
    class_label = tk.Label(take_attendance_window, text="Class")
    class_dropdown = tk.OptionMenu(take_attendance_window, class_id, *[c[0] for c in classes])

    # Create button for selecting class
    select_button = tk.Button(take_attendance_window, text="Select Class", command=select_class)

    # Pack everything onto take_attendance_window
    class_label.pack()
    class_dropdown.pack()
    select_button.pack()

def view_attendance():
    # Create new window for viewing attendance
    view_attendance_window = tk.Toplevel(root)
    view_attendance_window.title("View Attendance")

    # Create treeview to display attendance records
    tree = ttk.Treeview(view_attendance_window)
    tree["columns"] = ("date", "student_name", "status")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("date", anchor=tk.W, width=120)
    tree.column("student_name", anchor=tk.W, width=120)
    tree.column("status", anchor=tk.W, width=120)

    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("date", text="Date", anchor=tk.W)
    tree.heading("student_name", text="Student Name", anchor=tk.W)
    tree.heading("status", text="Status", anchor=tk.W)

    # Get attendance records from database
    cursor.execute("""
        SELECT attendances.date, students.name, attendances.status
        FROM attendances
        JOIN students ON attendances.student_id = students.id
        ORDER BY attendances.date DESC
    """)
    records = cursor.fetchall()

    # Insert records into treeview
    for record in records:
        tree.insert(parent="", index="end", iid=None, text="", values=record)

    # Pack treeview onto view_attendance_window
    tree.pack()

# Create buttons for each module
faculty_auth_button = tk.Button(root, text="Faculty Authentication", command=faculty_authentication)
add_class_button = tk.Button(root, text="Add Class", command=add_class)
add_students_button = tk.Button(root, text="Add Students", command=add_students)
take_attendance_button = tk.Button(root, text="Take Attendance", command=take_attendance)
view_attendance_button = tk.Button(root, text="View Attendance", command=view_attendance)

# Pack buttons onto main window
faculty_auth_button.pack()
add_class_button.pack()
add_students_button.pack()
take_attendance_button.pack()
view_attendance_button.pack()

# Run main loop
root.mainloop()
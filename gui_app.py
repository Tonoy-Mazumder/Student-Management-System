import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import random


# ---------- PARTICLE CLASS ----------
class Particle:
    def __init__(self, canvas, width, height, colors=None):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.x = random.randint(0, width)
        self.y = random.randint(-height, 0)
        self.size = random.randint(2, 6)
        self.speed = random.uniform(1, 3)
        self.colors = colors or ["#ffffff", "#ccccff", "#99ccff"]
        self.color = random.choice(self.colors)
        self.id = self.canvas.create_oval(self.x, self.y, self.x+self.size, self.y+self.size, fill=self.color, outline="")

    def move(self):
        self.y += self.speed
        if self.y > self.height:
            self.y = -self.size
            self.x = random.randint(0, self.width)
        self.canvas.coords(self.id, self.x, self.y, self.x+self.size, self.y+self.size)

    def change_color(self, colors):
        self.colors = colors
        self.color = random.choice(self.colors)
        self.canvas.itemconfig(self.id, fill=self.color)

# ---------- MAIN APP ----------
class StudentApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("1200x700")
        self.resizable(False, False)

        # Sidebar and main frame sizes
        self.sidebar_width = 220
        self.main_width = 700
        self.main_height = 500
        self.margin_x = (1200 - self.sidebar_width - self.main_width) // 2
        self.margin_y = (700 - self.main_height) // 2

        # Background canvas for particles
        self.bg_canvas = ctk.CTkCanvas(self, width=1200, height=700, bg="#1f1f1f", highlightthickness=0)
        self.bg_canvas.place(x=0, y=0)
        self.particle_colors = ["#ffffff", "#ccccff", "#99ccff"]
        self.particles = [Particle(self.bg_canvas, 1200, 700, self.particle_colors) for _ in range(80)]
        self.animate_particles()

        # Container for main frame
        self.main_frame = ctk.CTkFrame(self, width=self.main_width, height=self.main_height, corner_radius=15)

        # Dictionary for pages
        self.pages = {}

        # ---------- LOGIN PAGE ----------
        self.login_frame = ctk.CTkFrame(self, width=500, height=450, corner_radius=20, fg_color="#2b2b2b")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Icon at the top
        ctk.CTkLabel(self.login_frame, text="🎓", font=("Arial", 50)).pack(pady=(20, 10))
        ctk.CTkLabel(self.login_frame, text="Student Login", font=("Arial", 28, "bold")).pack(pady=(0, 30))

        # Username & password entries
        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username", width=350, height=45, font=("Arial", 14))
        self.username_entry.pack(pady=15)
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=350, height=45, font=("Arial", 14))
        self.password_entry.pack(pady=15)

        # Login button
        ctk.CTkButton(self.login_frame, text="Login", width=220, height=50, font=("Arial", 16, "bold"),
                       fg_color="#2196F3", hover_color="#1976D2", command=self.check_login).pack(pady=30)

    # ---------- PARTICLE ANIMATION ----------
    def animate_particles(self):
        for p in self.particles:
            p.move()
        self.after(30, self.animate_particles)

    # ---------- LOGIN FUNCTION ----------
    def check_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if username == "admin" and password == "admin":
            self.login_frame.destroy()
            self.init_app()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    # ---------- INITIALIZE APP AFTER LOGIN ----------
    def init_app(self):
        self.main_frame.place(x=self.sidebar_width + self.margin_x, y=self.margin_y)
        self.create_pages()
        self.show_page("welcome")
        self.show_sidebar()

    # ---------- CREATE PAGES ----------
    def create_pages(self):
        mw, mh = self.main_width, self.main_height

        # Welcome page
        welcome_frame = ctk.CTkFrame(self, width=1200, height=700)
        ctk.CTkLabel(welcome_frame, text="Welcome to Student Management System",
                     font=("Arial", 28)).place(relx=0.5, rely=0.5, anchor="center")
        self.pages["welcome"] = welcome_frame

        # ---------- ADD STUDENT ----------
        add_frame = ctk.CTkFrame(self.main_frame, width=mw, height=mh)
        self.add_entries = {}
        fields = ["Name", "Course", "Semester", "Phone", "Email"]
        start_y = 30
        gap = 55
        label_x = 50
        entry_x = 200
        for i, f in enumerate(fields):
            ctk.CTkLabel(add_frame, text=f, font=("Arial", 14)).place(x=label_x, y=start_y + i*gap)
            entry = ctk.CTkEntry(add_frame, width=350)
            entry.place(x=entry_x, y=start_y + i*gap)
            self.add_entries[f] = entry
        ctk.CTkButton(add_frame, text="Save", command=self.add_student, width=140, height=40)\
            .place(x=(mw-140)//2, y=start_y + len(fields)*gap + 20)
        self.pages["add"] = add_frame

        # ---------- VIEW STUDENTS ----------
        view_frame = ctk.CTkFrame(self.main_frame, width=mw, height=mh)
        self.search_box = ctk.CTkEntry(view_frame, placeholder_text="Search by name…", width=300)
        self.search_box.place(x=50, y=20)
        ctk.CTkButton(view_frame, text="Search", command=self.search_students, width=100, height=35).place(x=370, y=20)
        self.result_frame = ctk.CTkScrollableFrame(view_frame, width=mw-100, height=mh-80)
        self.result_frame.place(x=50, y=70)
        self.pages["view"] = view_frame

        # ---------- UPDATE STUDENT ----------
        update_frame = ctk.CTkFrame(self.main_frame, width=mw, height=mh)
        ctk.CTkLabel(update_frame, text="Student ID", font=("Arial", 14)).place(x=50, y=20)
        self.update_id = ctk.CTkEntry(update_frame, width=350)
        self.update_id.place(x=200, y=20)
        self.update_entries = {}
        start_y = 70
        gap = 55
        for i, f in enumerate(["Name","Course","Semester","Phone","Email"]):
            ctk.CTkLabel(update_frame, text=f, font=("Arial", 14)).place(x=50, y=start_y + i*gap)
            entry = ctk.CTkEntry(update_frame, width=350)
            entry.place(x=200, y=start_y + i*gap)
            self.update_entries[f] = entry
        ctk.CTkButton(update_frame, text="Load", command=self.load_student, width=120, height=35)\
            .place(x=250, y=start_y + 5*gap + 20)
        ctk.CTkButton(update_frame, text="Save Changes", command=self.update_student, width=140, height=35)\
            .place(x=400, y=start_y + 5*gap + 20)
        self.pages["update"] = update_frame

        # ---------- DELETE STUDENT ----------
        delete_frame = ctk.CTkFrame(self.main_frame, width=mw, height=mh)
        self.delete_search = ctk.CTkEntry(delete_frame, placeholder_text="Search by name or ID", width=400)
        self.delete_search.place(x=50, y=20)
        self.delete_search.bind("<KeyRelease>", lambda e: self.search_delete_students())
        self.delete_result_frame = ctk.CTkScrollableFrame(delete_frame, width=mw-100, height=mh-150)
        self.delete_result_frame.place(x=50, y=70)
        self.delete_info = ctk.CTkLabel(delete_frame, text="", justify="left", font=("Arial", 14))
        self.delete_info.place(x=50, y=mh-70)
        self.delete_btn = ctk.CTkButton(delete_frame, text="Delete Selected", fg_color="red", hover_color="#FF6666",
                                        command=self.delete_selected_student, width=160, height=40)
        self.delete_btn.place(x=mw//2-80, y=mh-40)
        self.delete_students = {}
        self.selected_delete_id = None
        self.pages["delete"] = delete_frame

        # ---------- ABOUT ----------
        about_frame = ctk.CTkFrame(self.main_frame, width=mw, height=mh)
        ctk.CTkLabel(about_frame, text="🏫", font=("Arial", 50)).place(relx=0.5, rely=0.25, anchor="center")
        about_text = (
            "Student Management System\n"
            "Version 1.0 – Released Dec 2025\n\n"
            "Developed by Web Wizards\n\n"
            "Description:\n"
            "A modern student management system to efficiently manage student records.\n\n"
            "Contact:\n"
            "Email: support@webwizards.com"
        )
        ctk.CTkLabel(about_frame, text=about_text, font=("Arial", 16), justify="center")\
            .place(relx=0.5, rely=0.55, anchor="center")
        self.pages["about"] = about_frame

    # ---------- SHOW PAGE ----------
    def show_page(self, page_name):
        for page in self.pages.values():
            page.place_forget()
        if page_name == "welcome":
            self.pages[page_name].place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.pages[page_name].place(x=0, y=0)
            if page_name == "view":
                self.load_all()
                self.search_box.focus_set()
            elif page_name == "delete":
                self.search_delete_students()

    # ---------- SIDEBAR ----------
    def show_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.place(x=0, y=0, relheight=1)
        buttons_info = [
            ("➕ Add Student", lambda: self.show_page("add"), "#42A5F5"),
            ("👀 View Students", lambda: self.show_page("view"), "#1E88E5"),
            ("✏️ Update Student", lambda: self.show_page("update"), "#1976D2"),
            ("🗑️ Delete Student", lambda: self.show_page("delete"), "#1565C0"),
            ("🎨 Change Particle Colors", self.change_particle_colors, "#64B5F6"),
            ("ℹ️ About", lambda: self.show_page("about"), "#29B6F6")
        ]
        for i, (text, cmd, color) in enumerate(buttons_info):
            ctk.CTkButton(self.sidebar, text=text, fg_color=color, hover_color="#0D47A1",
                           corner_radius=12, anchor="w", width=180, height=60, command=cmd)\
                .place(x=10, y=50+i*80)
        self.show_page("add")

    # ---------- PARTICLE COLOR ----------
    def change_particle_colors(self):
        palettes = [
            ["#ffffff", "#ccccff", "#99ccff"],
            ["#ff0000", "#ff9900", "#ffff00"],
            ["#00ff00", "#00ffff", "#0099ff"],
            ["#ff00ff", "#9900ff", "#ff99ff"]
        ]
        self.particle_colors = random.choice(palettes)
        for p in self.particles:
            p.change_color(self.particle_colors)

    # ---------- DATABASE FUNCTIONS ----------
    def add_student(self):
        data = tuple(self.add_entries[f].get().strip() for f in ["Name","Course","Semester","Phone","Email"])
        if any(not field for field in data):
            messagebox.showwarning("Warning", "Please fill in all fields before saving!")
            return
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students WHERE name=%s AND course=%s AND semester=%s", (data[0], data[1], data[2]))
        if cursor.fetchone():
            messagebox.showerror("Error", "This student already exists!")
            return
        cursor.execute("INSERT INTO students (name, course, semester, phone, email) VALUES (%s,%s,%s,%s,%s)", data)
        db.commit()
        messagebox.showinfo("Success","Student added successfully!")
        for entry in self.add_entries.values():
            entry.delete(0,"end")
        self.add_entries["Name"].focus_set()

    def load_all(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        for r in rows:
            ctk.CTkLabel(self.result_frame, text=f"ID:{r[0]} | Name:{r[1]} | Course:{r[2]} | Semester:{r[3]} | Phone:{r[4]} | Email:{r[5]}", anchor="w").pack(fill="x", pady=3)

    def search_students(self):
        keyword = self.search_box.get().strip()
        db = db_connection()
        cursor = db.cursor()
        if not keyword:
            cursor.execute("SELECT * FROM students")
        else:
            cursor.execute("SELECT * FROM students WHERE name LIKE %s", ('%' + keyword + '%',))
        rows = cursor.fetchall()
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        for r in rows:
            ctk.CTkLabel(self.result_frame, text=f"ID:{r[0]} | Name:{r[1]} | Course:{r[2]} | Semester:{r[3]} | Phone:{r[4]} | Email:{r[5]}", anchor="w").pack(fill="x", pady=3)

    def load_student(self):
        sid = self.update_id.get().strip()
        if not sid:
            messagebox.showwarning("Warning", "Please enter a Student ID to load!")
            return
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id=%s", (sid,))
        result = cursor.fetchone()
        if result:
            _, name, course, semester, phone, email = result
            for f, val in zip(["Name","Course","Semester","Phone","Email"], [name, course, semester, phone, email]):
                self.update_entries[f].delete(0,"end")
                self.update_entries[f].insert(0,val)
        else:
            messagebox.showerror("Error","Student ID does not exist!")

    def update_student(self):
        sid = self.update_id.get().strip()
        if not sid:
            messagebox.showwarning("Warning", "Please enter Student ID to update!")
            return
        data = tuple(self.update_entries[f].get().strip() for f in ["Name","Course","Semester","Phone","Email"])
        if any(not field for field in data):
            messagebox.showwarning("Warning", "All fields must be filled to update!")
            return
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id=%s", (sid,))
        if cursor.fetchone() is None:
            messagebox.showerror("Error","Student ID does not exist!")
            return
        cursor.execute("UPDATE students SET name=%s, course=%s, semester=%s, phone=%s, email=%s WHERE student_id=%s", data + (sid,))
        db.commit()
        messagebox.showinfo("Success","Student updated successfully!")
        self.update_id.delete(0,"end")
        for entry in self.update_entries.values():
            entry.delete(0,"end")
        self.update_id.focus_set()

    def search_delete_students(self):
        keyword = self.delete_search.get().strip()
        db = db_connection()
        cursor = db.cursor()
        if keyword.isdigit():
            cursor.execute("SELECT * FROM students WHERE student_id=%s", (keyword,))
        else:
            cursor.execute("SELECT * FROM students WHERE name LIKE %s", ('%' + keyword + '%',))
        rows = cursor.fetchall()
        for widget in self.delete_result_frame.winfo_children():
            widget.destroy()
        self.delete_students = {}
        for r in rows:
            key = f"ID:{r[0]} | {r[1]} | {r[2]} | Sem:{r[3]}"
            self.delete_students[key] = r[0]
            btn = ctk.CTkButton(self.delete_result_frame, text=key, anchor="w", width=self.main_width-120,
                                 command=lambda k=key: self.select_delete_student(k))
            btn.pack(pady=2)
        self.delete_info.configure(text="")
        self.selected_delete_id = None

    def select_delete_student(self, key):
        sid = self.delete_students.get(key)
        if sid:
            db = db_connection()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id=%s", (sid,))
            student = cursor.fetchone()
            if student:
                _, name, course, semester, phone, email = student
                self.selected_delete_id = sid
                self.delete_info.configure(text=f"ID: {sid}\nName: {name}\nCourse: {course}\nSemester: {semester}\nPhone: {phone}\nEmail: {email}")

    def delete_selected_student(self):
        if not self.selected_delete_id:
            messagebox.showwarning("Warning","Please select a student to delete!")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            db = db_connection()
            cursor = db.cursor()
            cursor.execute("DELETE FROM students WHERE student_id=%s", (self.selected_delete_id,))
            db.commit()
            messagebox.showinfo("Success","Student deleted successfully!")
            self.search_delete_students()


# ---------- RUN ----------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = StudentApp()
    app.mainloop()


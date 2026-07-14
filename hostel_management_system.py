# Import necessary libraries
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import tkinter as tk
from tkinter import messagebox
from sqlalchemy.exc import IntegrityError

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///hostel_management.db')
Session = sessionmaker(bind=engine)
session = Session()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    fee_due = Column(Float)
    room = relationship("Room", back_populates="students")

class Staff(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    salary = Column(Float)

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    size = Column(String)
    is_vacant = Column(String)
    students = relationship("Student", back_populates="room")

Base.metadata.create_all(engine)

# User Interface
class HostelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hostel Management System")
        self.root.geometry("800x600")

        self.login_screen()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Warden Login").pack()

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.check_login).pack()

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # For simplicity, hardcoding a single user
        if username == "warden" and password == "password":
            self.main_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Hostel Management System").pack()

        tk.Button(self.root, text="Student Registration", command=self.student_registration).pack()
        tk.Button(self.root, text="Staff Registration", command=self.staff_registration).pack()
        tk.Button(self.root, text="Room Management", command=self.room_management).pack()
        tk.Button(self.root, text="Accounts", command=self.accounts_management).pack()
        tk.Button(self.root, text="Reports", command=self.generate_reports).pack()

    def student_registration(self):
        self.clear_screen()
        tk.Label(self.root, text="Student Registration").pack()

        tk.Label(self.root, text="Name").pack()
        self.student_name_entry = tk.Entry(self.root)
        self.student_name_entry.pack()

        tk.Label(self.root, text="Room ID").pack()
        self.student_room_id_entry = tk.Entry(self.root)
        self.student_room_id_entry.pack()

        tk.Button(self.root, text="Register", command=self.register_student).pack()

        tk.Button(self.root, text="Show Students", command=self.show_students).pack()

        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def register_student(self):
        name = self.student_name_entry.get()
        room_id = self.student_room_id_entry.get()

        try:
            room = session.query(Room).filter_by(id=int(room_id)).first()
            if room and room.is_vacant.lower() == 'yes':
                new_student = Student(name=name, room_id=int(room_id), fee_due=0)
                room.is_vacant = 'no'
                session.add(new_student)
                session.commit()
                messagebox.showinfo("Success", "Student registered and room allocated successfully")
            else:
                messagebox.showerror("Error", "Room is either not vacant or does not exist")
        except IntegrityError:
            session.rollback()
            messagebox.showerror("Error", "Failed to register student. Please check the room ID.")

    def show_students(self):
        students = session.query(Student).all()
        student_info = "Registered Students:\n"
        for student in students:
            student_info += f"ID: {student.id}, Name: {student.name}, Room ID: {student.room_id}, Fee Due: {student.fee_due}\n"
        messagebox.showinfo("Students", student_info)

    def staff_registration(self):
        self.clear_screen()
        tk.Label(self.root, text="Staff Registration").pack()

        tk.Label(self.root, text="Name").pack()
        self.staff_name_entry = tk.Entry(self.root)
        self.staff_name_entry.pack()

        tk.Label(self.root, text="Salary").pack()
        self.staff_salary_entry = tk.Entry(self.root)
        self.staff_salary_entry.pack()

        tk.Button(self.root, text="Register", command=self.register_staff).pack()

        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def register_staff(self):
        name = self.staff_name_entry.get()
        salary = self.staff_salary_entry.get()

        new_staff = Staff(name=name, salary=float(salary))
        session.add(new_staff)
        session.commit()
        messagebox.showinfo("Success", "Staff registered successfully")

    def room_management(self):
        self.clear_screen()
        tk.Label(self.root, text="Room Management").pack()

        tk.Label(self.root, text="Room Size").pack()
        self.room_size_entry = tk.Entry(self.root)
        self.room_size_entry.pack()

        tk.Label(self.root, text="Vacant (Yes/No)").pack()
        self.room_vacant_entry = tk.Entry(self.root)
        self.room_vacant_entry.pack()

        tk.Button(self.root, text="Add Room", command=self.add_room).pack()

        tk.Button(self.root, text="Show Room Status", command=self.show_rooms).pack()

        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def add_room(self):
        size = self.room_size_entry.get()
        is_vacant = self.room_vacant_entry.get()

        new_room = Room(size=size, is_vacant=is_vacant)
        session.add(new_room)
        session.commit()
        messagebox.showinfo("Success", "Room added successfully")

    def show_rooms(self):
        rooms = session.query(Room).all()
        room_info = "Room Status:\n"
        for room in rooms:
            room_info += f"Room ID: {room.id}, Size: {room.size}, Vacant: {room.is_vacant}\n"
        messagebox.showinfo("Rooms", room_info)

    def accounts_management(self):
        self.clear_screen()
        tk.Label(self.root, text="Accounts Management").pack()

        tk.Label(self.root, text="Student ID").pack()
        self.account_student_id_entry = tk.Entry(self.root)
        self.account_student_id_entry.pack()

        tk.Label(self.root, text="Fee Due").pack()
        self.account_fee_due_entry = tk.Entry(self.root)
        self.account_fee_due_entry.pack()

        tk.Button(self.root, text="Update Fee", command=self.update_fee).pack()

        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def update_fee(self):
        student_id = self.account_student_id_entry.get()
        fee_due = self.account_fee_due_entry.get()

        student = session.query(Student).filter_by(id=int(student_id)).first()
        if student:
            student.fee_due = float(fee_due)
            session.commit()
            messagebox.showinfo("Success", "Fee updated successfully")
        else:
            messagebox.showerror("Error", "Student not found")

    def generate_reports(self):
        self.clear_screen()
        tk.Label(self.root, text="Reports").pack()

        # Placeholder for report generation logic
        tk.Button(self.root, text="Generate Report", command=self.generate_sample_report).pack()

        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def generate_sample_report(self):
        # Placeholder for generating sample report
        messagebox.showinfo("Report", "Sample report generated")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HostelManagementSystem(root)
    root.mainloop()

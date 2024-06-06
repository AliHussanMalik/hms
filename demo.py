import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

Base = declarative_base()
engine = create_engine('sqlite:///hostel_management.db')
Session = sessionmaker(bind=engine)
session = Session()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    student_id = Column(String, unique=True)
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
    room_number = Column(Integer, unique=True)  # Unique room number
    size = Column(String)
    is_vacant = Column(String)
    students = relationship("Student", back_populates="room")

Base.metadata.create_all(engine)

class HostelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hostel Management System")
        self.root.geometry("800x600")

        self.login_screen()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Warden Login").grid(row=0, column=1)

        tk.Label(self.root, text="Username").grid(row=1, column=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Password").grid(row=2, column=0)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Login", command=self.check_login).grid(row=3, column=1)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # For simplicity, hardcoding a single user
        if username == "warden" and password == "password":
            self.main_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def main_menu(self):
        # Implement main menu options
        pass

    def register_student(self):
        name = self.student_name_entry.get()
        room_id = self.student_room_id_entry.get()

        try:
            room = session.query(Room).filter_by(id=int(room_id)).first()
            if room and room.is_vacant.lower() == 'yes':
                # Generate student ID based on room number and student count
                student_count = session.query(Student).filter_by(room_id=int(room_id)).count() + 1
                student_id = f"0{room.room_number}{student_count}"  # Format: 0roomIDStudentCount
                new_student = Student(student_id=student_id, name=name, room_id=int(room_id), fee_due=0)
                room.is_vacant = 'no'
                session.add(new_student)
                session.commit()
                messagebox.showinfo("Success", "Student registered and room allocated successfully")
            else:
                messagebox.showerror("Error", "Room is either not vacant or does not exist")
        except IntegrityError:
            session.rollback()
            messagebox.showerror("Error", "Failed to register student. Please check the room ID.")

    # Implement other methods...

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HostelManagementSystem(root)
    root.mainloop()

import tkinter as tk
import sqlite3 as sql

class stdDatabase:
    def __init__(self):
        self.con = sql.connect("students.db")
        self.cursor = self.con.cursor()
    def createTable(self):
        student_table = """CREATE TABLE IF NOT EXISTS Student(
            STD_ID INT PRIMARY KEY,
            STD_NAME TEXT,
            STD_EMAIL TEXT,
            STD_GPA REAL)"""
        try:
            self.cursor.execute(student_table)
            self.con.commit()
            return True
        except sql.Error as err:
            return False
            #do something about the error.
    def insertRecord(self, std_ID, std_name, std_email, std_gpa):
        insert_statement = """INSERT INTO Student VALUES
        (?,?,?,?)"""
        try:
            self.cursor.execute(insert_statement, (std_ID, std_name, std_email, std_gpa))
            self.con.commit()
            return True
        except sql.Error as err:
            return False
    def updateRecord(self, std_ID, std_name, std_email, std_gpa):
        update_statement = '''UPDATE STUDENT 
                            SET STD_NAME=?, STD_EMAIL=?, STD_GPA=?
                            WHERE STD_ID=?'''
        try:
            self.cursor.execute(update_statement, (std_name, std_email, std_gpa, std_ID))
            self.con.commit()
            return True
        except sql.Error as err:
            return False
    def dataRecord(self):
        self.cursor.execute("SELECT * FROM Student")
    def closeConnection(self):
        self.con.close()



class StudentData(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("Student Management System")
        self.ID = tk.IntVar(self)
        self.name = tk.StringVar(self)
        self.email = tk.StringVar(self)
        self.gpa = tk.DoubleVar(self)
        self.database = stdDatabase()
    def createStudentTable(self):
        self.database.createTable();
    def createLabel(self, rowNum, columnNum, labelText):
        label = tk.Label(self, text=labelText)
        label.grid(row=rowNum, column=columnNum)
    def createEntry(self, rowNum, columnNum, fieldName):
        if fieldName == 'ID':
            entryVar = self.ID
        elif fieldName == 'Name':
            entryVar = self.name
        elif fieldName == 'EMAIL':
            entryVar = self.email
        elif fieldName == 'GPA':
            entryVar = self.gpa
        else:
            entryVar = None
        if entryVar is not None:
            entry = tk.Entry(self, textvariable=entryVar)
            entry.grid(row=rowNum, column=columnNum)
    def createTextArea(self, rowNum, columnNum, text):
        textArea = tk.Text(self, height=len(text), width=max(len(line) for line in text))
        textArea.grid(row=rowNum, column=columnNum)
        
        for line in text:
            textArea.insert(tk.END, line + "\n")
    def createButton(self, parent, rowNum, columnNum, buttonTitle, functionName):
        button = tk.Button(parent, text=buttonTitle, command=functionName)
        button.grid(row=rowNum, column=columnNum)
    def addNewStudent(self):
        print("Hello from addnewstudent")
        self.database.insertRecord(self.ID.get(), self.name.get(), self.email.get(), self.gpa.get())
    
    def addStudent(self):
        newWindow = tk.Toplevel(self)
        newWindow.title("Add Student")
        print("hello from addstudent")
        tk.Label(newWindow, text="Student ID:").grid(row=0, column=0)
        idEntry = tk.Entry(newWindow, textvariable=self.ID)
        idEntry.grid(row=0, column=1)
        tk.Label(newWindow, text="Student Name:").grid(row=1, column=0)
        nameEntry = tk.Entry(newWindow, textvariable=self.name)
        nameEntry.grid(row=1, column=1)
        tk.Label(newWindow, text="Student Email:").grid(row=2, column=0)
        emailEntry = tk.Entry(newWindow, textvariable=self.email)
        emailEntry.grid(row=2, column=1)
        tk.Label(newWindow, text="Student GPA:").grid(row=3, column=0)
        gpaEntry = tk.Entry(newWindow, textvariable=self.gpa)
        gpaEntry.grid(row=3, column=1)
        
        self.createButton(newWindow, 4, 0, "Add", self.addNewStudent)
        
    def updateStudent(self):
        newWindow = tk.Toplevel(self)
        newWindow.title("Update Student Data")
        
        tk.Label(newWindow, text="Student ID:").grid(row=0, column=0)
        idEntry = tk.Entry(newWindow, textvariable=self.ID)
        idEntry.grid(row=0, column=1)
        tk.Label(newWindow, text="Student Name:").grid(row=1, column=0)
        nameEntry = tk.Entry(newWindow, textvariable=self.name)
        nameEntry.grid(row=1, column=1)
        tk.Label(newWindow, text="Student Email:").grid(row=2, column=0)
        emailEntry = tk.Entry(newWindow, textvariable=self.email)
        emailEntry.grid(row=2, column=1)
        tk.Label(newWindow, text="Student GPA:").grid(row=3, column=0)
        gpaEntry = tk.Entry(newWindow, textvariable=self.gpa)
        gpaEntry.grid(row=3, column=1)
        self.createButton(newWindow, 4, 0, "Update", self.updateExistingStudent)
        
    def updateExistingStudent(self, id, name, email, gpa):
        print("whoa")
        
        self.database.insertRecord(id, name, email, gpa)
        
    def displayStudent(self):
        newWindow = tk.Toplevel(self)
        newWindow.title("Student Data")
        textArea = tk.Text(newWindow)
        textArea.grid(row=0, column=0)
        students = self.database.dataRecord()
        for student in students:
            textArea.insert(student)

def main():
    std = StudentData()
    std.createStudentTable()
    std.createLabel(0, 0, "System Management System")
    std.createButton(std, 1, 0, "Add Student", std.addStudent)
    std.createButton(std, 2, 0, "Update Student", std.updateStudent)
    std.createButton(std, 3, 0, "Display Students", std.displayStudent)
    std.mainloop()

if __name__ == "__main__":
    main()
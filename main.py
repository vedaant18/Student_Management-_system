from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
from PyQt6.QtGui import *
import sqlite3 as sq
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500,300)
        self.setWindowTitle("Student Management system")

        #file menu bar
        file_menu_item=self.menuBar().addMenu("&File")
        Help_menu_item=self.menuBar().addMenu("&Help")
        Edit_menu_item=self.menuBar().addMenu("&Edit")
        

        #add student 
        add_student= QAction(QIcon("add.png"),"Add Student",self)
        add_student.triggered.connect(self.insert_student)
        file_menu_item.addAction(add_student)
        #about the student management system 
        about_action=QAction("About",self)
        Help_menu_item.addAction(about_action)
        about_action.MenuRole(QAction.MenuRole.NoRole)
        #search student
        self.search_student= QAction(QIcon("search.png"),"Search",self)
        
        self.search_student.triggered.connect(self.search_stud)
        Edit_menu_item.addAction(self.search_student)


        self.table=QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID","Name","Course","Mobile"))
        self.setCentralWidget(self.table)
        self.table.verticalHeader().setVisible(False)
        self.load_data()
        #create toolbar
        toolbar=QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student)
        toolbar.addAction(self.search_student)
        #status bar
        self.statusbar=QStatusBar()
        self.setStatusBar(self.statusbar)
        
        #detect selected cells 
        self.table.cellClicked.connect(self.cell_click)
    
    def cell_click(self):
         edit_button=QPushButton("Edit")
         edit_button.clicked.connect(self.edit)
         
         delete_button=QPushButton("Delete")
         delete_button.clicked.connect(self.detele_student)

         children=self.findChildren(QPushButton)
         if children:
             for child in children:
                self.statusbar.removeWidget(child)

                
         self.statusbar.addWidget(delete_button)
         self.statusbar.addWidget(edit_button)

    def load_data(self):
        connection= sq.connect("database.db")
        result= connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_numb, row_data in enumerate(result):
            self.table.insertRow(row_numb)
            for comlumb_numb, data in enumerate(row_data):
                self.table.setItem(row_numb,comlumb_numb,QTableWidgetItem(str(data)))
        connection.close()
        self.table
    def insert_student(self):
        dialog= InsertDialog()
        dialog.exec()
    def search_stud(self):
        search_page= Search()
        search_page.exec()

    #edit function
    def edit(self):
        edit_dialog=EditDialog()
        edit_dialog.exec()
    #delete function
    def detele_student(self):
        delete_dialog=DeleteDialog()
        delete_dialog.exec()


    




class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        layout=QVBoxLayout()

        #student data entry 

        #student name entry
        self.student_name= QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)
        #student course
        self.student_course= QComboBox()
        course=["Biology","Astronomy","Physics",]
        self.student_course.addItems(course)
        layout.addWidget(self.student_course)
        #student mobile
        self.student_mobile= QLineEdit()
        self.student_mobile.setPlaceholderText('Mobile Number')
        layout.addWidget(self.student_mobile)

        #button
        button=QPushButton("Submit")
        button.clicked.connect(self.add_student)
        button.clicked.connect(self.close)
        layout.addWidget(button)
        self.setLayout(layout)

    def add_student(self):
        name=self.student_name.text()
        course=self.student_course.itemText(self.student_course.currentIndex())
        mobile=self.student_mobile.text()

        connection=sq.connect("database.db")
        cursor=connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",(name,course,mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_page.load_data()
    


    

class Search(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        layout=QVBoxLayout()

        self.student_name= QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        #button
        button=QPushButton("Search")
        button.clicked.connect(self.find_student)
        button.clicked.connect(self.close)
        layout.addWidget(button)
        
        self.setLayout(layout)
        

    def find_student(self):
        name=self.student_name.text()
        connection=sq.connect("database.db")
        cursor=connection.cursor()
        result=cursor.execute("SELECT * FROM students WHERE name = ?",(name,))
        rows=list(result)
        
        
        items= main_page.table.findItems(name,Qt.MatchFlag.MatchFixedString)
        for item in items:         
            main_page.table.item(item.row(),1).setSelected(True)
        cursor.close()
        connection.close()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        layout=QVBoxLayout()

        index=main_page.table.currentRow()
        student_name=main_page.table.item(index,1).text()

        self.student_id=main_page.table.item(index,0).text()

        #student name entry
        self.student_name= QLineEdit(student_name)
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)
        #student course
        course_name=main_page.table.item(index,2).text()
        self.student_course= QComboBox()
        course=["Biology","Astronomy","Physics",]
        self.student_course.addItems(course)
        self.student_course.setCurrentText(course_name)
        layout.addWidget(self.student_course)
        #student mobile
        student_mob=main_page.table.item(index,3).text()
        self.student_mobile= QLineEdit(student_mob)
        self.student_mobile.setPlaceholderText('Mobile Number')
        layout.addWidget(self.student_mobile)

        #button
        button=QPushButton("Update")
        button.clicked.connect(self.edit_student)
        button.clicked.connect(self.close)
        layout.addWidget(button)
        self.setLayout(layout)

    def edit_student(self):
        connection= sq.connect('C:\VEDAANT\student management system\database.db')
        cursor= connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",(self.student_name.text(),self.student_course.itemText(self.student_course.currentIndex()),self.student_mobile.text(),self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_page.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("delete Student data")
        self.setFixedHeight(100)
        self.setFixedWidth(300)
        layout=QGridLayout()

        confirmation= QLabel("Are your sure you want to delete this row?")
        yes_button=QPushButton("YES")
        
        no_button=QPushButton("NO")
        layout.addWidget(confirmation,0,0,1,2)
        layout.addWidget(yes_button,1,0)
        layout.addWidget(no_button,1,1)
        self.setLayout(layout)

        index=main_page.table.currentRow()
        

        self.student_id=main_page.table.item(index,0).text()
        yes_button.clicked.connect(self.delete_student)
        yes_button.clicked.connect(self.close)
        no_button.clicked.connect(self.close)




        #write a fuction for delete buttons
    def delete_student(self):
        index=main_page.table.currentRow()
        student_id=main_page.table.item(index,0).text()

        connection= sq.connect('C:\VEDAANT\student management system\database.db')
        cursor= connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?",(student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_page.load_data()

            




            
            




    
        



        

            
            
            


    




    
        
        
        
        





        
        
        







app=QApplication(sys.argv)  
main_page=MainWindow()
main_page.show()
sys.exit(app.exec())




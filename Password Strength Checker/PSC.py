import os
import json
import csv
import datetime
import requests
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QMainWindow
from PyQt5.QtCore import Qt, QThread, pyqtSignal   
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import random

print("--------------------------------------------------------------------")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 400, 500, 300)
        self.setFixedSize(500, 300)
        self.setWindowTitle("Password Strength Checker")
        self.initUI()
        
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        row1 = QVBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QVBoxLayout()
        
        self.title = QLabel("Password Strength Checker")
        self.title.setFont(QFont("Arial", 18, QFont.Bold))
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setStyleSheet("color: #222222;")

        self.subtitle = QLabel("Check how secure your password is")
        self.subtitle.setFont(QFont("Arial", 11))
        self.subtitle.setStyleSheet("color: #666666;")
        self.subtitle.setAlignment(Qt.AlignLeft)

        row1.addWidget(self.title)
        row1.addWidget(self.subtitle)
        row1.setContentsMargins(20, 10, 20, 20)

        layout.addLayout(row1)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter your password here")
        self.input.setFont(QFont("Arial", 11))
        self.input.setFixedWidth(350)
        row2.addWidget(self.input)
        row2.addStretch()
        row2.setContentsMargins(20, 0, 0, 0)
        
        self.submit_button = QPushButton("Check Password")
        self.submit_button.setFont(QFont("Arial", 8, QFont.Bold))
        self.submit_button.setFixedWidth(125)
        self.submit_button.setFixedHeight(35)
        self.submit_button.clicked.connect(self.check_password_strength)
        self.submit_button.setStyleSheet("""
                                         QPushButton {
                                             background-color: #4CAF50;
                                             color: white;
                                             border: none;
                                             padding: 10px;
                                             border-radius: 5px;
                                             }
                                             
                                             QPushButton:hover {
                                                 background-color: #45a049;
                                             }
                                             """)
        row3.addWidget(self.submit_button)
        
        
        self.tips_button = QPushButton("Tips")
        self.tips_button.setFont(QFont("Arial", 8, QFont.Bold))
        self.tips_button.setFixedWidth(70)
        self.tips_button.setFixedHeight(35)
        self.tips_button.clicked.connect(self.tips_screen)
        
        self.tips_button.setStyleSheet("""
                                         QPushButton {
                                             background-color: #4CAF50;
                                             color: white;
                                             border: none;
                                             padding: 10px;
                                             border-radius: 5px;
                                             }
                                             
                                             QPushButton:hover {
                                                 background-color: #45a049;
                                             }
                                             """)
        row3.addWidget(self.tips_button)
        
        row3.addStretch()
        row3.setContentsMargins(20, 5, 0, 20)
         
        self.password_strength_label = QLabel("")
        self.password_strength_label.setFont(QFont("Arial", 11))
        self.password_strength_label.setStyleSheet("""
                                                   QLabel{
                                                       font-weight: bold;
                                                   }
                                                   
                                                   """)
        row4.addWidget(self.password_strength_label)
        
        
        self.comment_label = QLabel("")
        self.comment_label.setFont(QFont("Arial", 10))
        row4.addWidget(self.comment_label)
        
        row4.addStretch()
        row4.setContentsMargins(20, 5, 0, 20)
        
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addStretch()
        layout.addLayout(row4)
        
    def evaluate_strength(self, password):
        
        common_patterns = [
    
        "password", "passw0rd", "p@ssword",
        "admin", "administrator", "root",
        "login", "welcome", "letmein",

        
        "123", "1234", "12345", "123456", "1234567", "12345678",
        "111", "1111", "000", "0000",
        "1212", "1122", "123123",

        
        "qwerty", "qwertyuiop",
        "asdf", "asdfgh", "asdfghjkl",
        "zxcv", "zxcvbn", "zxcvbnm",


        "abc", "abcd", "abcdef",
        "xyz", "mnop"
        
        ]
        
        special_characters = [
        "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_",
        "+", "=", "{", "}", "[", "]", "|", ":", ";", "<", ">", ",",
        ".", "?", "/", "~", "`"
    ]
        
        strength = len(password) * 3
            
        strength += min(sum(c in special_characters for c in password) * 2, 20)
            
            
        if len(set(password)) < len(password) * 0.5:
            strength -= 15
            
        
        if any(c.isupper() for c in password) and any(c.islower() for c in password):
            strength += 14
            
        if any(c.isdigit() for c in password):
            strength += 14
            
        if any(pattern.lower() in password.lower() for pattern in common_patterns):
            strength *= 0.5
            
        if password.islower():
            strength *= 0.75
            
        if password.isupper():
            strength *= 0.75
        
        strength = min(strength, 100)
        strength = max(strength, 0)
        
        return round(strength)
        
    def check_password_strength(self): 
        password = self.input.text()
        
        if not password:
            QMessageBox.warning(self, "Input Error", "Please enter a password to check its strength.")
            return
        elif len(password) < 6:
            QMessageBox.warning(self, "Input Error", "Password must be between 6 and 32 characters")
            return
        elif len(password) > 32:
            QMessageBox.warning(self, "Input Error", "Password must be between 6 and 32 characters")
        elif " " in password:
            QMessageBox.warning(self, "Input Error", "Password must not contain spaces")
        else:
            strength = self.evaluate_strength(password)
            self.password_strength_label.setText(f"Password Strength Score: {strength}")
            
            if strength <= 20:
                self.comment_label.setText("Password is very weak!")
                self.comment_label.setStyleSheet("color: #ff1100; font:bold;")
            elif strength <= 30 and strength > 20:
                self.comment_label.setText("Password is weak!")
                self.comment_label.setStyleSheet("color: #ab1309; font:bold;")
            elif strength <= 50 and strength > 30:
                self.comment_label.setText("Password is moderate!")
                self.comment_label.setStyleSheet("color: #e67300; font:bold;")
            elif strength <= 70 and strength > 50:
                self.comment_label.setText("Password is Strong!")
                self.comment_label.setStyleSheet("color: #339900; font:bold;")
            else:
                self.comment_label.setText("Password is Extremely strong!")
                self.comment_label.setStyleSheet("color: #006600; font:bold;")
            
    def tips_screen(self):
        tips = (
        "• Make the password long\n"
        "• Mix uppercase and lowercase letters\n"
        "• Include digits (0-9)\n"
        "• Include special characters like @, #, !\n"
        "• Avoid common phrases like 'password' or '123'"
        )
        QMessageBox.information(self, "Password Tips", tips)
            

            

         
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()

print("--------------------------------------------------------------------")



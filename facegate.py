from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QApplication, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QLabel

import sys, json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #with open("procs.json") as f:
        #    procs = json.load(f)

        # LINE LAYOUT WIDGETS
        layout_line = QHBoxLayout()

        self.file_name = ""

        self.proc_name_line = QLabel("File name: " + self.file_name)
        layout_line.addWidget(self.proc_name_line)
        
        proc_location = QPushButton("Open file")
        proc_location.clicked.connect(lambda: self.get_file_name(self.proc_name_line))
        layout_line.addWidget(proc_location)

        add_proc = QPushButton("Add")
        add_proc.clicked.connect(self.add_procs)
        layout_line.addWidget(add_proc)

        # PROCS LAYOUT WIDGETS
        layout_procs = QVBoxLayout()

        # COMBINING LAYOUTS
        main_layout = QVBoxLayout()

        widget_line = QWidget()
        widget_line.setLayout(layout_line)

        widget_procs = QWidget()
        widget_procs.setLayout(layout_procs)

        main_layout.addWidget(widget_line)
        main_layout.addWidget(widget_procs)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)
    
    def add_procs(self, proc):
        with open("procs.json", "r") as f:
            procs = json.load(f)
        procs.update(proc)

        json.dump(procs)
        
    def get_file_name(self, label):
        filename, filetype = QFileDialog.getOpenFileName(self,
                             "Choose file",
                             ".",
                             "Executable Files(*.exe)")
        print(filename)
        self.file_name = filename.split('/')[-1]
        self.update()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
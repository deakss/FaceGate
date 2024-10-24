from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QApplication, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QLabel, QListWidget

import sys, json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        with open("current_user.json") as f:
            self.current_user = json.load(f)

        self.setWindowTitle('Face Gate')

        # LINE LAYOUT WIDGETS
        layout_line = QHBoxLayout()

        self.proc_name_line = QLabel("None selected")
        layout_line.addWidget(self.proc_name_line)
        
        proc_location = QPushButton("Open file")
        proc_location.clicked.connect(lambda: self.get_file_name())
        layout_line.addWidget(proc_location)

        add_proc = QPushButton("Add")
        add_proc.clicked.connect(self.add_procs)
        layout_line.addWidget(add_proc)

        # PROCS LAYOUT WIDGETS
        layout_procs = QVBoxLayout()

        self.procs_list_widget = QListWidget()
        self.fill_list()

        layout_procs.addWidget(self.procs_list_widget)

        self.del_proc_button = QPushButton("Delete")
        self.del_proc_button.clicked.connect(self.delete_procs)
        layout_procs.addWidget(self.del_proc_button)

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
        if self.proc_name_line.text() not in procs[self.current_user] and self.proc_name_line.text() != None and self.proc_name_line.text() != "None selected":
            procs[self.current_user].append(self.proc_name_line.text())
            self.procs_list_widget.addItem(self.proc_name_line.text())
            self.proc_name_line.setText("None selected")
        else:
            print("Такой процесс уже есть в списке!")

        with open("procs.json", "w") as f:
            json.dump(procs, f)

    def delete_procs(self):
        with open("procs.json", "r") as f:
            procs = json.load(f)
        list_items = self.procs_list_widget.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.procs_list_widget.takeItem(self.procs_list_widget.row(item))
            procs[self.current_user].remove(item.text())
            with open("procs.json", "w") as f:
                json.dump(procs, f)

    def get_file_name(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                             "Choose file",
                             ".",
                             "Executable Files(*.exe)")
        if filename != "" and filetype != "":
            self.proc_name_line.setText(filename.split('/')[-1])

    def fill_list(self):
        with open("procs.json", "r") as f:
            procs = json.load(f)

        for k, v in procs.items():
            if k == self.current_user:
                self.procs_list_widget.addItems(procs[k])

    
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
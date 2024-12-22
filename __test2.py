from PySide2 import QtWidgets
from async_assignment import async_assignment
import time

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Async Assignment Debug Example")
        self.setGeometry(100, 100, 400, 200)

        # Layout
        layout = QtWidgets.QVBoxLayout()

        # TextBox to display data
        self.textbox = QtWidgets.QLineEdit()
        layout.addWidget(self.textbox)

        # Button to start fetching data
        self.button = QtWidgets.QPushButton("Fetch Data")
        layout.addWidget(self.button)

        self.setLayout(layout)

        # Connect button
        self.button.clicked.connect(self.fetch_data)

    def fetch_data(self):
        print("Debug: Fetch Data button clicked")

        def long_task():
            print("Debug: Starting long_task")
            time.sleep(3)
            self.result = "ShotGrid Data: ABC123"
            print("Debug: Finished long_task")

        def update_ui():
            print("Debug: Updating UI")
            self.textbox.setText(self.result)

        worker = async_assignment(working=long_task, callback=update_ui)
        worker.start_async()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()

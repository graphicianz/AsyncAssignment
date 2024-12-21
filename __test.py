import sys
import time
from PySide2 import QtWidgets, QtCore
import async_assignment

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PySide2 Example")
        self.setGeometry(100, 100, 300, 100)

        # Layout
        layout = QtWidgets.QVBoxLayout()

        # Button
        self.button = QtWidgets.QPushButton("Start Working")
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def on_button_click(self):
        self.button.setEnabled(False)  # Disable button to prevent multiple clicks

        # Run the working function directly (UI may freeze)
        self.working()
        self.on_work_done()

    def working(self):
        result = sum(range(1, 1001))  # Add numbers from 1 to 1000
        time.sleep(3)  # Simulate long task
        print(f"Sum result: {result}")

    def on_work_done(self):
        self.button.setEnabled(True)  # Re-enable button
        QtWidgets.QMessageBox.information(self, "Info", "Done")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())

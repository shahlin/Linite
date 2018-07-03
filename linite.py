import sys
from PyQt5.QtWidgets import QDialog, QApplication
import main_screen


class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = main_screen.MainScreenFormUi()
        self.ui.setup_ui(self)

        # Add State Changed Listener for the Checkboxes
        for checkbox in self.ui.checkboxes_dict.values():
            checkbox.stateChanged.connect(self.ui.checkbox_state_changed)

        self.show()


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())

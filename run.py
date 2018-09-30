# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_screen.ui'
#
# Created by: PyQt5 UI code generator 5.10.1

# Make sure Python 3 is installed
import sys
if sys.version_info[0] < 3:
    print('--------------------------------------------------------------')
    print('|                                                            |')
    print('| Please use Python3 to use Linite (>=Python3.5 recommended) |')
    print('|                                                            |')
    print('--------------------------------------------------------------')
    exit()

# Make sure PyQt5 is installed
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import QMessageBox
except ImportError:
    print('--------------------------------------------------------------')
    print('|                                                            |')
    print('|    Please install python3-pyqt5 dependency to use Linite   |')
    print('|                                                            |')
    print('--------------------------------------------------------------')
    exit()

import xml.etree.ElementTree as ET
import subprocess

from download_screen import DownloadScreenFormUi


class MainScreenFormUi(QtWidgets.QWidget):
    # Parse XML file to get packages/applications info
    tree = ET.parse('package_list.xml')
    root = tree.getroot()

    # List to hold package icon labels
    icon_label_list = []

    # Dictionary to hold applications checkboxes
    checkboxes_dict = {}

    # List to hold category heading labels
    category_label_list = []

    # List to hold applications that are checked
    checked_applications_list = []

    # Number of applications selected
    selected_application_count = 0

    # Invalid distro message
    invalid_distro_msg = "Invalid distro specified"

    # Number of columns allowed in the grid
    GRID_COLUMNS = 5

    def __init__(self):

        # If the distro is not supported by Linite, do not start the application
        if self.get_package_manager(self.get_distro().rstrip()) == self.invalid_distro_msg:
            print('--------------------------------------------------------------')
            print('|                                                            |')
            print('| Unfortunately Linite does not support your Linux distro :( |')
            print('|                                                            |')
            print('--------------------------------------------------------------')
            exit()

        super().__init__()

        self.setup_ui(self)

        # Center Window
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())

        self.show()

    def setup_ui(self, main_screen_form):

        # Main screen form widget
        main_screen_form.setObjectName("main_screen_form")
        main_screen_form.resize(917, 668)
        main_screen_form.setMaximumSize(QtCore.QSize(917, 668))

        # Disable maximizing button
        main_screen_form.setWindowFlags(main_screen_form.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)

        # Set application icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/app/icons/app/logo_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main_screen_form.setWindowIcon(icon)
        main_screen_form.setStyleSheet("background-color: white;")

        # Create grid layout for main screen
        self.gridLayout_2 = QtWidgets.QGridLayout(main_screen_form)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # Create a label with logo image
        self.logo_label = QtWidgets.QLabel(main_screen_form)
        self.logo_label.setObjectName("logo_label")
        self.gridLayout_2.addWidget(self.logo_label, 0, 0, 1, 1)

        # Create a label with separator image
        self.separator_label = QtWidgets.QLabel(main_screen_form)
        self.separator_label.setObjectName("separator_label")

        # Add separator to grid
        self.gridLayout_2.addWidget(self.separator_label, 1, 0, 1, 2)

        # Create a button for 'About'
        self.about_btn = QtWidgets.QPushButton(main_screen_form)

        # Set properties for About button
        self.about_btn.setMaximumSize(QtCore.QSize(65, 16777215))
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.about_btn.setFont(font)
        self.about_btn.setStyleSheet("border:none;")

        self.about_btn.clicked.connect(self.show_about)

        # Set cursor as pointing hand when hovered over 'About'
        self.about_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.about_btn.setObjectName("about_btn")

        # Add 'About' button to grid
        self.gridLayout_2.addWidget(self.about_btn, 0, 1, 1, 1)

        # Create a scroll area to contain the list of applications
        self.apps_container = QtWidgets.QScrollArea(main_screen_form)
        self.apps_container.setStyleSheet("border:none;")
        self.apps_container.setWidgetResizable(True)
        self.apps_container.setObjectName("apps_container")

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, -213, 885, 720))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        self.apps_grid_container = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.apps_grid_container.setObjectName("apps_grid_container")

        # Start inserting categories from row 0
        category_row = 0

        # Start inserting applications from row 1
        application_row = 1

        # Loop through each category
        for category in self.root.findall('category'):
            category_name = category.get('name')

            # Start inserting applications for every category from col 0
            col = 0

            # Generic Heading Label
            self.category_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
            self.category_label.setStyleSheet("margin-top: 50px;\n"
                                              "margin-bottom: 50px;\n"
                                              "font-weight: bold;")
            self.category_label.setObjectName(category_name.lower() + "_heading_label")
            self.apps_grid_container.addWidget(self.category_label, category_row, col, 1, 3)

            self.category_label_list.append(self.category_label)

            # One row for the heading
            # Second row for icon
            # Third row for application name
            application_row += 3

            # Loop through each package in a category
            for package in self.root.findall('./category[@name="' + category_name + '"]/package'):
                # Get package manager so we can disable applications that are not supported for certain distros
                package_manager = self.get_package_manager(self.get_distro().rstrip())

                steps = ""

                try:
                    steps = package.find('commands/' + package_manager).attrib['steps']
                except AttributeError:
                    pass
                except KeyError:
                    pass

                application_name = package.find('name').text

                self.icon_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
                self.icon_label.setStyleSheet("margin-left:10px; margin-bottom:15px;")
                self.icon_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                self.icon_label.setObjectName(application_name.lower() + "_icon_label")
                self.apps_grid_container.addWidget(self.icon_label, application_row, col, 1, 1)

                self.icon_label_list.append(self.icon_label)

                self.checkbox_widget = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_2)
                self.checkbox_widget.setObjectName(application_name + "_checkbox")
                self.checkbox_widget.setStyleSheet("margin-bottom:15px;")
                self.apps_grid_container.addWidget(self.checkbox_widget, application_row + 1, col, 1, 1)

                # If the package is not available for download, disable the checkbox
                if steps == 'unavailable':
                    self.checkbox_widget.setEnabled(False)

                self.checkboxes_dict[application_name] = self.checkbox_widget

                # Add State Changed Listener for the Checkboxes(
                self.checkbox_widget.stateChanged.connect(self.checkbox_state_changed)

                # Add a column for every icon
                col += 1

                if col == self.GRID_COLUMNS:
                    col = 0
                    application_row += 2

                category_row = application_row + 2

        self.apps_container.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.addWidget(self.apps_container, 2, 0, 1, 2)

        # Create a frame to contain a label mentioning number of applications selected and download button
        self.frame = QtWidgets.QFrame(main_screen_form)

        # Set properties for the frame
        self.frame.setMinimumSize(QtCore.QSize(0, 60))
        self.frame.setStyleSheet("border: none; border-top: 1px solid #ccc;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # Create a label in the frame mentioning how many applications are selected
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(28, 22, 211, 20))
        self.label.setStyleSheet("border: none;")
        self.label.setObjectName("label")

        # Create a push button to proceed with downloading the applications
        self.proceed_btn = QtWidgets.QPushButton(self.frame)
        self.proceed_btn.setGeometry(QtCore.QRect(670, 10, 221, 41))
        self.proceed_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.proceed_btn.clicked.connect(self.confirm_download)

        self.proceed_btn_qss = """
            QPushButton#proceed_btn {
                background-color: #96989b;
                border-radius: 5px;
                color: white;
            }
            
            QPushButton#proceed_btn:hover:!pressed {
                background-color: #20873d;
            }
            
        """
        self.proceed_btn.setStyleSheet(self.proceed_btn_qss)
        self.proceed_btn.setObjectName("proceed_btn")
        self.proceed_btn.setEnabled(False)
        self.gridLayout_2.addWidget(self.frame, 3, 0, 1, 2)

        self.retranslate_ui(main_screen_form)
        QtCore.QMetaObject.connectSlotsByName(main_screen_form)

    def get_distro(self):
        name = subprocess.check_output(['./distro_name.sh'])

        # Decode bytes to string ( b'Antergos Linux\n' to Antergos Linux )
        return name.decode("utf-8")

    def get_package_manager(self, distro):
        package_managers = {
            "Arch": "pacman",
            "Arch Linux": "pacman",
            "Antergos Linux": "pacman",
            "ManjaroLinux": "pacman",
            "Debian": "apt",
            "Ubuntu": "apt"
        }

        return package_managers.get(distro, self.invalid_distro_msg)

    def checkbox_state_changed(self):
        for key, value in self.checkboxes_dict.items():
            # Do not allow duplicates
            if value.isChecked():
                if key not in self.checked_applications_list:
                    self.checked_applications_list.append(key)
            else:
                if key in self.checked_applications_list:
                    self.checked_applications_list.remove(key)

        # Update number of applications selected/checked
        self.update_selected_count()

        # Update the proceed button to be enabled or disabled according to the options selected
        self.update_proceed_btn()

    def update_selected_count(self):
        _translate = QtCore.QCoreApplication.translate

        # Number of applications selected label
        self.label.setText(
            _translate("main_screen_form", str(len(self.checked_applications_list)) + " application"
                       + ("s" if len(self.checked_applications_list) > 1 else '') + " selected"))  # Add s if plural

    def update_proceed_btn(self):
        # Enable/Disable download button depending on options selected
        if len(self.checked_applications_list) != 0:
            # Enable proceed button
            bg_color = '#29a04b'
            self.proceed_btn.setEnabled(True)
        else:
            # Disable proceed button
            bg_color = '#96989b'
            self.proceed_btn.setEnabled(False)

        # Change proceed button background color according to the state (enabled/disabled)
        self.proceed_btn.setStyleSheet(
            self.proceed_btn_qss + "QPushButton#proceed_btn {background-color: " + bg_color + ";}")

    def confirm_download(self):
        confirm_dialog = QMessageBox.question(self, "Confirm Download", 'Download '
                                              + str(len(self.checked_applications_list)) + ' application' +

                                              # Add s if plural
                                              ('s' if len(self.checked_applications_list) > 1 else '') + '?',
                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if confirm_dialog == QMessageBox.Yes:
            self.write_apps_to_file()
            self.open_download_window()
            self.close()

    def open_download_window(self):
        self.download_ui = DownloadScreenFormUi()

        # Pass the list to the next window
        self.download_ui.checked_applications_list = self.checked_applications_list.copy()
        self.download_ui.show()

    def show_about(self):
        # Display a success message box
        msg = QMessageBox()

        # Read about body from file
        with open('about.txt') as f:
            about_body = f.readline()

        msg.about(self, 'About Linite', about_body)

    def write_apps_to_file(self):
        temp_file = open(".download.txt", "a")

        for application in self.checked_applications_list:
            temp_file.write(application + "\n")

    def retranslate_ui(self, main_screen_form):
        _translate = QtCore.QCoreApplication.translate

        # Set window title
        main_screen_form.setWindowTitle(_translate("main_screen_form", "Linite"))

        # Set content for labels
        # Linite Logo label
        self.logo_label.setText(_translate("main_screen_form", "<html><head/><body><p><img "
                                                               "src=\":/app/icons/app/logo_small.png\"/></p></body"
                                                               "></html>"))

        # Separator label
        self.separator_label.setText(_translate("main_screen_form", "<html><head/><body><p><img "
                                                                    "src=\":/app/icons/app/separator.png\"/></p"
                                                                    "></body></html>"))

        # About button
        self.about_btn.setText(_translate("main_screen_form", "About"))

        j = 0
        for i, category in enumerate(self.root.findall('category')):
            category_name = category.get('name').lower()

            self.category_label_list[i].setText(_translate("main_screen_form", category_name.title()))

            for package in self.root.findall('./category[@name="' + category_name + '"]/package'):
                icon_name = package.find('icon').text
                application_name = package.find('name').text

                # Icon path as required by the .qrc
                icon_path = category_name + "/icons/" + category_name.lower() + "/" + icon_name.lower()

                # As per the .qrc, example,
                #   category_name --> internet
                #   /icons/
                #   category_name --> internet/
                #   icon_name --> chromium.png
                self.icon_label_list[j].setText(_translate("main_screen_form", "<html><head/><body><p><img src=\":/"
                                                           + icon_path + "\"/></p></body></html>"))

                self.checkboxes_dict[application_name].setText(_translate("main_screen_form", application_name.title()))

                j += 1

        # Download and Install Push Button
        self.proceed_btn.setText(_translate("main_screen_form", "Proceed"))

    @staticmethod
    def run():
        app = QtWidgets.QApplication(sys.argv)
        window = MainScreenFormUi()
        sys.exit(app.exec_())


MainScreenFormUi.run()
import assets.icons_rc

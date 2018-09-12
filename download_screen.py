# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download_screen.ui'
#
# Created by: PyQt5 UI code generator 5.10.1

import os
import subprocess
import xml.etree.ElementTree as ET
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox


class DownloadScreenFormUi(QtWidgets.QWidget):
    # Parse XML file to get packages/applications info
    tree = ET.parse('package_list.xml')
    root = tree.getroot()

    # List of selected applications
    checked_applications_list = []

    # List of installed applications
    installed_applications_list = []

    # Get total count of applications to download
    applications_count = 0

    # Variable to hold current progress value
    progress_val = 0

    # Invalid distro message
    invalid_distro_msg = "Invalid distro specified"

    def __init__(self):
        super().__init__()

        self.setup_ui(self)

        # Center Window
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())

        # Populate checked applications list
        self.populate_checked_list()

        # Delete temp file
        self.delete_temp_file()

        # Start Download
        self.download()

    def setup_ui(self, download_screen_form):

        # Download screen form widget
        download_screen_form.setObjectName("download_screen_form")
        download_screen_form.resize(917, 668)
        download_screen_form.setMinimumSize(QtCore.QSize(917, 668))

        # Set window icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/app/icons/app/logo_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        download_screen_form.setWindowIcon(icon)

        # Set background color to white
        download_screen_form.setStyleSheet("background-color: white;")

        # Add about button to the window
        self.about_btn = QtWidgets.QPushButton(download_screen_form)

        # Font object to change font style of GUI elements
        font = QtGui.QFont()

        # Set properties for the about button
        self.about_btn.setGeometry(QtCore.QRect(844, 10, 65, 50))
        self.about_btn.setMaximumSize(QtCore.QSize(65, 16777215))
        font.setFamily("Cantarell")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.about_btn.setFont(font)
        self.about_btn.setStyleSheet("border:none;")
        self.about_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.about_btn.clicked.connect(self.show_about)

        self.about_btn.setObjectName("about_btn")

        # Add logo label
        self.logo_label = QtWidgets.QLabel(download_screen_form)
        self.logo_label.setGeometry(QtCore.QRect(10, 10, 828, 50))
        self.logo_label.setObjectName("logo_label")

        # Add a label to hold the separator below the logo
        self.separator_label = QtWidgets.QLabel(download_screen_form)
        self.separator_label.setGeometry(QtCore.QRect(10, 70, 899, 15))
        self.separator_label.setObjectName("separator_label")

        # Add a progress bar widget to indicate download/install progress
        self.download_progress = QtWidgets.QProgressBar(download_screen_form)
        self.download_progress.setGeometry(QtCore.QRect(70, 240, 711, 51))
        self.download_progress.setObjectName("download_progress")

        # Add a heading label for Status
        self.status_heading_label = QtWidgets.QLabel(download_screen_form)
        self.status_heading_label.setGeometry(QtCore.QRect(70, 130, 81, 21))

        # Set properties for the above heading
        font.setFamily("Bitstream Vera Sans")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.status_heading_label.setFont(font)
        self.status_heading_label.setObjectName("status_heading_label")

        # Add a label to show the current status
        self.current_status_label = QtWidgets.QLabel(download_screen_form)
        self.current_status_label.setGeometry(QtCore.QRect(73, 190, 701, 20))
        self.current_status_label.setText("")
        self.current_status_label.setObjectName("current_status_label")

        # Add a heading label for Installed
        self.installed_heading_label = QtWidgets.QLabel(download_screen_form)
        self.installed_heading_label.setGeometry(QtCore.QRect(70, 360, 121, 30))

        # Set properties for the above heading
        font.setPointSize(16)
        self.installed_heading_label.setFont(font)
        self.installed_heading_label.setObjectName("installed_heading_label")

        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(True)
        self.check_terminal_label = QtWidgets.QLabel(download_screen_form)
        self.check_terminal_label.setGeometry(QtCore.QRect(70, 318, 221, 20))
        self.check_terminal_label.setFont(font)
        self.check_terminal_label.setObjectName("check_terminal_label")

        # Add a list widget to show list of applications installed
        self.installed_list = QtWidgets.QListWidget(download_screen_form)
        self.installed_list.setGeometry(QtCore.QRect(70, 420, 711, 221))
        self.installed_list.setObjectName("installed_list")
        self.installed_list.setSpacing(10)

        self.retranslate_ui(download_screen_form)
        QtCore.QMetaObject.connectSlotsByName(download_screen_form)

    def populate_checked_list(self):
        # Get every application from file and add it to the list
        with open(".download.txt", "r") as f:
            for line in f:
                # Get full names of applications and insert it to the list
                self.checked_applications_list.extend(line.split('\n'))

        # The list contains empty elements for some reason and I wanna sleep now, so here's a quick fix.
        # Remove empty elements from the list
        self.checked_applications_list = list(filter(lambda val: val != '', self.checked_applications_list))

        # Get the count of checked applications
        self.applications_count = len(self.checked_applications_list)

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

    def show_about(self):
        # Display a success message box
        msg = QMessageBox()

        # Read about body from file
        with open('about.txt') as f:
            about_body = f.readline()

        msg.about(self, 'About Linite', about_body)

    def download(self):
        # If no application exists in the list, show success and return
        if len(self.checked_applications_list) == 0:

            # Since it's completed, set progress bar to 100%
            self.download_progress.setValue(100)

            # Display a success message box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Download Complete!")
            msg.setWindowTitle("Information")

            # Set Button for Message Box
            msg.setStandardButtons(QMessageBox.Ok)

            # Show Message Box
            msg.exec()

            return

        # Get distro name
        # Using .rstrip() to remove the trailing \n
        distro_name = self.get_distro().rstrip()

        # Get package manager name
        package_manager = self.get_package_manager(distro_name)

        # Create a thread that runs the download
        self.download_worker = DownloadWorker()

        # Loop through checked list
        # For each application, find the application in XML file
        # Install the application using the package manager.
        # If single, then simply execute, if multiple, execute each step

        # Get pending application name
        application = self.checked_applications_list[0]

        # Set current status in GUI
        self.current_status_label.setText('Downloading and Installing ' + application)

        # Variable holding each command for applications that require multiple steps for installation
        installation_steps = []

        # Multiple of single step flag
        multiple_steps = False

        # Loop through every package in XML
        for package in self.root.iter('package'):

            command = ""

            # If the current iteration in XML matches the application
            if package.find('name').text == application:

                # Check if there are multiple steps involved
                if 'steps' in package.find('commands/' + package_manager).attrib:
                    # Check for steps
                    steps = package.find('commands/' + package_manager).attrib['steps']

                    if steps == 'multiple':

                        # Multiple step flag
                        multiple_steps = True

                        # Get list of commands from XML
                        steps_list = package.find('commands/' + package_manager)

                        for step in steps_list:
                            installation_steps.append(step.text)
                else:
                    command = package.find('commands/' + package_manager).text

                self.detailMessage = None

                # Check if detail is provided
                if 'detail' in package.find('commands/' + package_manager).attrib:
                    self.detailMessage = package.find('commands/' + package_manager).attrib['detail']

                # Set variables
                if multiple_steps is True:
                    self.download_worker.command = installation_steps
                else:
                    self.download_worker.command = command

                self.download_worker.application_name = application

                self.download_worker.download_signal.connect(self.show_download_completed)

                # When the thread has finished running, call the download_finished function
                # which will start downloading the next application if any
                self.download_worker.finished.connect(self.download_finished)

                # Start the thread
                self.download_worker.start()

                return

    def download_finished(self):
        """
            Remove the downloaded list from the checked_applications_list
            and start downloading the next application
        """

        self.checked_applications_list.pop(0)
        self.download()

    def show_download_completed(self, application_name):
        # Show download complete when the application finishes downloading
        self.current_status_label.setText('Download and Install Complete')

        # Check if the item has a detail
        if self.detailMessage is not None:
            # Add to the list of installed applications with the detail
            item = QListWidgetItem(application_name + " (" + self.detailMessage + ")")
        else:
            # Add to the list of installed applications without the detail
            item = QListWidgetItem(application_name)

        self.installed_list.addItem(item)

        progress_div = round(100 / self.applications_count)
        self.progress_val += progress_div

        self.download_progress.setValue(self.progress_val)

    def delete_temp_file(self):
        temp_file = ".download.txt"

        # Check if file exists
        if os.path.isfile(temp_file):
            # Delete file
            os.remove(temp_file)
        else:
            print("Error: File not found")

    def retranslate_ui(self, download_screen_form):
        _translate = QtCore.QCoreApplication.translate

        # Window title
        download_screen_form.setWindowTitle(_translate("download_screen_form", "Linite"))

        # about button
        self.about_btn.setText(_translate("download_screen_form", "About"))

        # Logo label
        self.logo_label.setText(_translate("download_screen_form", "<html><head/><body><p><img "
                                                                   "src=\":/app/icons/app/logo_small.png\"/></p"
                                                                   "></body></html>"))

        # Status heading label
        self.status_heading_label.setText(_translate("download_screen_form", "Status"))

        # Separator label
        self.separator_label.setText(_translate("download_screen_form", "<html><head/><body><p><img "
                                                                        "src=\":/app/icons/app/separator.png\"/></p"
                                                                        "></body></html>"))

        # Check terminal for details label
        self.check_terminal_label.setText(_translate("download_screen_form", "[Check terminal for details]"))

        # Installed heading label
        self.installed_heading_label.setText(_translate("download_screen_form", "Installed"))


class DownloadWorker(QThread):

    download_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.command = None
        self.application_name = ""

    def run(self):
        if isinstance(self.command, str):
            # Run single command
            subprocess.call(self.command.split())
        elif isinstance(self.command, list):
            # Run multiple commands
            for each_command in self.command:
                # Run each command
                subprocess.call(each_command, shell=True)

        # When the command has finished running
        self.download_signal.emit(self.application_name)


import assets.icons_rc

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download_screen.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import os
import subprocess
import threading
import xml.etree.ElementTree as ET
from PyQt5 import QtCore, QtGui, QtWidgets


class DownloadScreenFormUi(QtWidgets.QWidget):
    # Parse XML file to get packages/applications info
    tree = ET.parse('package_list.xml')
    root = tree.getroot()

    # List of selected applications
    checked_applications_list = []

    def __init__(self):
        super().__init__()
        self.setup_ui(self)

        # Center Window
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())

        # Populate checked applications list
        self.populate_checked_list()

        # Delete temp file
        self.delete_temp_file()

        # Show window
        self.show()

        # Start download
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

        # Add about label to the window
        self.about_label = QtWidgets.QLabel(download_screen_form)

        # Set properties for the about label
        self.about_label.setGeometry(QtCore.QRect(844, 10, 65, 50))
        self.about_label.setMaximumSize(QtCore.QSize(65, 16777215))
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.about_label.setFont(font)
        self.about_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.about_label.setObjectName("about_label")

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
        self.download_progress.setMinimum(0)
        self.download_progress.setMaximum(0)
        self.download_progress.setObjectName("download_progress")

        # Add a heading label for Status
        self.status_heading_label = QtWidgets.QLabel(download_screen_form)
        self.status_heading_label.setGeometry(QtCore.QRect(70, 130, 81, 21))

        # Set properties for the above heading
        font = QtGui.QFont()
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
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.installed_heading_label.setFont(font)
        self.installed_heading_label.setObjectName("installed_heading_label")
        self.installed_list = QtWidgets.QListView(download_screen_form)
        self.installed_list.setGeometry(QtCore.QRect(70, 410, 721, 211))
        self.installed_list.setObjectName("installed_list")

        self.retranslate_ui(download_screen_form)
        QtCore.QMetaObject.connectSlotsByName(download_screen_form)

    def populate_checked_list(self):
        temp_file = open(".download.txt", "r")

        # Get every application from file and add it to the list
        with open(".download.txt", "r") as f:
            for line in f:
                self.checked_applications_list.extend(line.split())

    def get_distro(self):
        name = subprocess.check_output(['./distro_name.sh'])

        # Decode bytes to string ( b'Antergos Linux\n' to Antergos Linux)
        return name.decode("utf-8")

    def get_package_manager(self, distro):
        package_managers = {
            "Antergos Linux": "pacman"
        }

        return package_managers.get(distro, "Invalid distro specified")

    def download(self):
        # Get distro name
        # Using .rstrip() to remove the trailing \n
        distro_name = self.get_distro().rstrip()

        # Get package manager name
        package_manager = self.get_package_manager(distro_name)

        # Loop through checked list
        # For each application, find the application in XML file
        # Install the application using the package manager.
        # If single, then simply execute, if multiple, execute each

        for application in self.checked_applications_list:
            # Loop through every package
            for package in self.root.iter('package'):

                command = ""

                # If the current iteration in XML matches the application
                if package.find('name').text == application:
                    # Get the command
                    if package_manager == 'pacman':
                        # Check for steps
                        steps = package.find('commands/' + package_manager).attrib['steps']

                        if steps == 'single':
                            # Single step
                            command = package.find('commands/' + package_manager + '/step').text
                        elif steps == 'multiple':
                            # Multiple steps
                            pass

                    else:
                        command = package.find('commands/' + package_manager).text


                    # Create a thread that runs the download
                    import threading
                    download_thread = threading.Thread(target=self.run_download_command, args=[command.split()])
                    download_thread.start()



    def delete_temp_file(self):
        temp_file = ".download.txt"

        # Check if file exists
        if os.path.isfile(temp_file):
            # Delete file
            os.remove(temp_file)
        else:
            print("Error: File not found")

    def run_download_command(self, command):
        # Run command
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        out, err = process.communicate()

        print(out)

    def retranslate_ui(self, download_screen_form):
        _translate = QtCore.QCoreApplication.translate

        # Window title
        download_screen_form.setWindowTitle(_translate("download_screen_form", "Linite"))

        # About label
        self.about_label.setText(_translate("download_screen_form", "About"))

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

        # Installed heading label
        self.installed_heading_label.setText(_translate("download_screen_form", "Installed"))

import assets.icons_rc

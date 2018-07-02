# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_screen.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import xml.etree.ElementTree as ET


class MainScreenFormUi(object):
    # Parse XML file to get packages/applications info
    tree = ET.parse('package_list.xml')
    root = tree.getroot()

    # List to hold package icon labels
    icon_label_list = []

    # List to hold package checkboxes
    checkboxes_list = []

    # List to hold category heading labels
    category_label_list = []

    # Number of columns allowed in the grid
    GRID_COLUMNS = 5

    def setup_ui(self, main_screen_form):

        # Main screen form widget
        main_screen_form.setObjectName("main_screen_form")
        main_screen_form.resize(917, 668)
        main_screen_form.setMaximumSize(QtCore.QSize(917, 668))

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

        # Create a label for 'About'
        self.about_label = QtWidgets.QLabel(main_screen_form)

        # Set properties for About label
        self.about_label.setMaximumSize(QtCore.QSize(65, 16777215))
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.about_label.setFont(font)

        # Set cursor as pointing hand when hovered over 'About'
        self.about_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.about_label.setObjectName("about_label")

        # Add 'About' label to grid
        self.gridLayout_2.addWidget(self.about_label, 0, 1, 1, 1)

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

        for category in self.root.findall('category'):
            category_name = category.get('name')
            print("Category Row : " + str(category_row))

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

            application_row += 3

            for package in self.root.findall('./category[@name="' + category_name + '"]/package'):
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

                self.checkboxes_list.append(self.checkbox_widget)

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
        self.download_btn = QtWidgets.QPushButton(self.frame)
        self.download_btn.setGeometry(QtCore.QRect(670, 10, 221, 41))
        self.download_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.download_btn.setStyleSheet("QPushButton#download_btn {\n"
                                        "    background-color: #29a04b;\n"
                                        "    border-radius: 5px;\n"
                                        "    color: white;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton#download_btn:hover:!pressed {\n"
                                        "    background-color: #20873d;\n"
                                        "}")
        self.download_btn.setObjectName("download_btn")
        self.gridLayout_2.addWidget(self.frame, 3, 0, 1, 2)

        self.retranslate_ui(main_screen_form)
        QtCore.QMetaObject.connectSlotsByName(main_screen_form)

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

        # About label
        self.about_label.setText(_translate("main_screen_form", "About"))

        print(len(self.icon_label_list))

        j = 0
        for i, category in enumerate(self.root.findall('category')):
            category_name = category.get('name').lower()
            print("\nCategory: " + category_name)

            self.category_label_list[i].setText(_translate("main_screen_form", category_name.title()))

            for package in self.root.findall('./category[@name="' + category_name + '"]/package'):
                icon_path = package.find('icon').text
                application_name = package.find('name').text

                self.icon_label_list[j].setText(_translate("main_screen_form", "<html><head/><body><p><img "
                                                           "src=\":/" + category_name + "/icons/" +
                                                           icon_path + "\"/></p></body></html>"))
                self.checkboxes_list[j].setText(_translate("main_screen_form", application_name.title()))
                print("Icon: " + icon_path)

                j += 1

        # Number of applications selected label
        self.label.setText(_translate("main_screen_form", "# application(s) selected"))

        # Download and Install Push Button
        self.download_btn.setText(_translate("main_screen_form", "Download and Install"))

import assets.icons_rc
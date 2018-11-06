# Linite
**Linite** is a Linux based application that allows users to easily select the applications they want and download & install them with just a click of a button. Typically, the user would have to go over each application's website, download the package and install it themself. Linite eases this process. Also it downloads the latest packages from the operating system's official repository so the user gets the latest version at all times.

Linite is inspired by Ninite, a similar program available on Windows platform. Since Ninite was no longer supported on Linux, I decided to build one for Linux myself. Even though there are many package managers on Linux, I wanted to create something that lets users install their essential applications with a very simple and minimal design. It is still in its early stages, so go easy on me if you find any bugs. :)

## Supported Linux Distributions
- Arch Linux based distros
- Antergos Linux
- Manjaro Linux
- Ubuntu based distros
- Debian

## Usage
Before you run the application, make sure you have the following dependencies installed:
- python3
- python3-pyqt5

Once you've got these dependencies installed, run the following command on your **terminal**:
```bash
sudo python3 run.py
```
##### **NOTE: Make sure to run the command with sudo**
There will be a password prompt upon running the command. Linite will open once you enter your password. You can select the applications you want to install and click on **Proceed**.

## Screenshots
#### Main Screen
![alt text](https://i.imgur.com/FuVve0X.png "Main screen")

#### Download Screen
![alt text](https://i.imgur.com/GuY4YZn.png "Download screen")

## For Developers
### Basic requirements
- Python 3
- PyQt5
- Qt5 Designer for GUI

### Flow
#### run.py
- The **run.py** is the entry point of the application.
- When the file is run, first the program checks if python3 and pyqt5 is installed and if the linux distro is supported. To check the user's distro, a shell script is run. If the output of this shell script is found in the given list of supported distros, the program's user interface is run.
- Users can now select/check the applications they want to download and install. Once the selections are made, the proceed button is pressed and confirmed, the list of selected applications are saved to a temporary file called **.download.txt** and the download window is displayed (and previous screen hidden).
#### download_screen.py
- When the download window is displayed, first the list of applications are stored in a python list called **checked_applications_list**. Second, the temporary **.download.txt** file is deleted. Finally, the download is started by calling the **download** method.
- The download method creates a thread in order to keep the application responsive while the applications are being downloaded and installed. But the thread still waits for one application to finish its download and only then does it start downloading the next application in the list.
- Once a thread is done with downloading and installing an application, it pops the first element from the list and calls download method again. **The download method always downloads the first application in the list**
- As and when an application is downloaded and installed, it is added to the list of completed applications.
- After every application is downloaded and installed, a success dialog is displayed.

## Application structure and layout
### Structure
All the applications' information are stored in **package_list.xml**. The XML document contains information such as the category the application belongs to, its name, its icon location, the commands used to download them, etc. Below is an example of a browser application named TestBrowser in the XML document.

```XML
<packages>
    <category name="internet">
        <package>
            <name>TestBrowser</name>
            <icon>testbrowser.png</icon>
            <commands>
                <pacman>sudo pacman -S --noconfirm testbrowser</pacman>
                <apt>sudo apt install -y testbrowser</apt>
            </commands>
        </package>
        .
        .
        . <!-- MORE PACKAGES IN INTERNET CATEGORY -->
    </category>
    .
    .
    . <!-- MORE CATEGORIES -->
</packages>
```

**NOTE: Any application that has** `steps="unavailable"` **in its package manager element will not be available for download and will be greyed out (disabled) for a distro using that package manager**

**NOTE: To show any detail/message in the list view after an application is downloaded, you can add the attribute** `detail="some information"` **in its package manager element**

### Graphical User Interface
The application parses the XML document using the **xml.etree.ElementTree** library. Linite uses a grid layout to display the list of applications.
- It first loops through the applications in the first category.
- Gets the category name and displays as a heading (Label) on the screen.
- Next, it loops through each package in the category, gets their information and outputs it accordingly.
- And so on for every category.
 
The great thing about this is, if you want to add a new application to the list, the python code doesn't have to be touched at all. Just add it to the XML file with appropriate values and you're done. However, if you're using an icon, you need to make sure to update the **.qrc** using Qt5 Designer and run the **pyrcc5** command (name it icons_rc.py and put it in the assets folder). Also, to convert a GUI made in Qt5 Designer to python, you need to run the **pyuic5** command.

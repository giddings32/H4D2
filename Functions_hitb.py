#!/usr/bin/env python3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import *
import time
import subprocess

widgets = {
    "logo": [],
    "button_enter": [],
    "text_box": [],
    "text_box_preview": [],
    "tool_select": [],
    "tool_options": [],
    "info": [],
    "flag": [],
    "list3": [],
    "button_run": [],
    "rhosts": [],
    "interface": []
}

data = {
    "Nmap": ["FullScan+", "S1 Option2", "S1 Option3"],
    "Select2": ["S2 Option1", "S2 Option2", "S2 Option3", "S2 Option4", "S2 Option5", "S2 Option6"],
    "Select3": ["S3 Option1", "S3 Option2", "S3 Option3", "S3 Option4", "S3 Option5", "S3 Option 6", "S3 Option7",
                "S3 Option8", "S3 Option9", "S3 Option10"],
    "Select4": ["S4 Option1", "S4 Option2", "S4 Option3"]
}

target = {
    "eth0": ["192.168.153.21", "192.168.153.24", "192.168.153.24"],
    "eth1": ["192.168.110.5", "192.168.110.14", "192.168.110.42"],
    "tun0": ["10.10.10.3", "10.10.10.16", "10.10.10.184", "10.10.10.245"]

}

grid = QGridLayout()


def clear_widgets():
    for widget in widgets:
        if widgets[widget]:
            widgets[widget][-1].hide()
            for i in range(0, len(widgets[widget])):
                widgets[widget].pop()


def frame1_button():
    clear_widgets()
    frame2()


def frame2_button():
    clear_widgets()
    frame1()


def frame1():
    QGridLayout()
    image = QPixmap("./logo2.png")
    image.scaled(20, 20, QtCore.Qt.KeepAspectRatio)
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    widgets["logo"].append(logo)

    button_enter = QPushButton("Enter", )
    button_enter.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button_enter.setStyleSheet(
        "*{border: 4px solid '#20C20e';" +
        "border-radius: 10px;" +
        "font-size: 20px;" +
        "color: 'white';" +
        "font-style: 'bold';" +
        "padding: 10px;" +
        "margin: 10px 600px;}" +
        "*:hover{background: '#20C20e';}"
    )

    button_enter.clicked.connect(frame1_button)
    widgets["button_enter"].append(button_enter)
    grid.addWidget(logo, 2, 7, 4, 6)
    grid.addWidget(button_enter, 8, 8, 1, 4)


def frame2():
    # ---
    # find_interface = subprocess.getoutput("ifconfig | grep flags | cut -d ':' -f 1")
    # ---
    button_run = QPushButton("Run", )
    button_run.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button_run.setStyleSheet(
        "*{border: 4px solid '#20C20e';" +
        "border-radius: 10px;" +
        "font-size: 20px;" +
        "color: 'white';" +
        "font-style: 'bold';}" +
        "*:hover{background: '#20C20e';}"
    )

    button_run.clicked.connect(frame2_button)
    widgets["button_run"].append(button_run)

    tool_select = QComboBox()
    model = QStandardItemModel()
    tool_select.setEditable(True)
    tool_select.lineEdit().setReadOnly(True)
    tool_select.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
    tool_select.setModel(model)
    tool_select.setStyleSheet(
        "*{border: 4px solid '#20C20e';" +
        "border-radius: 10px;" +
        "font-size: 20px;" +
        "color: 'white';" +
        "font-style: 'bold';}"
    )
    widgets["tool_select"].append(tool_select)

    tool_options = QComboBox()
    tool_options.setEditable(True)
    tool_options.lineEdit().setReadOnly(True)
    tool_options.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
    tool_options.setModel(model)
    tool_options.setStyleSheet(
        "*{border: 4px solid '#20C20e';" +
        "border-radius: 10px;" +
        "font-size: 20px;" +
        "color: 'white';" +
        "font-style: 'bold';}"
    )

    for k, v in data.items():
        select = QStandardItem(k)
        model.appendRow(select)
        for value in v:
            options = QStandardItem(value)
            select.appendRow(options)

    def update_tools(index):
        indx = model.index(index, 0, tool_select.rootModelIndex())
        tool_options.setRootModelIndex(indx)
        tool_options.setCurrentIndex(0)

    tool_select.currentIndexChanged.connect(update_tools)
    update_tools(0)

    interface = QComboBox()
    model = QStandardItemModel()
    interface.setEditable(True)
    interface.lineEdit().setReadOnly(True)
    interface.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
    interface.setModel(model)
    interface.setStyleSheet(
        "*{border: 4px solid '#20C20e';" +
        "border-radius: 10px;" +
        "font-size: 20px;" +
        "color: 'white';" +
        "font-style: 'bold';}"
    )
    widgets["interface"].append(interface)

    rhosts = QComboBox()
    rhosts.setEditable(True)
    rhosts.lineEdit().setReadOnly(True)
    rhosts.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
    rhosts.setModel(model)
    rhosts.setStyleSheet(
        "*{border: 4px solid '#20C20e';" +
        "border-radius: 10px;" +
        "font-size: 20px;" +
        "color: 'white';" +
        "font-style: 'bold';}"
    )
    widgets["rhosts"].append(rhosts)

    for k, v in target.items():
        interface_key = QStandardItem(k)
        model.appendRow(interface_key)
        for value in v:
            rhost_value = QStandardItem(value)
            interface_key.appendRow(rhost_value)

    def update_rhosts(index):
        dex = model.index(index, 0, interface.rootModelIndex())
        rhosts.setRootModelIndex(dex)
        rhosts.setCurrentIndex(0)

    interface.currentIndexChanged.connect(update_rhosts)
    update_rhosts(0)

    while True:
        tool_options.update()
        QApplication.processEvents()
        if tool_options.currentText() == "FullScan+":
            flag = QLabel(
                "\n-sV\n\n" +
                "-n\n\n" +
                "-v\n\n" +
                "-Pn\n\n" +
                "-p-\n\n" +
                "-T4\n\n" +
                "-A\n\n" +
                "--open"
            )
            flag.setAlignment(QtCore.Qt.AlignTop)
            flag.setAlignment(QtCore.Qt.AlignHCenter)
            flag.setStyleSheet(
                "*{border: 4px solid '#20C20e';" +
                "border-radius: 10px;" +
                "font-size: 15px;" +
                "color: 'white';" +
                "font-style: 'bold';}" +
                ""
            )

            info = QLabel(
                "\n probe open ports to determine service/version info\n\n" +
                " (No DNS resolution)\n\n" +
                " (Increase verbosity level)\n\n" +
                " Treat All hosts as online --skip host discovery\n\n" +
                " scan ports from 1 through 65535\n\n" +
                " (Set Timing Template) 0 Paronoid | 1 Sneaky | 2 Polite | 3 Normal | 4 Aggressive | 5 Insane\n\n" +
                " Enables OS detection (-O), Version scanning (-sV), Script scanning (-sC), and Traceroute ("
                " --traceroute)\n\n" +
                " Only show open (or possibly open) ports"
            )
            info.setAlignment(QtCore.Qt.AlignTop)
            info.setStyleSheet(
                "*{border: 4px solid '#20C20e';" +
                "border-radius: 10px;" +
                "font-size: 15px;" +
                "color: 'white';" +
                "font-style: 'bold';}" +
                ""
            )
            widgets["info"].append(info)
            widgets["flag"].append(flag)

            text_box_preview = QLineEdit()
            #host = subprocess.getoutput("whoami")
            text_box_preview.setPlaceholderText("nmap -sV -n -v -Pn -p- -T4 -A --open 192.168.153.21 ")
            text_box_preview.setStyleSheet(
                "*{border: 4px solid '#20C20e';" +
                "border-radius: 10px;" +
                "font-size: 20px;" +
                "color: 'white';" +
                "font-style: 'bold';}"
            )
            widgets["text_box_preview"].append(text_box_preview)

            text_box = QLineEdit()
            text_box.setPlaceholderText("")
            text_box.setStyleSheet(
                "*{border: 4px solid '#20C20e';" +
                "border-radius: 10px;" +
                "background:transparent;" +
                "font-size: 20px;" +
                "color: '#20C20e';" +
                "font-style: 'bold';}"

            )
            widgets["text_box"].append(text_box)

        else:
            flag = QLabel(
                "\nPlaceHolder Text\n\n"
            )
            flag.setAlignment(QtCore.Qt.AlignTop)
            flag.setAlignment(QtCore.Qt.AlignHCenter)
            flag.setStyleSheet(
                "*{border: 4px solid '#20C20e';" +
                "border-radius: 10px;" +
                "font-size: 15px;" +
                "color: 'white'-sV;" +
                "font-style: 'bold';}" +
                ""
            )

            info = QLabel(
                "\nPlaceHolder Text\n\n"
            )
            info.setAlignment(QtCore.Qt.AlignTop)
            info.setStyleSheet(
                "*{border: 4px solid '#20C20e';" +
                "border-radius: 10px;" +
                "font-size: 15px;" +
                "color: 'white';" +
                "font-style: 'bold';}" +
                ""
            )
            widgets["info"].append(info)
            widgets["flag"].append(flag)

            text_box_preview = QLineEdit()
            text_box_preview.setPlaceholderText("Type Over This Text ")
            text_box_preview.setStyleSheet(
                "*{border: 4px solid '#20C20e';" +
                "border-radius: 10px;" +
                "font-size: 20px;" +
                "color: 'white';" +
                "font-style: 'bold';}"
            )
            widgets["text_box_preview"].append(text_box_preview)

            text_box = QLineEdit()
            text_box.setPlaceholderText("Type Over This Text")
            text_box.setStyleSheet(
                "*{border: 4px solid '#20C20e';" +
                "border-radius: 10px;" +
                "background:transparent;" +
                "font-size: 20px;" +
                "color: '#20C20e';" +
                "font-style: 'bold';}"

            )
            widgets["text_box"].append(text_box)

        # Top line 0,*,1,*
        grid.addWidget(tool_select, 0, 0, 1, 4)
        grid.addWidget(tool_options, 0, 4, 1, 8)
        grid.addWidget(interface, 0, 12, 1, 3)
        grid.addWidget(rhosts, 0, 15, 1, 5)

        grid.addWidget(flag, 1, 0, 8, 2)
        grid.addWidget(info, 1, 2, 8, 18)
        grid.addWidget(text_box_preview, 9, 0, 1, 17)
        grid.addWidget(text_box, 9, 0, 1, 17)
        grid.addWidget(button_run, 9, 17, 1, 3)

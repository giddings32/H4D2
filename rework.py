#!/usr/bin/env python3
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import subprocess

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.widgets = {}
        self.lhost = ""

        # Create home page
        self.home_page = QWidget()
        
        #create QLabel and set its pixmap
        self.image = QLabel()
        self.image.setPixmap(QPixmap("/opt/H4D2/logo2.png"))
        self.image.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.show_main_page)

        # create a main layout 
        layout = QVBoxLayout()
        # create a horizontal layout for the image
        layout.addStretch()
        layout.addWidget(self.image, 0, Qt.AlignCenter)
        layout.addStretch()
        # create a vertical layout for the button
        self.start_button.setFixedSize(150,50)
        self.start_button.setStyleSheet("QPushButton { border: 2px solid green; }"
                                "QPushButton:hover { background-color: green;}")
        layout.addWidget(self.start_button, 0, Qt.AlignBottom | Qt.AlignCenter)
        layout.addStretch()

        self.home_page.setLayout(layout)
        self.stacked_widget.addWidget(self.home_page)

        # Create main page
        self.main_page = QWidget()
        
        # Set up the user interface
        self.setStyleSheet('background: #161219;')
        self.setWindowTitle('H4D2')
        self.setGeometry(1200, 0, 1000, 600)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.tabBar().setStyleSheet("QTabBar::tab:selected { background-color: #20C20E}")

        # Create tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tabs.addTab(self.tab1, "Initial Recon")
        self.tabs.addTab(self.tab2, "HTTPHelper")
        self.tabs.addTab(self.tab3, "Linux Priv Esc")
        self.tabs.addTab(self.tab4, "Windows Priv Esc")
        self.tabs.addTab(self.tab5, "TTY Shell Breakout")
        self.tabs.currentChanged.connect(self.tabChanged)

        # Create a horizontal layout for the Lhost label and dropdown
        self.lhost_layout = QHBoxLayout()
        self.lhost_label = QLabel("Lhost:")
        self.lhost_label.setStyleSheet("color: 'white'; font-size: 16px;")
        self.lhost_combo = QComboBox()
        self.lhost_combo.setFixedWidth(100) #set width of the dropdown
        self.lhost_combo.activated[str].connect(self.onActivated)
        self.lhost_layout.addStretch()
        
        # Get the list of available interfaces
        interfaces = subprocess.check_output("ip link show", shell=True)
        interface_list = interfaces.decode().split("\n")

        # Extract the interface names and add them to the dropdown
        for interface in interface_list:
            if ": <" in interface:
                self.lhost_combo.addItem(interface.split(":")[1].strip())

        # Add dropdown and labels to layout
        self.lhost_layout.addWidget(self.lhost_label)
        self.lhost_layout.addWidget(self.lhost_combo)
        layout = QVBoxLayout()
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.lhost_layout)
        main_layout.addWidget(self.tabs)
        self.main_page.setLayout(main_layout)
        self.stacked_widget.addWidget(self.main_page)


    def onActivated(self, text):
        # Get the IP associated with the selected interface
        ip = subprocess.check_output("ip addr show " + text + " | grep 'inet ' | awk '{print $2}' | cut -d/ -f1", shell=True)
        self.lhost = ip.decode().strip()
        self.lhost_label.setText("Lhost: " + self.lhost)


    def show_main_page(self):
    	self.stacked_widget.setCurrentWidget(self.main_page)

    def create_divider(self):
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setLineWidth(3)
        divider.setStyleSheet("color: #20C20E;")
        return divider

    def tabChanged(self, text):
        self.lhost = ""
        current_tab = self.tabs.currentIndex()
        if current_tab == 0:
            self.httphelper()
        elif current_tab == 1:
            self.httphelper()
        elif current_tab == 2:
            self.httphelper()
        elif current_tab == 3:
            self.httphelper
        elif current_tab == 4:
            self.httphelper


    def httphelper(self):
        self.tab2.layout = QVBoxLayout()
        self.scroll = QScrollArea()
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container.setLayout(self.container_layout)
        self.scroll.setWidget(self.container)
        self.scroll.setWidgetResizable(True)
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.container_layout.setContentsMargins(0,0,0,0)
        self.container.adjustSize()
        spacer = QSpacerItem(0, 25)
        divider = self.create_divider()
        self.tab2.layout.addWidget(self.scroll)
        self.tab2.setLayout(self.tab2.layout)
        
        Nmap = QLabel("[+ Nmap]")
        Nmap.setStyleSheet(
            "color: #20C20E;" +
            "font-size: 20px;" +
            "font-style: 'bold';"
        )
        self.container_layout.addWidget(Nmap)
        
        nmap_Scan1 = QLabel(f"nmap -p- -sT -sV -A  {self.lhost}")
        nmap_Scan1.setStyleSheet(
            "color: 'white';" +
            "font-size: 20px;" +
            "font-style: 'bold';" 
        )
        self.container_layout.addWidget(nmap_Scan1)
        
        copy_button = QPushButton()
        copy_button.setIcon(QIcon.fromTheme("edit-copy"))
        copy_button.setFixedSize(QSize(20,20))
        copy_button.clicked.connect(lambda: QApplication.clipboard().setText(nmap_Scan1.text()))
        copy_button.setStyleSheet(
            "*:hover{background: '#20C20e';}"
        ) 
        label_layout = QHBoxLayout()
        label_layout.addWidget(copy_button)
        label_layout.addWidget(nmap_Scan1)
        self.container_layout.addLayout(label_layout)
        
        run_button = QPushButton()
        run_button.setIcon(QIcon.fromTheme("media-playback-start"))
        run_button.setFixedSize(QSize(20,20))
        command1 = nmap_Scan1.text() + "; bash"
        run_button.clicked.connect(lambda: subprocess.Popen(["/usr/bin/terminator", "--new-tab", "-e", command1]))
        run_button.setStyleSheet(
            "*:hover{background: '#20C20e';}"
        )    
        label_layout = QHBoxLayout()
        label_layout.addWidget(copy_button)
        label_layout.addWidget(run_button)
        label_layout.addWidget(nmap_Scan1)
        self.container_layout.addLayout(label_layout)
        self.container_layout.addStretch()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

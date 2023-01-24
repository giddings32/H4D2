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
        self.start_button.clicked.connect(self.recon)
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
        self.lhost = "127.0.0.1"
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
        self.lhost_combo.setCurrentIndex(0)
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
        self.tabChanged(text)

        
    def show_main_page(self):
    	self.stacked_widget.setCurrentWidget(self.main_page)

    def tabChanged(self, text):
        current_tab = self.tabs.currentIndex()
        if current_tab == 0:
            self.recon()
        elif current_tab == 1:
            self.httphelper()
        elif current_tab == 2:
            self.lpe()
        elif current_tab == 3:
            self.wpe()
        elif current_tab == 4:
            self.tty()


    def recon(self):
        rhost = "127.0.0.1"
        if not hasattr(self, 'tab1_container'):
            self.tab1_container = QWidget()
            self.tab1_container_layout = QVBoxLayout(self.tab1_container)
            self.tab1_container.setLayout(self.tab1_container_layout)
            self.scroll = QScrollArea()
            self.scroll.setWidget(self.tab1_container)
            self.scroll.setWidgetResizable(True)
            self.tab1_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.tab1_container_layout.setContentsMargins(0,0,0,0)
            self.tab1_container.adjustSize()
            
            self.tab1.setLayout(QVBoxLayout())
            self.tab1.layout().addWidget(self.scroll)
        # nmap
        if hasattr(self, 'nmap'):
            self.tab1_container_layout.removeWidget(self.nmap)
            self.nmap.deleteLater()
        self.nmap = QLabel("[+ Nmap]")
        self.nmap.setStyleSheet(
            "color: #20C20E;" +
            "font-size: 20px;" +
            "font-style: 'bold';"
        )
        self.tab1_container_layout.insertWidget(0,self.nmap)

        # nmap Scan1
        if hasattr(self, 'nmap_Scan1'):
            self.tab1_container_layout.removeWidget(self.nmap_Scan1)
            self.nmap_Scan1.deleteLater()
        self.nmap_Scan1 = QLabel(f"nmap -p- -sT -sV -A  {self.lhost}")
        self.nmap_Scan1.setStyleSheet(
            "color: 'white';" +
            "font-size: 20px;" +
            "font-style: 'bold';" 
            )

        # nmap_Scan1 copy button
        if hasattr(self, 'nmap_Scan1_Copy'):
            self.tab1_container_layout.removeWidget(self.nmap_Scan1_Copy)
            self.nmap_Scan1_Copy.deleteLater()
        self.nmap_Scan1_Copy = QPushButton()
        self.nmap_Scan1_Copy.setIcon(QIcon.fromTheme("edit-copy"))
        self.nmap_Scan1_Copy.setFixedSize(QSize(20,20))
        self.nmap_Scan1_Copy.clicked.connect(lambda: QApplication.clipboard().setText(self.nmap_Scan1.text()))
        self.nmap_Scan1_Copy.setStyleSheet(
            "*:hover{background: '#20C20e';}"
        )

        # nmap_Scan1 run button
        if hasattr(self, 'nmap_Scan1_Run'):
            self.tab1_container_layout.removeWidget(self.nmap_Scan1_Run)
            self.nmap_Scan1_Run.deleteLater()
        self.nmap_Scan1_Run = QPushButton()
        self.nmap_Scan1_Run.setIcon(QIcon.fromTheme("media-playback-start"))
        self.nmap_Scan1_Run.setFixedSize(QSize(20,20))
        command1 = self.nmap_Scan1.text() + "; bash"
        self.nmap_Scan1_Run.clicked.connect(lambda: subprocess.Popen(["/usr/bin/terminator", "--new-tab", "-e", command1]))
        self.nmap_Scan1_Run.setStyleSheet(
            "*:hover{background: '#20C20e';}"
        )

        # nmap_Scan1 adding widgets
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.nmap_Scan1_Copy)
        label_layout.addWidget(self.nmap_Scan1_Run)
        label_layout.addWidget(self.nmap_Scan1)
        self.tab1_container_layout.insertLayout(1, label_layout)
        self.tab1_container_layout.addStretch()

        # nmap Scan2
        if hasattr(self, 'nmap_Scan2'):
            self.tab1_container_layout.removeWidget(self.nmap_Scan2)
            self.nmap_Scan2.deleteLater()
        self.nmap_Scan2 = QLabel(f"nmap -p- -sC -sV {rhost} --open") 
        self.nmap_Scan2.setStyleSheet(
            "color: 'white';" +
            "font-size: 20px;" +
            "font-style: 'bold';" 
            )

        # nmap_Scan2 copy button
        if hasattr(self, 'nmap_Scan2_Copy'):
            self.tab1_container_layout.removeWidget(self.nmap_Scan2_Copy)
            self.nmap_Scan2_Copy.deleteLater()
        self.nmap_Scan2_Copy = QPushButton()
        self.nmap_Scan2_Copy.setIcon(QIcon.fromTheme("edit-copy"))
        self.nmap_Scan2_Copy.setFixedSize(QSize(20,20))
        self.nmap_Scan2_Copy.clicked.connect(lambda: QApplication.clipboard().setText(self.nmap_Scan2.text()))
        self.nmap_Scan2_Copy.setStyleSheet(
            "*:hover{background: '#20C20e';}"
        )

        # nmap_Scan2 run button
        if hasattr(self, 'nmap_Scan2_Run'):
            self.tab1_container_layout.removeWidget(self.nmap_Scan2_Run)
            self.nmap_Scan2_Run.deleteLater()
        self.nmap_Scan2_Run = QPushButton()
        self.nmap_Scan2_Run.setIcon(QIcon.fromTheme("media-playback-start"))
        self.nmap_Scan2_Run.setFixedSize(QSize(20,20))
        command1 = self.nmap_Scan2.text() + "; bash"
        self.nmap_Scan2_Run.clicked.connect(lambda: subprocess.Popen(["/usr/bin/terminator", "--new-tab", "-e", command1]))
        self.nmap_Scan2_Run.setStyleSheet(
            "*:hover{background: '#20C20e';}"
        )

        # nmap_Scan2 adding widgets
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.nmap_Scan2_Copy)
        label_layout.addWidget(self.nmap_Scan2_Run)
        label_layout.addWidget(self.nmap_Scan2)
        self.tab1_container_layout.insertLayout(2, label_layout)
        self.tab1_container_layout.addStretch()
        
        # nmap Scan3
        if hasattr(self, 'nmap_Scan3'):
            self.tab1_container_layout.removeWidget(self.nmap_Scan3)
            self.nmap_Scan3.deleteLater()
        self.nmap_Scan3 = QLabel(f"nmap -p- --script=vuln {rhost}")
        self.nmap_Scan3.setStyleSheet(
            "color: 'white';" +
            "font-size: 20px;" +
            "font-style: 'bold';"
            )

        # nmap copy button
        if hasattr(self, 'nmap_Scan3_Copy'):
            self.tab1_container_layout.removeWidget(self.nmap_Scan3_Copy)
            self.nmap_Scan3_Copy.deleteLater()
        self.nmap_Scan3_Copy = QPushButton()
        self.nmap_Scan3_Copy.setIcon(QIcon.fromTheme("edit-copy"))
        self.nmap_Scan3_Copy.setFixedSize(QSize(20,20))
        self.nmap_Scan3_Copy.clicked.connect(lambda: QApplication.clipboard().setText(self.nmap_Scan3.text()))
        self.nmap_Scan3_Copy.setStyleSheet(
            "*:hover{background: '#20C20e';}"
        )

        # nmap run button
        if hasattr(self, 'nmap_Scan3_Run'):
            self.tab1_container_layout.removeWidget(self.nmap_Scan3_Run)
            self.nmap_Scan3_Run.deleteLater()
        self.nmap_Scan3_Run = QPushButton()
        self.nmap_Scan3_Run.setIcon(QIcon.fromTheme("media-playback-start"))
        self.nmap_Scan3_Run.setFixedSize(QSize(20,20))
        command1 = self.nmap_Scan3.text() + "; bash"
        self.nmap_Scan3_Run.clicked.connect(lambda: subprocess.Popen(["/usr/bin/terminator", "--new-tab", "-e", command1]))
        self.nmap_Scan3_Run.setStyleSheet(
            "*:hover{background: '#20C20e';}"
        )

        # nmap_Scan3 adding widgets
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.nmap_Scan3_Copy)
        label_layout.addWidget(self.nmap_Scan3_Run)
        label_layout.addWidget(self.nmap_Scan3)
        self.tab1_container_layout.insertLayout(3, label_layout)
        self.tab1_container_layout.addStretch()
        
        # nmap divider 1
        if hasattr(self, 'nmap_divider1'):
            self.tab1_container_layout.removeWidget(self.nmap_divider1)
            self.nmap_divider1.deleteLater()
        self.nmap_divider1 = QFrame()
        self.nmap_divider1.setFrameShape(QFrame.HLine)
        self.nmap_divider1.setLineWidth(3)
        self.nmap_divider1.setStyleSheet("color: #20C20E;")
        
        # nmap divider2
        if hasattr(self, 'nmap_divider2'):
            self.tab1_container_layout.removeWidget(self.nmap_divider2)
            self.nmap_divider2.deleteLater()
        self.nmap_divider2 = QFrame()
        self.nmap_divider2.setFrameShape(QFrame.HLine)
        self.nmap_divider2.setLineWidth(3)
        self.nmap_divider2.setStyleSheet("color: #20C20E;")
        
        # nmap spacer1
        if hasattr(self, 'nmap_spacer1'):
            self.tab1_container_layout.removeWidget(self.nmap_spacer1)
            self.nmap_spacer1.deleteLater()
        self.nmap_spacer1 = QLabel()
        self.nmap_spacer1.setFixedWidth(40)
        self.nmap_spacer1.setFixedHeight(40)
        # nmap spacer2
        if hasattr(self, 'nmap_spacer2'):
            self.tab1_container_layout.removeWidget(self.nmap_spacer2)
            self.nmap_spacer2.deleteLater()
        self.nmap_spacer2 = QLabel()
        self.nmap_spacer2.setFixedWidth(40)
        self.nmap_spacer2.setFixedHeight(40)

        # nmap spacer & divider layout
        self.tab1_container_layout.insertWidget(4, self.nmap_spacer1)
        self.tab1_container_layout.insertWidget(5, self.nmap_divider1)
        self.tab1_container_layout.insertWidget(6, self.nmap_divider2)
        self.tab1_container_layout.insertWidget(7, self.nmap_spacer2)

### HTTPHelper
    def httphelper(self):
        rhost = "127.0.0.1"
        if not hasattr(self, 'tab2_container'):
            self.tab2_container = QWidget()
            self.tab2_container_layout = QVBoxLayout(self.tab2_container)
            self.tab2_container.setLayout(self.tab2_container_layout)
            self.scroll = QScrollArea()
            self.scroll.setWidget(self.tab2_container)
            self.scroll.setWidgetResizable(True)
            self.tab2_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.tab2_container_layout.setContentsMargins(0,0,0,0)
            self.tab2_container.adjustSize()
            
            self.tab2.setLayout(QVBoxLayout())
            self.tab2.layout().addWidget(self.scroll)

        # nmap_methods
        if hasattr(self, 'nmap_methods'):
            self.tab2_container_layout.removeWidget(self.nmap_methods)
            self.nmap_methods.deleteLater()
        self.nmap_methods = QLabel("[+ Nmap HTTP Methods]")
        self.nmap_methods.setStyleSheet(
            "color: #20C20E;" +
            "font-size: 20px;" +
            "font-style: 'bold';"
        )
        self.tab2_container_layout.insertWidget(0,self.nmap_methods)
        self.tab2_container_layout.addStretch()
        
        # httphelper_divider 1
        if hasattr(self, 'httphelper_divider1'):
            self.tab2_container_layout.removeWidget(self.httphelper_divider1)
            self.httphelper_divider1.deleteLater()
        self.httphelper_divider1 = QFrame()
        self.httphelper_divider1.setFrameShape(QFrame.HLine)
        self.httphelper_divider1.setLineWidth(3)
        self.httphelper_divider1.setStyleSheet("color: #20C20E;")
        
        # httphelper_divider2
        if hasattr(self, 'httphelper_divider2'):
            self.tab2_container_layout.removeWidget(self.httphelper_divider2)
            self.httphelper_divider2.deleteLater()
        self.httphelper_divider2 = QFrame()
        self.httphelper_divider2.setFrameShape(QFrame.HLine)
        self.httphelper_divider2.setLineWidth(3)
        self.httphelper_divider2.setStyleSheet("color: #20C20E;")
        
        # httphelper_spacer1
        if hasattr(self, 'httphelper_spacer1'):
            self.tab2_container_layout.removeWidget(self.httphelper_spacer1)
            self.httphelper_spacer1.deleteLater()
        self.httphelper_spacer1 = QLabel()
        self.httphelper_spacer1.setFixedWidth(40)
        self.httphelper_spacer1.setFixedHeight(40)
        # httphelper_spacer2
        if hasattr(self, 'httphelper_spacer2'):
            self.tab2_container_layout.removeWidget(self.httphelper_spacer2)
            self.httphelper_spacer2.deleteLater()
        self.httphelper_spacer2 = QLabel()
        self.httphelper_spacer2.setFixedWidth(40)
        self.httphelper_spacer2.setFixedHeight(40)

        # httphelper_spacer & divider layout
        self.tab2_container_layout.insertWidget(2, self.httphelper_spacer1)
        self.tab2_container_layout.insertWidget(3, self.httphelper_divider1)
        self.tab2_container_layout.insertWidget(4, self.httphelper_divider2)
        self.tab2_container_layout.insertWidget(5, self.httphelper_spacer2)
        self.tab2_container_layout.addStretch()
##### LPE
    def lpe(self):
        rhost = "127.0.0.1"
        if not hasattr(self, 'container'):
            self.container = QWidget()
            self.tab3_container_layout = QVBoxLayout(self.container)
            self.container.setLayout(self.tab3_container_layout)
            self.scroll = QScrollArea()
            self.scroll.setWidget(self.container)
            self.scroll.setWidgetResizable(True)
            self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.tab3_container_layout.setContentsMargins(0,0,0,0)
            self.container.adjustSize()
            
            self.tab3.setLayout(QVBoxLayout())
            self.tab3.layout().addWidget(self.scroll)

    def wpe(self):
        rhost = "127.0.0.1"
        if not hasattr(self, 'container'):
            self.container = QWidget()
            self.tab4_container_layout = QVBoxLayout(self.container)
            self.container.setLayout(self.tab4_container_layout)
            self.scroll = QScrollArea()
            self.scroll.setWidget(self.container)
            self.scroll.setWidgetResizable(True)
            self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.tab4_container_layout.setContentsMargins(0,0,0,0)
            self.container.adjustSize()
            
            self.tab4.setLayout(QVBoxLayout())
            self.tab4.layout().addWidget(self.scroll)

    def tty(self):
        rhost = "127.0.0.1"
        if not hasattr(self, 'container'):
            self.container = QWidget()
            self.tab5_container_layout = QVBoxLayout(self.container)
            self.container.setLayout(self.tab5_container_layout)
            self.scroll = QScrollArea()
            self.scroll.setWidget(self.container)
            self.scroll.setWidgetResizable(True)
            self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.tab5_container_layout.setContentsMargins(0,0,0,0)
            self.container.adjustSize()
            
            self.tab5.setLayout(QVBoxLayout())
            self.tab5.layout().addWidget(self.scroll)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

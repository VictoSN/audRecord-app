from PyQt6.QtWidgets import (
    QLabel, QMainWindow, QPushButton,
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit,QSystemTrayIcon, QStyle
)
from recorder import Recorder
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.recordings = []
        self.selected_idx = None
        self.recorder = Recorder()
        
        self.setup_notification()
        self.setup_ui()
        self.setup_connections()
        self.render_recording()
        
    def setup_notification(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        self.tray.show()
        
    def setup_ui(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Audio Recorder")
        
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left & Right column
        self.left_column = QVBoxLayout()
        main_layout.addLayout(self.left_column)
        
        self.right_column = QVBoxLayout()
        main_layout.addLayout(self.right_column)
        
        self.record_button = QPushButton("Record")
        self.right_column.addWidget(self.record_button)
        
    def setup_connections(self):
        self.record_button.clicked.connect(self.toggle_record)
    
    def render_recording(self):
        pass
    
    def load_audio(self):
        pass
    
    def select_audio(self, idx):
        pass
    
    def play_audio(self):
        pass

    def toggle_record(self):
        if self.recorder.is_recording:
            pass
        else:
            
            pass
    
    def stop_record(self):
        pass
    
    def add_audio(self):
        pass
    
    def update_audio(self):
        pass
    
    def delete_audio(self):
        pass
    
    def set_inputs(self, enabled):
        pass
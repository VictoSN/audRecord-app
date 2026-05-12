from PyQt6.QtWidgets import (
    QLabel, QMainWindow, QPushButton,
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit,QSystemTrayIcon, QStyle
)
from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from pathlib import Path
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
        self.setup_timer()
        self.setup_sound_effects()
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
        main_layout = QVBoxLayout(central_widget)
        
        # Left & Right column
        self.top_row = QVBoxLayout()
        main_layout.addLayout(self.top_row)
        
        self.bottom_row = QVBoxLayout()
        main_layout.addLayout(self.bottom_row)
        
        # Timer duration
        self.timer_duration = QLabel()
        self.bottom_row.addWidget(self.timer_duration)
        self.timer_duration.setStyleSheet("""
                                          font-size: 48px;
                                          font-weight: bold;
                                          qproperty-alignment: AlignCenter;
                                          """)
        
        # Record button
        self.record_button = QPushButton("Start Recording")
        self.bottom_row.addWidget(self.record_button)
        
    def setup_connections(self):
        self.record_button.clicked.connect(self.toggle_record)
  
    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_ms = 0
      
    def setup_sound_effects(self):
        # Sound effects
        BASE_DIR = Path(__file__).resolve().parent
        self.start_file = BASE_DIR / "sound_effects/start.wav"
        self.end_file = BASE_DIR / "sound_effects/end.wav"
        
        self.sound = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.sound.setAudioOutput(self.audio_output)
      
    # Load the list of recording in the left column
    def render_recording(self):
        
        pass
    
    # From the list, able to choose the audio
    def select_audio(self, idx):
        
        pass
    
    # From the selected audio, load it from the storage and database
    def load_audio(self):
        
        pass
    
    def play_audio(self):
        
        pass

    def update_timer(self):
        if not self.recorder.is_recording: return
        
        self.elapsed_ms += 1
        total_seconds = self.elapsed_ms // 100
        ms = (self.elapsed_ms % 100) // 10
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        self.timer_duration.setText(f"{minutes:02}:{seconds:02}.{ms:01}")

    def toggle_record(self):
        if self.recorder.is_recording:
            self.hide_top_row(False)
            self.stop_record()
            self.record_button.setText("Start Recording")
        else:
            self.hide_top_row(True)
            self.start_record()
            self.record_button.setText("Stop Recording")
    
    def stop_record(self):
        self.sound.setSource(QUrl.fromLocalFile(str(self.end_file)))
        self.sound.play()
        
        self.recorder.stop()
        self.elapsed_ms = 0
        self.timer_duration.setText("")
        
        name = "Voice " + datetime.now().strftime('%Y%m%d_%H%M%S')
        self.recorder.save("recordings", name)
    
    def start_record(self):
        self.sound.setSource(QUrl.fromLocalFile(str(self.start_file)))
        self.sound.play()
        
        self.timer.start(10)
        self.recorder.start()
        
    def update_audio(self):
        
        pass
    
    def delete_audio(self):
        
        pass
    
    def set_inputs(self, enabled):
        
        pass
    
    def hide_top_row(self, enabled):
        for i in range(self.top_row.count()):
            widget = self.top_row.itemAt(i).widget()
            if enabled:
                widget.hide()
            else:
                widget.show()
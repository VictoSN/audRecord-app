from PyQt6.QtWidgets import (
    QLabel, QMainWindow, QPushButton,
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit,QSystemTrayIcon, QStyle
)
from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from pathlib import Path
from recorder import Recorder
from storage import Storage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.recorder = Recorder()
        self.recorder.player.mediaStatusChanged.connect(self.media_status)
        self.storage = Storage()
        
        self.recordings = []
        self.recordings = self.storage.get_audio()
        self.selected_idx = None
        
        self.setup_notification()
        self.setup_ui()
        self.hide_control(True)
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
        
        # Playback Audio layout
        self.playback_layout = QVBoxLayout()
        main_layout.addLayout(self.playback_layout)
        
        self.audio_name = QLineEdit()
        self.playback_layout.addWidget(self.audio_name)
        
        # Timer duration
        self.timer_duration = QLabel()
        self.playback_layout.addWidget(self.timer_duration)
        self.timer_duration.setStyleSheet("""
                                          font-size: 48px;
                                          font-weight: bold;
                                          qproperty-alignment: AlignCenter;
                                          """)
        
        self.total_duration = QLabel()
        self.playback_layout.addWidget(self.total_duration)
        self.total_duration.setStyleSheet("""
                                          font-size: 24px;
                                          font-weight: bold;
                                          qproperty-alignment: AlignCenter;
                                          """)
        

        self.playback_control_layout = QHBoxLayout()
        self.playback_layout.addLayout(self.playback_control_layout)
        
        self.backward_playback = QPushButton("-5")
        self.playback_control_layout.addWidget(self.backward_playback)

        self.play_playback = QPushButton("Play")
        self.playback_control_layout.addWidget(self.play_playback)
        
        self.forward_playback = QPushButton("+5")
        self.playback_control_layout.addWidget(self.forward_playback)
        
        self.playback_navigation_layout = QHBoxLayout()
        self.playback_layout.addLayout(self.playback_navigation_layout)
        
        self.delete_playback = QPushButton("Delete")
        self.playback_navigation_layout.addWidget(self.delete_playback)
        
        self.back_playback = QPushButton("Back")
        self.playback_navigation_layout.addWidget(self.back_playback)
        
        # Top & Bottom row
        self.top_row = QVBoxLayout()
        main_layout.addLayout(self.top_row)
        
        self.bottom_row = QVBoxLayout()
        main_layout.addLayout(self.bottom_row)
                
        # Record button
        self.record_button = QPushButton("Start Recording")
        self.bottom_row.addWidget(self.record_button)
        
    def setup_connections(self):
        self.record_button.clicked.connect(self.toggle_record)
        self.play_playback.clicked.connect(self.toggle_playback)
        self.delete_playback.clicked.connect(self.delete_audio)
        self.back_playback.clicked.connect(self.back_audio)
  
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
      
    # Audio Playback Logic
    # Load the list of recording in the left column
    def render_recording(self):
        # Clear the layout first
        for i in reversed(range(self.top_row.count())):
            widget = self.top_row.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                        
        # Rebuild the UI
        for i, recording in enumerate(self.recordings):
            btn = QPushButton(recording[1])
            btn.clicked.connect(lambda _, idx =i: self.select_audio(idx))
            self.top_row.addWidget(btn)
            
    # From the list, able to choose the audio
    def select_audio(self, idx):
        self.selected_idx = idx
        recording = self.recordings[idx]
        
        self.hide_control(False)
        self.hide_top_row(True)
        print(recording)
        self.timer_duration.setText("00:00.0")
        self.audio_name.setText(recording[1])
        self.total_duration.setText(recording[2])
        
    def update_audio(self):    
        pass
    
    def toggle_playback(self):
        if self.recorder.is_playing:
            self.play_playback.setText("Play")
            self.repaint()
            self.recorder.pause()
            return

        if self.recorder.is_paused:
            self.play_playback.setText("Pause")
            self.repaint()
            self.recorder.resume()
            return

        self.play_playback.setText("Pause")
        recording = self.recordings[self.selected_idx]
        self.recorder.play(recording[4])
        self.timer.start(10)
        
    def media_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.play_playback.setText("Play")
            self.recorder.is_playing = False
            self.recorder.is_paused = False
            self.timer.stop()
            
    def navigate_playback(self):
        pass
    
    def delete_audio(self):
        recording = self.recordings[self.selected_idx]
        self.storage.delete_audio(recording[0])
        self.back_audio()
    
    def back_audio(self):
        self.timer_duration.setText("")
        self.hide_control(True)
        self.hide_top_row(False)
        self.recordings = self.storage.get_audio()
        self.render_recording()
    
    # Audio Recording Logic
    def update_timer(self):
        if self.recorder.is_recording:
            self.elapsed_ms += 1
            
            total_seconds = self.elapsed_ms // 100
            ms = (self.elapsed_ms % 100) // 10
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            
            self.timer_duration.setText(f"{minutes:02}:{seconds:02}.{ms:01}")
        elif self.recorder.is_playing:
            ms = self.recorder.player.position()
            self.timer_duration.setText(self.recorder.format_time(ms / 1000))
            
    def toggle_record(self):
        if self.recorder.is_recording:
            self.hide_top_row(False)
            self.stop_record()
            self.record_button.setText("Start Recording")
            self.recordings = self.storage.get_audio()
            self.render_recording()
        else:
            self.hide_top_row(True)
            self.start_record()
            self.timer_duration.show()
            self.record_button.setText("Stop Recording")
    
    def stop_record(self):
        self.sound.setSource(QUrl.fromLocalFile(str(self.end_file)))
        self.sound.play()
        
        self.recorder.stop()
        self.recorder.save()
        self.elapsed_ms = 0
        self.timer_duration.setText("")
    
    def start_record(self):
        self.sound.setSource(QUrl.fromLocalFile(str(self.start_file)))
        self.sound.play()
        
        self.timer.start(10)
        self.recorder.start()
    
    # Controls Visibility
    def set_layout_visible(self, layout, visible):
        for i in range(layout.count()):
            item = layout.itemAt(i)

            if item.widget():
                item.widget().setVisible(visible)
            elif item.layout():
                self.set_layout_visible(item.layout(), visible)
    
    def hide_control(self, enabled):
        self.set_layout_visible(self.playback_layout, not enabled)
        
    def hide_top_row(self, enabled):
        self.set_layout_visible(self.top_row, not enabled)
                
    def closeEvent(self, event):
        self.recorder.storage.close()
        event.accept()
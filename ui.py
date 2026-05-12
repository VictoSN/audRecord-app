from PyQt6.QtWidgets import (
    QLabel, QMainWindow, QPushButton, QScrollArea,
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit,QSystemTrayIcon, QStyle,
)
from PyQt6.QtCore import QTimer, QUrl, Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from datetime import datetime
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
        
        self.storage.delete_audio()
                
    def setup_notification(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        self.tray.show()
        
    def setup_ui(self):
        self.setGeometry(100, 100, 330, 330)
        self.setWindowTitle("Audio Recorder")
        
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Playback Audio layout
        self.playback_layout = QVBoxLayout()
        self.playback_layout.setSpacing(0)
        main_layout.addLayout(self.playback_layout)
        
        self.audio_name = QLineEdit()
        self.playback_layout.addWidget(self.audio_name)
        
        # Timer duration
        self.timer_duration = QLabel()
        self.timer_duration.setStyleSheet("""
                                          font-size: 60px;
                                          font-weight: bold;
                                          padding: 0px;
                                          margin: 0px;
                                          qproperty-alignment: AlignCenter;
                                          """)
        self.playback_layout.addWidget(self.timer_duration)
        
        self.total_duration = QLabel()
        self.total_duration.setStyleSheet("""
                                          font-size: 42px;
                                          font-weight: bold;
                                          padding: 0px;
                                          margin: 0px;
                                          qproperty-alignment: AlignCenter;
                                          """)
        self.playback_layout.addWidget(self.total_duration)

        self.playback_button = QVBoxLayout()
        self.playback_button.setSpacing(5)
        self.playback_layout.addLayout(self.playback_button)

        self.playback_control_layout = QHBoxLayout()
        self.playback_control_layout.setSpacing(5)
        self.playback_button.addLayout(self.playback_control_layout)
        
        self.backward_playback = QPushButton("-5")
        self.playback_control_layout.addWidget(self.backward_playback)

        self.play_playback = QPushButton("Play")
        self.playback_control_layout.addWidget(self.play_playback)
        
        self.forward_playback = QPushButton("+5")
        self.playback_control_layout.addWidget(self.forward_playback)
        
        self.playback_navigation_layout = QHBoxLayout()
        self.playback_navigation_layout.setSpacing(5)
        self.playback_button.addLayout(self.playback_navigation_layout)
        
        self.delete_playback = QPushButton("Delete")
        self.playback_navigation_layout.addWidget(self.delete_playback)
        
        self.back_playback = QPushButton("Back")
        self.playback_navigation_layout.addWidget(self.back_playback)
        
        # Top & Bottom row
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.top_container = QWidget()
        self.top_row = QVBoxLayout(self.top_container)

        self.scroll.setWidget(self.top_container)
        main_layout.addWidget(self.scroll)
                
        self.bottom_row = QVBoxLayout()
        main_layout.addLayout(self.bottom_row)
                
        # Record button
        self.record_button = QPushButton("Start Recording")
        self.bottom_row.addWidget(self.record_button)
        
    def setup_connections(self):
        self.record_button.clicked.connect(self.toggle_record)
        self.audio_name.editingFinished.connect(self.update_audio)
        self.play_playback.clicked.connect(self.toggle_playback)
        self.backward_playback.clicked.connect(lambda: self.duration_playback(-5))
        self.forward_playback.clicked.connect(lambda: self.duration_playback(5))
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
    def clear_rendering(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

            elif item.layout():
                self.clear_rendering(item.layout())
                
    # Load the list of recording in the left column
    def render_recording(self):
        self.clear_rendering(self.top_row)

        for i, recording in enumerate(self.recordings):
            recording_layout = QHBoxLayout()

            info_layout = QVBoxLayout()
            info_layout2 = QVBoxLayout()

            recording_layout.addLayout(info_layout)
            recording_layout.addStretch()
            recording_layout.addLayout(info_layout2)

            # Format date
            raw_date = recording[3]
            formatted_date = datetime.strptime(
                raw_date,
                "%Y%m%d_%H%M%S"
            ).strftime("%Y-%m-%d : %H:%M:%S")

            # Widgets
            title = QLabel(recording[1])
            date = QLabel(formatted_date)
            duration = QLabel(recording[2])

            btn = QPushButton("▶")
            btn.setFixedWidth(45)

            btn.clicked.connect(lambda _, idx=i: self.select_audio(idx))

            # Styles
            title.setStyleSheet("font-size: 16px; font-weight: bold;")
            date.setStyleSheet("color: gray; font-size: 12px;")
            duration.setStyleSheet("font-size: 13px; font-weight: bold;")
            btn.setStyleSheet("QPushButton {padding: 6px; font-size: 16px;}")

            # Layouts
            info_layout.addWidget(title)
            info_layout.addWidget(date)

            info_layout2.addWidget(btn)
            info_layout2.addWidget(duration)

            self.top_row.addLayout(recording_layout)
               
    def reset_flags(self):
        self.recorder.is_playing = False
        self.recorder.is_paused = False
        self.recorder.player.stop()
        self.timer.stop()

    # From the list, able to choose the audio
    def select_audio(self, idx):
        self.selected_idx = idx
        recording = self.recordings[idx]
        
        self.hide_control(False)
        self.hide_record_button(True)
        self.hide_top_row(True)
        print(recording)
        self.timer_duration.setText("00:00.0")
        self.audio_name.setText(recording[1])
        self.total_duration.setText(recording[2])
        
    def update_audio(self):
        recording = self.recordings[self.selected_idx]
        new_name = self.audio_name.text()
        self.storage.update_audio_name(recording[0], new_name)
    
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
            self.reset_flags()
                            
    # Forward / Backward playback
    def duration_playback(self, amount):
        if not self.recorder.is_playing and not self.recorder.is_paused:
            self.toggle_playback()
        elif self.recorder.is_paused:
            self.recorder.resume()
        self.recorder.progress(amount)
    
    def delete_audio(self):
        recording = self.recordings[self.selected_idx]
        self.storage.delete_audio(recording[0])
        self.back_audio()
    
    def back_audio(self):
        self.reset_flags()
        self.timer_duration.setText("")
        self.hide_control(True)
        self.hide_record_button(False)
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
        self.timer_duration.hide()
    
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
                if visible:
                    item.widget().show()
                else:
                    item.widget().hide()
                    
            elif item.layout():
                self.set_layout_visible(item.layout(), visible)
    
    def hide_control(self, enabled):
        self.set_layout_visible(self.playback_layout, not enabled)
            
    def hide_top_row(self, enabled):
        self.set_layout_visible(self.top_row, not enabled)
        
        if enabled:
            self.scroll.hide()
        else:
            self.scroll.show()
               
    def hide_record_button(self, enabled):
        if enabled:
            self.record_button.hide()
        else:
            self.record_button.show()
                
    def closeEvent(self, event):
        self.recorder.storage.close()
        event.accept()
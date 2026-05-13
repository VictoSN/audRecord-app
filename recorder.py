from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl

from storage import Storage
from datetime import datetime
from pathlib import Path
import sounddevice as sd
import soundfile as sf
import numpy as np

class Recorder:
    def __init__(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        self.storage = Storage()
        self.is_recording = False
        self.audio_data = None
        self.sample_rate = 44100
        self.recorded = []
        self.record = None
        self.filepath = "recordings"
        self.is_playing = False
        self.is_paused = False
        
    # Recorder Logic
    def callback(self, data, frames, time, status):
        self.recorded.append(data.copy())
        
    def start(self):
        self.is_recording = True
        self.recorded.clear()
        
        self.record = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=self.callback
            )
        self.record.start()
    
    def stop(self):
        if self.record:
            self.is_recording = False
            self.record.stop()
            self.record.close()
            self.audio_data = np.concatenate(self.recorded, axis=0)
    
    def format_time(self, seconds):
        min = int(seconds // 60)
        sec = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 10)
        
        return f"{min:02}:{sec:02}.{ms}"
    
    def save(self):
        Path(self.filepath).mkdir(exist_ok=True)
        name = "Voice " + datetime.now().strftime('%y%m%d_%H%M%S')
        duration = self.format_time(len(self.audio_data) / self.sample_rate)
        date = datetime.now().strftime('%Y%m%d_%H%M%S')
        sf.write(
            f"{self.filepath}/{name}.wav", 
            self.audio_data, 
            self.sample_rate
            )
        self.storage.add_audio(name, duration, date, f"{self.filepath}/{name}.wav")
    
    # Playback Logic
    def play(self, filepath):
        self.is_playing = True;
        try:
            self.player.setSource(QUrl.fromLocalFile(filepath))
            self.player.play()
        except:
            print("Error Loading File")
        
    def pause(self):
        self.is_playing = False;
        self.is_paused = True
        self.player.pause()
    
    def resume(self):
        self.is_playing = True;
        self.is_paused = False;
        self.player.play()
        
    def progress(self, amount):
        current_position = self.player.position()
        new_position = current_position + (amount * 1000) # Convert to ms
        new_position = max(0, min(new_position, self.player.duration()))
        self.player.setPosition(new_position)
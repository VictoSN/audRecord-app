from storage import Storage
from datetime import datetime
from pathlib import Path
import sounddevice as sd
import soundfile as sf
import numpy as np

class Recorder:
    def __init__(self):
        self.storage = Storage()
        self.is_recording = False
        self.audio_data = None
        self.sample_rate = 44100
        self.recorded = []
        
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
    
    def save(self):
        filepath = "recordings"
        Path(filepath).mkdir(exist_ok=True)
        name = "Voice " + datetime.now().strftime('%y%m%d_%H%M%S')
        duration = f"{(len(self.audio_data) / self.sample_rate):.1f}"
        date = datetime.now().strftime('%Y%m%d_%H%M%S')
        sf.write(
            f"{filepath}/{name}.wav", 
            self.audio_data, 
            self.sample_rate
            )
        self.storage.add_audio(name, duration, date, filepath)
    
    def play(self, filepath):
        data, fs = sf.read(f"{filepath}")
        sd.play(data, fs)
        sd.wait()
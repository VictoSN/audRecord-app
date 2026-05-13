# audio-recorder
## A desktop audio recorder built with PyQt6
A Python desktop application for recording, playing back, and managing audio recordings.

## Features
- Record / Delete Recordings
- Named Recordings
- Forward / Backward Playback Controls
- Persistent Storage in SQLite
- Sound effects on record start / stop

## How it works
- Recordings are stored in SQLite and loaded on startup
- sounddevice captures audio via a callback stream
- Recordings are saved as .wav files using soundfile
- Playback is handled by QMediaPlayer with seek support

## Screenshots
### Default Interface
![Default](/images/Default.png)

### Recording
![Recording](/images/Recording.png)

### Single Recording
![Single Recording](/images/Single.png)

### Multiple Recording
![Multiple Recording](/images/Multiple.png)

### Dark Mode
![Dark Mode](/images/Dark.png)

### Replay Recording
![Replay Recording](/images/Replay.png)

## How to run
### 1. Clone the repository
```bash
git clone <your-repo-url>
cd alarm-app
```

---

# Windows (PowerShell)

### 2. Create a virtual environment
```powershell
python -m venv venv
```

### 3. Activate the virtual environment
```powershell
.\venv\Scripts\Activate
```

### 4. Install dependencies
```powershell
pip install PyQt6 sounddevice soundfile numpy
```

### 5. Run the application
```powershell
python main.py
```

---

# Linux / macOS

### 2. Create a virtual environment
```bash
python3 -m venv venv
```

### 3. Activate the virtual environment
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install PyQt6 sounddevice soundfile numpy
```

### 5. Run the application
```bash
python main.py
```

## License
This project is licensed under the [MIT License](LICENSE)
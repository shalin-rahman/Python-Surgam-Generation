import aubio
import numpy as np
import pyaudio

# Define Indian classical music frequencies (Sa Re Ga Ma...)
SARGAM_NOTES = {
    "Sa": 261.63, "Re": 293.66, "Ga": 329.63, "Ma": 349.23,
    "Pa": 392.00, "Dha": 440.00, "Ni": 493.88, "Sa'": 523.25
}

def get_closest_sargam(freq):
    return min(SARGAM_NOTES, key=lambda note: abs(SARGAM_NOTES[note] - freq))

# Set up real-time audio listening
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, frames_per_buffer=1024)
pitch_detector = aubio.pitch("default", 1024, 1024, 44100)
pitch_detector.set_unit("Hz")

print("Listening... Sing a note!")

while True:
    audio_data = np.frombuffer(stream.read(1024), dtype=np.float32)
    pitch = pitch_detector(audio_data)[0]
    if pitch > 0:
        print(f"Detected: {get_closest_sargam(pitch)} ({pitch:.2f} Hz)")

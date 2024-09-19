import os
import wave
import time
import pyaudio
import threading
import tkinter as tk

class VoiceRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Recorder")
        self.root.resizable(False, False)

        self.button = tk.Button(self.root, text="🎤", font=("Arial", 120, "bold"), command=self.click_handler)
        self.button.pack(expand=True)

        self.label = tk.Label(self.root, text="00:00:00")
        self.label.pack(expand=True)

        self.recording = False
        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
        else:
            self.recording = True
            self.button.config(fg="red")
            threading.Thread(target=self.record).start()

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []

        start_time = time.time()

        while self.recording:
            data = stream.read(1024)
            frames.append(data)

            # Update time on the label
            elapsed_time = time.time() - start_time
            secs = int(elapsed_time % 60)
            mins = int((elapsed_time / 60) % 60)
            hours = int(elapsed_time / 3600)
            self.label.config(text=f"{hours:02}:{mins:02}:{secs:02}")
            self.label.update()

        # Stop the stream and close audio input when recording is stopped
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Saving the recorded audio file
        exists = True
        i = 1
        while exists:
            if os.path.exists(f"record{i}.wav"):
                i += 1
            else:
                exists = False

        sound_file = wave.open(f"record{i}.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()

# Instantiate the VoiceRecorder class to run the application
VoiceRecorder()

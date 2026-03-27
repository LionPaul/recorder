import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import os

class AudioRecorder:
    def __init__(self):
        self.fs = 44100  # Taxa de amostragem (Qualidade de CD)
        self.channels = 1
        self.is_recording = False
        self.recording_data = []
        self.thread = None

    def _record_loop(self, filename):
        """Loop de gravação que captura o áudio em blocos."""
        # Criamos uma lista para armazenar os blocos de áudio (numpy arrays)
        self.recording_data = []
        
        # O 'InputStream' do sounddevice é mais eficiente para gravações longas
        with sd.InputStream(samplerate=self.fs, channels=self.channels, callback=self._callback):
            while self.is_recording:
                sd.sleep(100) # Mantém a thread viva enquanto grava
        
        # Ao sair do loop, concatena todos os blocos e salva
        if self.recording_data:
            audio_full = np.concatenate(self.recording_data, axis=0)
            sf.write(filename, audio_full, self.fs)

    def _callback(self, indata, frames, time, status):
        """Esta função é chamada automaticamente pelo hardware a cada novo bloco de áudio."""
        if self.is_recording:
            self.recording_data.append(indata.copy())

    def start_recording(self, filename="gravacao.wav"):
        if not self.is_recording:
            self.is_recording = True
            
            if not os.path.exists("recordings"):
                os.makedirs("recordings")
                
            filepath = os.path.join("recordings", filename)
            self.thread = threading.Thread(target=self._record_loop, args=(filepath,))
            self.thread.start()
            print(f"Gravando em: {filepath}")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.thread.join()
            print("Gravação salva com sucesso.")
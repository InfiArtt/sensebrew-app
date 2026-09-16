import wave
import struct
import math

def generate_beep(filename, freq, duration_ms=100, volume=0.5):
    sample_rate = 44100
    num_samples = int(sample_rate * (duration_ms / 1000.0))
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            # Exponential decay envelope for a "click/tick" sound
            envelope = math.exp(-i / (sample_rate * 0.05))
            value = int(volume * envelope * 32767.0 * math.sin(2.0 * math.pi * freq * i / sample_rate))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)

generate_beep('tick.wav', 1200, 50)
generate_beep('tock.wav', 800, 50)

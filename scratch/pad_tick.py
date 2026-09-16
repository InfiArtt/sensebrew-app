import struct
import os

input_path = 'assets/tick.wav'
output_path = 'assets/tick.wav'
silence_ms = 60

# Read original WAV
with open(input_path, 'rb') as f:
    data = f.read()

# Parse WAV header (standard 44-byte PCM header)
if len(data) < 44:
    print("File too small")
    exit(1)

# Verify RIFF header
riff = data[0:4]
wave = data[8:12]
fmt = data[12:16]
if riff != b'RIFF' or wave != b'WAVE' or fmt != b'fmt ':
    print(f"Not a standard WAV file: {riff} {wave} {fmt}")
    exit(1)

num_channels = struct.unpack_from('<H', data, 22)[0]
sample_rate = struct.unpack_from('<I', data, 24)[0]
bits_per_sample = struct.unpack_from('<H', data, 34)[0]
bytes_per_sample = (bits_per_sample // 8) * num_channels

print(f"Channels: {num_channels}, Sample Rate: {sample_rate}, Bits: {bits_per_sample}")

# Calculate silence padding
silence_samples = int(sample_rate * silence_ms / 1000)
silence_bytes = silence_samples * bytes_per_sample
print(f"Adding {silence_ms}ms = {silence_samples} samples = {silence_bytes} bytes of silence")

# Find the 'data' chunk
# Standard WAV has 'data' at offset 36, but let's search for it
data_offset = data.find(b'data')
if data_offset == -1:
    print("Could not find 'data' chunk")
    exit(1)

orig_data_size = struct.unpack_from('<I', data, data_offset + 4)[0]
audio_start = data_offset + 8
orig_audio = data[audio_start:audio_start + orig_data_size]

print(f"Original data size: {orig_data_size}, audio starts at offset: {audio_start}")

# Build new WAV
new_data_size = silence_bytes + orig_data_size
header = bytearray(data[:audio_start])

# Update RIFF chunk size
new_file_size = audio_start + new_data_size
struct.pack_into('<I', header, 4, new_file_size - 8)

# Update data chunk size
struct.pack_into('<I', header, data_offset + 4, new_data_size)

# Write output
# Backup original first
backup_path = 'assets/tick_original.wav'
if not os.path.exists(backup_path):
    with open(backup_path, 'wb') as f:
        f.write(data)
    print(f"Backed up original to {backup_path}")

with open(output_path, 'wb') as f:
    f.write(bytes(header))
    f.write(b'\x00' * silence_bytes)  # Silence
    f.write(orig_audio)

final_size = os.path.getsize(output_path)
print(f"Done! New file size: {final_size} bytes (was {len(data)})")

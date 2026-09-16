import os

dart_file = "lib/core/timer_state.dart"

with open(dart_file, 'r', encoding='utf-8') as f:
    content = f.read()

old_keep_alive = """  Future<void> _startKeepAlive() async {
    _keepAlivePlayer?.dispose();
    _keepAlivePlayer = AudioPlayer();
    _keepAlivePlayer!.setReleaseMode(ReleaseMode.loop);
    final header = Uint8List.fromList([
      0x52, 0x49, 0x46, 0x46, 0x74, 0x22, 0x00, 0x00,
      0x57, 0x41, 0x56, 0x45, 0x66, 0x6D, 0x74, 0x20,
      0x10, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00,
      0x44, 0xAC, 0x00, 0x00, 0x88, 0x58, 0x01, 0x00,
      0x02, 0x00, 0x10, 0x00, 0x64, 0x61, 0x74, 0x61,
      0x58, 0x22, 0x00, 0x00,
    ]);
    final silenceData = Uint8List(8792);
    final wavBytes = Uint8List(header.length + silenceData.length);
    wavBytes.setRange(0, header.length, header);
    wavBytes.setRange(header.length, wavBytes.length, silenceData);
    
    await _keepAlivePlayer!.setVolume(0.01);
    await _keepAlivePlayer!.setSourceBytes(wavBytes);
    await _keepAlivePlayer!.resume();
  }"""

new_keep_alive = """  Uint8List _createSilenceWav(int seconds) {
    int sampleRate = 44100;
    int channels = 1;
    int byteRate = sampleRate * channels * 2;
    int dataSize = seconds * byteRate;
    int fileSize = 36 + dataSize;

    var header = ByteData(44);
    header.setUint8(0, 0x52); header.setUint8(1, 0x49); header.setUint8(2, 0x46); header.setUint8(3, 0x46); // RIFF
    header.setUint32(4, fileSize, Endian.little);
    header.setUint8(8, 0x57); header.setUint8(9, 0x41); header.setUint8(10, 0x56); header.setUint8(11, 0x45); // WAVE
    header.setUint8(12, 0x66); header.setUint8(13, 0x6D); header.setUint8(14, 0x74); header.setUint8(15, 0x20); // fmt 
    header.setUint32(16, 16, Endian.little);
    header.setUint16(20, 1, Endian.little);
    header.setUint16(22, channels, Endian.little);
    header.setUint32(24, sampleRate, Endian.little);
    header.setUint32(28, byteRate, Endian.little);
    header.setUint16(32, channels * 2, Endian.little);
    header.setUint16(34, 16, Endian.little);
    header.setUint8(36, 0x64); header.setUint8(37, 0x61); header.setUint8(38, 0x74); header.setUint8(39, 0x61); // data
    header.setUint32(40, dataSize, Endian.little);

    final wavBytes = Uint8List(44 + dataSize);
    wavBytes.setRange(0, 44, header.buffer.asUint8List());
    return wavBytes;
  }

  Future<void> _startKeepAlive() async {
    _keepAlivePlayer?.dispose();
    _keepAlivePlayer = AudioPlayer();
    _keepAlivePlayer!.setReleaseMode(ReleaseMode.loop);
    
    // Create 10 seconds of silence to prevent platform channel event flooding
    final wavBytes = _createSilenceWav(10);
    
    await _keepAlivePlayer!.setVolume(0.01);
    await _keepAlivePlayer!.setSourceBytes(wavBytes);
    await _keepAlivePlayer!.resume();
  }"""

content = content.replace(old_keep_alive, new_keep_alive)

with open(dart_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated keep alive logic!")

# SenseBrew (V60 Blind Guide) - Flutter Version

SenseBrew adalah aplikasi asisten pembuat kopi pintar (V60 & Aeropress) yang dirancang khusus dari nol dengan mengutamakan **Aksesibilitas (Accessibility)** untuk penyandang tunanetra (Tunanetra Netra / *Visually Impaired*). 

Aplikasi ini membimbing pengguna di setiap tahap penyeduhan kopi menggunakan panduan suara (*Voice Over* / *TalkBack*), metronom tuangan, dan kecerdasan buatan (AI) untuk meracik resep yang dapat disesuaikan dengan kebutuhan.

## 🚀 Fitur Utama yang Telah Dikerjakan

### 1. Aksesibilitas Total (TalkBack Optimized)
* Seluruh elemen UI (tombol, teks, daftar resep) telah dikonfigurasi dengan `Semantics` khusus agar terbaca dengan jelas, deskriptif, dan masuk akal oleh pembaca layar Android (TalkBack).
* Mengatasi masalah *focus traversal* agar pengguna tidak terjebak saat mengusap layar (termasuk eksperimen integrasi *PlatformView* untuk navigasi kursor teks tingkat lanjut).
* Dukungan *High Contrast* dan pembacaan nilai numerik secara eksplisit.

### 2. Metronom & Panduan Seduh Real-time
* **Metronome Bridge:** Fitur panduan kecepatan tuangan air yang tersinkronisasi.
* **Audio Cues:** Panduan suara (*Text-to-Speech*) dan bunyi bip pada setiap fase penyeduhan (Blooming, Pour 1, Pour 2, dst) untuk memberitahu kapan harus menuang dan kapan harus berhenti, tanpa perlu melihat layar.

### 3. SenseBrew AI (Rancang Bersama AI)
* Asisten AI pintar yang bisa ditanya, "Buatkan saya resep V60 15 gram yang manis," dan ia akan langsung membuatkan parameter seduhnya.
* **Mendukung Pesan Suara:** Pengguna tunanetra dapat berbicara langsung ke aplikasi, dan AI akan merespons (menggunakan *Groq Whisper API*).
* **Multi-Model Support:** Mendukung Google Gemini dan Groq (Llama / GPT-OSS 120B) untuk pemrosesan super cepat.

### 4. Arsitektur Keamanan (Cloudflare Proxy)
* **Zero Hardcoded API Keys:** Kunci API Groq dan Gemini **tidak** disimpan di dalam aplikasi maupun di HP pengguna. 
* Semua permintaan AI dialihkan melalui **Cloudflare Worker Proxy** rahasia yang menangani injeksi kunci rahasia secara aman di awan (*cloud*). Ini mencegah pencurian API Key saat aplikasi di-*compile* menjadi APK.
* Aplikasi dapat mengganti *provider* (Groq/Gemini) dengan sangat mudah melalui menu Pengaturan.

## 🛠️ Cara Menjalankan Aplikasi (Development)

1. Pastikan Anda telah menginstal **Flutter SDK** (versi 3.22+ direkomendasikan).
2. Kloning *repository* ini.
3. Jalankan `flutter pub get` untuk mengunduh semua *library*.
4. **PENTING (Konfigurasi AI):** 
   Aplikasi ini menunjuk ke Cloudflare Worker lokal milik *developer* (`https://divine-art-85f1.aswar-drummer.workers.dev/`). Jika Anda ingin membuat versi Anda sendiri:
   * Buat Cloudflare Worker baru.
   * Masukkan kodingan *proxy* JavaScript.
   * Masukkan rahasia `GROQ_API_KEY` dan `GEMINI_API_KEY` di menu *Variables* Cloudflare.
   * Ubah URL proksi di file `lib/core/ai_service.dart` ke URL Cloudflare milik Anda.
5. Jalankan aplikasi ke HP fisik menggunakan perintah: `flutter run`

## 📝 Catatan Tambahan (Roadmap)
Versi Flutter ini merupakan **pondasi utama** dan *Proof of Concept* (PoC) dari keseluruhan logika SenseBrew. Saat ini, pengembangan sedang dalam proses migrasi menuju **React Native (Expo)** untuk mempermudah pemeliharaan lintas platform (iOS & Android) dan memperluas ekosistem *library* aksesibilitas pihak ketiga.

---
*Dibangun dengan dedikasi untuk inklusivitas penikmat kopi di seluruh dunia.* ☕

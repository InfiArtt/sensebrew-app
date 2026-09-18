# ☕ SenseBrew - Handover Document (Flutter to Expo Migration)

## 🎯 Tentang Aplikasi & Tujuan Utama
**SenseBrew** (sebelumnya V60 Blind Guide) adalah asisten penyeduh kopi interaktif yang **didesain khusus dengan mengutamakan aksesibilitas (Tunanetra & _Visually Impaired_)**. 

Aplikasi ini tidak sekadar menampilkan timer, melainkan memandu pengguna menyeduh kopi langkah demi langkah menggunakan suara (TTS) dan detak metronom untuk menjaga ritme tuangan air. Selain itu, aplikasi ini dilengkapi dengan **Asisten AI** (menggunakan Groq/Gemini) yang memungkinkan pengguna meracik atau memodifikasi resep kopi hanya lewat obrolan (suara/teks).

**Alasan Migrasi ke Expo (React Native):**
Alasan utama kita meninggalkan Flutter adalah **keterbatasan mesin Aksesibilitas Flutter (Semantics)** saat berhadapan dengan komponen _native_. Di Flutter, _TalkBack_ (Android) sering "tersangkut" atau membaca elemen secara ganda saat kita mencoba menggunakan kolom teks asli (_NativeTextField_). Karena React Native menerjemahkan UI langsung ke komponen _native_ (asli), Expo dipastikan akan jauh lebih ramah dan stabil untuk pembaca layar (TalkBack / VoiceOver).

---

## ✅ Status Pengerjaan Saat Ini (Selesai di Flutter)
Berikut adalah fitur-fitur yang sudah berfungsi penuh di versi Flutter dan perlu di-replika di Expo:

1. **Manajemen Resep (_Recipe Management_)**
   - Mendukung berbagai metode (V60, French Press, Aeropress, Cupping, dll).
   - Struktur data resep sangat detail: Gramasi kopi, total air, suhu, ukuran gilingan, dan daftar **Fase Tuangan** (contoh: Detik ke-0 tuang 50ml, detik ke-45 tuang 100ml).
2. **Layar Seduh (_Brewing Screen_)**
   - Menjalankan timer yang tersinkronisasi dengan fase resep.
   - **Text-to-Speech (TTS):** Mengucapkan instruksi secara otomatis saat fase baru dimulai (misal: "Mulai tuangkan 50 mili air").
   - **Metronom:** Suara detak (_tick_) setiap detik untuk memandu kecepatan tuangan pengguna.
3. **AI Barista Assistant**
   - Obrolan (teks dan _speech-to-text_ / _Whisper API_) untuk meminta AI membuatkan resep baru atau memodifikasi resep yang sedang diedit (misal: "Bikin resep ini jadi lebih manis").
   - AI mengembalikan data dalam format JSON terstruktur yang langsung merender UI resep.
   - Mendukung bahasa Indonesia dan Inggris secara otomatis.
4. **Penyimpanan Lokal**
   - API Key, pengaturan aplikasi, dan draf resep disimpan menggunakan `SharedPreferences` (bisa diganti dengan `AsyncStorage` di Expo).

---

## 🐛 Daftar Bug & Isu dari Versi Flutter (Perhatian untuk Versi Expo)
Berikut adalah daftar keluhan dan bug aktual yang dialami di versi Flutter. Mohon pastikan isu-isu ini **tidak direplikasi** di versi Expo:

1. **Navigasi Usap (Swipe) TalkBack Tersangkut & Melompat (Form Input):**
   Di halaman pembuatan resep custom, navigasi usap (swipe) tersangkut di judul halaman ("Buat resep seduh custom"). Pengguna terpaksa harus menyentuh manual area lain agar bisa lanjut. Saat di-swipe lagi, pembaca layar malah melompati kolom input teks (Nama & Catatan) dan langsung melompat jauh ke pengaturan "Jenis Biji Kopi".
2. **Audio Guide Pembaca Layar (TalkBack) Mendahului Metronom:**
   Aplikasi memiliki dua metode keluaran panduan suara: TTS internal dan Pembaca Layar (via Semantics). Ketukan metronom selalu akurat (_on tempo_). Namun, **suara dari Pembaca Layar (TalkBack) cenderung mendahului metronom sekitar 5-10ms**, sehingga terdengar tidak ritmis/balapan. Berbeda halnya dengan TTS internal aplikasi yang timing-nya lebih pas.
   *(Solusi Expo: Perlu mekanisme penyesuaian delay/offset khusus antara pemanggilan audio dan pemanggilan accessibility announcement).*
3. **Kategori Resep "Nyangkut" saat Buat Resep Baru:**
   Sempat terjadi cacat logika (_logical flaw_) di mana ketika pengguna menekan tombol "Buat Resep Baru" dari dalam menu kategori Cupping, aplikasi malah menganggap pengguna sedang membuat resep V60. 
   *(Solusi Expo: Pastikan parameter kategori (target method) dikirim dengan benar saat memanggil form kosong).*
4. **Tombol Tanpa Label di AI Chat:**
   Sempat terjadi tombol _Send_ dan _Microphone_ di layar obrolan AI tidak memiliki label aksesibilitas sehingga tidak dibaca oleh TalkBack.
   *(Solusi Expo: Pastikan setiap `TouchableOpacity` atau `Pressable` yang hanya berisi ikon selalu diberi `accessibilityLabel`).*

---

## 🚧 Catatan Khusus untuk Developer Expo (Temanmu)
Hal-hal penting yang harus diperhatikan saat membangun ulang di Expo:

*   **Aksesibilitas (Prioritas Utama):** Gunakan _props_ aksesibilitas bawaan React Native secara maksimal (`accessible={true}`, `accessibilityLabel`, `accessibilityRole`). Pastikan alur usap kanan/kiri TalkBack mengalir logis dari atas ke bawah.
*   **Sinkronisasi Metronom & TTS:** Di Flutter, kita sempat kesulitan menyamakan ketukan metronom dengan suara TTS (ada _delay_ terutama di speaker Bluetooth). Di Expo, pertimbangkan menggunakan `expo-av` yang dioptimalkan, atau gunakan trik menghentikan metronom sejenak saat TTS sedang berbicara.
*   **Input Teks:** Semua Form/Input teks silakan gunakan `<TextInput>` standar React Native. Ini akan otomatis membereskan bug kursor TalkBack yang membuat kita frustrasi di Flutter.
*   **State Management:** Di Flutter kita menggunakan `Provider`. Untuk Expo, sangat disarankan menggunakan `Zustand` atau `React Context` untuk menyimpan status timer dan resep.

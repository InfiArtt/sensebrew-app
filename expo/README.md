# SenseBrew — versi Expo

Port dari aplikasi Flutter di `../lib`. Alasan migrasinya ada di
[../MIGRATION_HANDOVER.md](../MIGRATION_HANDOVER.md): mesin aksesibilitas Flutter
bermasalah dengan komponen native, dan React Native merender langsung ke
komponen native sehingga TalkBack jauh lebih stabil.

Aplikasi Flutter **tidak dihapus**. Dua versi ini bisa dipasang berdampingan di
satu HP untuk dibandingkan, karena package id-nya berbeda:

| | package id |
|---|---|
| Flutter | `com.example.v60_blind_guide` |
| Expo | `com.sensebrew.expo` |

## Menjalankan saat ngoding (Expo Go)

```bash
npm install
npm start
```

Buka Expo Go di HP (satu jaringan Wi-Fi dengan laptop), lalu scan QR atau
masukkan URL `exp://<ip-laptop>:8081`. Perubahan kode langsung muncul tanpa
rebuild.

## Membuat APK untuk tester

APK berdiri sendiri — tester tinggal install, tidak perlu Expo Go dan tidak perlu
dev server:

```bash
npx expo prebuild --platform android && cd android && ./gradlew assembleRelease
```

Hasilnya di `android/app/build/outputs/apk/release/app-release.apk`.

APK ini ditandatangani dengan debug keystore bawaan template React Native, jadi
bisa di-sideload tapi **tidak** untuk Play Store. Untuk rilis sungguhan pakai
keystore sendiri, atau build di cloud:

```bash
npx eas-cli build --platform android --profile qa
```

Profil `qa`, `development`, dan `production` ada di [eas.json](eas.json).
Perintah ini butuh login akun Expo.

## Perintah lain

| Perintah | Kegunaan |
|---|---|
| `npm run check` | Bandingkan aritmetika seduh, tabel data, dan click track dengan nilai dari versi Flutter, dan pastikan tidak ada kontrol yang dibaca dua kali oleh pembaca layar |

Aturan untuk pembaca layar yang dijaga `check`: kontrol yang punya
`accessibilityLabel` tidak boleh berisi `<Text>` biasa — pakai
`components/VisualText` untuk teks yang terlihat. TalkBack membaca labelnya
saja, tapi Jieshuo membaca label **lalu** teks di dalamnya, jadi tanpa aturan ini
setiap tombol terdengar dua kali di Jieshuo.
| `npm run typecheck` | TypeScript |

Catatan build: kalau habis mengubah aset atau import ikon, jalankan
`./gradlew clean assembleRelease`. Task `createBundleReleaseJsAndAssets` tidak
membersihkan `android/app/build/generated/res/react/` lebih dulu, jadi aset lama
ikut terkemas dan ukuran APK tidak turun seperti seharusnya.

## Struktur

```
src/core/            model, i18n, aritmetika seduh, AI service, stores (Zustand)
src/core/audio/      metronom, TTS, perekam pesan suara
src/screens/         delapan layar, satu berbanding satu dengan lib/screens/
src/components/      field teks berlabel & bottom-sheet picker
scripts/             konverter data Dart→TS, checker
```

Tiga file di `src/core/` **auto-generated** dari sumber Dart dan akan tertimpa:
`recipeDatabase.ts`, `generatedStrings.ts`, `grinderDatabase.ts`. Regenerate
dengan `python scripts/convert_recipes.py` dan `python scripts/convert_strings.py`.
Tambahan string tulis tangan masuk ke `appStrings.ts`, yang menimpa tabel
generated.

## Cara metronomnya bekerja

Versi Flutter memakai engine Kotlin (`AudioTrack` + `AudioTimestamp`) yang
menulis PCM manual supaya ketukan jatuh di batas frame yang tepat. Expo Go tidak
bisa memuat native module custom, jadi jaminan itu dipindah ke dalam file audio:
click track berisi 60 klik yang attack-nya persis di offset satu detik, didahului
satu detik silence supaya beat 1 jatuh di t=1,000s (sama seperti `Timer.periodic`
Dart yang nyala setelah interval pertama).

JavaScript tidak pernah menentukan kapan klik berbunyi — player native yang
melakukannya, dari file. JS hanya membaca `player.currentTime` untuk tahu beat ke
berapa, dan tiap beat dijadwalkan ulang terhadap jam audio itu, jadi timer yang
telat tidak menggeser beat-beat sesudahnya.

**Click track-nya tidak dibundel.** File 61 detik itu 5,1 MB PCM dan 95% isinya
silence, tapi aapt2 punya daftar ekstensi hardcoded yang tidak pernah dikompresi
dan `.wav` ada di dalamnya — jadi 5,1 MB itu masuk APK apa adanya. Sebagai
gantinya yang dibundel hanya `assets/audio/tick.wav` (15 KB), dan click track-nya
dirender di perangkat saat pertama aplikasi dibuka lalu disimpan di cache
(`src/core/audio/clickTrack.ts`). Byte-nya identik: `npm run check` membandingkan
hasil generator dengan SHA-256 file 5,1 MB yang sudah diverifikasi, dan memastikan
ke-60 klik tetap attack di detik bulat.

**Batas yang masih ada:** track-nya 60 ketukan. Kalau satu fase tuangan lebih
panjang dari 60 detik — bisa terjadi kalau `mlPerSecond` hasil kalibrasi sangat
kecil — metronomnya berhenti di ketukan ke-60 sementara fasenya masih jalan.

Selama menyeduh ada dua jam yang jalan dan keduanya sengaja terpisah: jam seduh
(interval 50 ms, mengukur waktu berlalu) menentukan kapan fase mulai dan kapan
tiap panduan suara keluar; metronom jalan dari jam audionya sendiri. Jam seduh
boleh melenceng beberapa milidetik tanpa mengganggu ketukan yang dipakai
pengguna untuk menuang.

## Perbedaan yang diambil sengaja dari versi Flutter

Semuanya memperbaiki bug, bukan mengubah fitur:

1. **Lead-in `tick.wav` dipotong.** `assets/tick.wav` punya 60,3 ms digital
   silence sebelum kliknya, sedangkan `tick_original.wav` dan `tock.wav` cuma
   0,3 ms. Karena engine Kotlin menulis PCM tick tepat di batas periode *dan*
   menembakkan event aksesibilitasnya di batas yang sama, padding itu membuat
   tiap klik terdengar ~60 ms setelah pengumuman yang menyertainya — inilah
   kemungkinan penyebab keluhan "pembaca layar mendahului metronom". Generator
   click track memotongnya. Kalau masih perlu digeser, ada
   `announcementOffsetMs` yang tersimpan di settings.

   Perlu dicatat: ini **mengubah** suara dibanding versi Flutter, dan belum
   diuji dengan telinga. Kalau ternyata terasa lebih buruk, hilangkan
   pemotongannya di `buildClickTrack` (`src/core/audio/clickTrack.ts`) — hash
   patokan di `npm run check` juga perlu diperbarui kalau begitu.
2. **Volume TTS.** Dart menyimpannya di kunci `ttsVolume` tapi membacanya dari
   `tts_volume`, jadi slider-nya reset tiap buka app. Sekarang satu kunci.
   Catatan: `expo-speech` tidak punya opsi volume, jadi slidernya dihapus dari
   Settings — kalau volume suara perlu diatur, itu butuh pendekatan lain.
3. **Slider TTS jadi tombol +/−.** Slider sulit dipakai dengan pembaca layar
   (nilainya berubah lewat gestur dan gampang kelewat). Speed dan pitch sekarang
   pakai dua tombol, dan nilainya ikut diucapkan di nama tiap tombol.
4. **API key per provider.** Versi Flutter selalu mengirim `geminiApiKey`,
   termasuk ketika provider-nya Groq — jadi Groq dijamin gagal (401, atau error
   "API Key kosong"). Sekarang tiap provider pakai kuncinya sendiri, dan field
   Groq API Key muncul di Settings.
5. **Metode seduh jadi parameter wajib.** Di layar resep custom, metode datang
   sebagai route param yang wajib, bukan argumen konstruktor opsional. Resep yang
   dibuat dari daftar Cupping tidak bisa lagi tersimpan sebagai V60 (isu 3 di
   handover) — melupakannya sekarang jadi type error.
6. **ID resep.** Dulu dari `microsecondsSinceEpoch` dan sering tabrakan (itu
   sebabnya `RecipeRepository` punya pass perbaikan). Sekarang pakai counter.
   Pass perbaikannya tetap ada, karena HP yang upgrade dari versi Flutter masih
   menyimpan data lama.

## Ukuran APK

Sebagian besar isi APK adalah lantai dasar React Native dan tidak bisa dikurangi:

| Bagian | Ukuran |
|---|---|
| `lib/arm64-v8a/` (libreactnative 6,7 MB, hermes 2,4 MB, expo-modules-core 1,4 MB, …) | ~16,5 MB |
| `classes.dex` ×3 | ~9,9 MB |
| `assets/index.android.bundle` | ~2,1 MB |
| `resources.arsc` + sisa resource | ~3,4 MB |

Flutter meng-AOT Dart jadi satu `libapp.so` dengan engine ~7 MB, sedangkan RN
membawa Hermes plus libreactnative plus JSI/Fabric. Selisih itu harga
arsitektur, bukan hasil porting yang buruk.

Yang belum dipakai: R8/minify (`android.enableMinifyInReleaseBuilds=true`) bisa
memotong beberapa MB dari 9,9 MB dex, tapi R8 bisa merusak kode RN yang memakai
refleksi, jadi jangan dikirim ke tester sebelum di-smoke-test di HP sendiri.

## Yang perlu dites

Prioritaskan yang tidak tertangkap `npm run check` — semua yang bunyi, bergetar,
atau dibaca TalkBack.

**Metronom & panduan suara** (paling penting)
- Klik terasa on-tempo sepanjang satu fase tuangan, tanpa ketukan yang meleset.
- Suara panduan dan ketukan terdengar sejajar, tidak balapan.
- Cek juga dengan speaker Bluetooth — di versi Flutter ini titik tersulitnya.
- Ganti mode keluaran suara (TTS aplikasi vs Pembaca Layar) di Settings dan
  bandingkan keduanya.

**TalkBack**
- Navigasi usap di layar Kalibrasi mengalir: tombol minus → kolom angka →
  tombol plus, tanpa nyangkut dan tanpa melewati kolomnya.
- Usap di form Resep Custom tidak melompati kolom Nama dan Catatan.
- Tombol Kirim dan Mikrofon di AI Chat terbaca namanya.
- Hitungan detik saat menyeduh terbaca tanpa membanjiri.

**Alur biasa**
- Kalibrasi dulu, lalu seduh — tanpa kalibrasi, tombol Seduh memang menolak.
- Buat resep baru dari daftar Cupping, simpan, pastikan muncul di daftar Cupping.
- Edit resep bawaan lalu "Simpan sebagai baru": yang asli harus tetap utuh.
- AI Chat butuh API key di Settings. Coba teks dan pesan suara.
- Tandai favorit, tutup aplikasi, buka lagi — favoritnya harus bertahan.

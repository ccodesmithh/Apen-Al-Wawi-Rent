# Apen Al-wawi

# UNDER MAINTENACE

<!-- Ringkasan
- Program CLI sederhana untuk menyewa kendaraan (mobil, motor, sepeda) dengan fitur perhitungan harga, pajak, diskon, voucher, dan pencetakan struk.
- Menyediakan interaksi singkat dengan AI customer service (masyud) berdasarkan isi `context.txt`.

Persyaratan
- Python 3.8+
- Paket:
  - python-dotenv
  - google-generativeai (atau SDK yang sesuai)

Instalasi
1. Pasang dependensi:
   ```
   pip install python-dotenv google-generativeai
   ```
2. Pastikan file `rent.py` dan `context.txt` berada di direktori yang sama.

Konfigurasi
- Buat file `.env` di direktori proyek:
  ```
  MASYUD_API_KEY=your_api_key_here
  ```
- `context.txt` harus berisi konteks layanan (mis. deskripsi layanan, kebijakan, jam operasional) yang digunakan untuk menjawab pertanyaan AI.

Struktur data singkat
- `pilihan` (dict): mapping kode -> (nama_kendaraan, harga_per_hari, list_warna)
  - Contoh: `"mb1": ("G-Class", 5000000, ["Hitam","Putih","Silver"])`

Fitur utama
- Menampilkan tabel kendaraan dan harga.
- Memilih kendaraan berdasarkan kode (mis. `mb1`, `mk2`, `s1`).
- Memilih warna yang tersedia.
- Menghitung:
  - Subtotal = harga_per_hari * jumlah_hari
  - Pajak = 10% dari subtotal
  - Diskon durasi: >=14 hari -> 10%, >=7 hari -> 5%
  - Voucher: 
    - `MERDEKA17` -> 17% dari total setelah diskon durasi
    - `HEMAT5` -> 5% dari total setelah diskon durasi
- Pembayaran: tunai (cek jumlah hingga cukup) atau transfer.
- Mencetak struk ke layar dan menyimpan ke `struk_penyewaan.txt`.

Cara menjalankan
1. Pastikan `.env` dan `context.txt` benar.
2. Jalankan:
   ```
   python rent.py
   ```
3. Ikuti prompt untuk memilih kendaraan, durasi, mengisi data penyewa, dan memilih metode pembayaran.
4. Untuk bertanya ke AI saat input, ketik `halo mas` (alias `halomas` tanpa spasi) saat diminta input.

Contoh alur singkat
- Pilih: `mb1` -> pilih warna -> konfirmasi Y -> jumlah hari 10 -> isi data -> voucher `HEMAT5` -> pembayaran tunai.

Keluaran
- File struk: `struk_penyewaan.txt` disimpan di direktori kerja.
- Data yang disimpan: nama, alamat, jenis kelamin, telepon, detail pesanan, jumlah & total pembayaran.

Keamanan & privasi
- README tidak menyertakan API key. Simpan `MASYUD_API_KEY` di `.env` dan jangan commit ke VCS.
- Program menyimpan data dasar penyewa dalam struk teks; hindari menyimpan data sensitif tanpa persetujuan.

Troubleshooting
- Error akses AI: periksa `MASYUD_API_KEY` dan koneksi internet.
- Error file: pastikan `context.txt` ada dan dapat dibaca (UTF-8).
- Jika dependency SDK berubah, sesuaikan import `google.generativeai` dengan SDK yang benar.

Lisensi & Catatan
- MIT:
  Copyright (c) 2025 Rayud

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE. -->

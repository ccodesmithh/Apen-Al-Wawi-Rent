"""
Apen Al-wawi Rent - Rental kendaraan dengan AI customer service.

Overview:
    Program baris perintah untuk menyewa kendaraan (mobil, motor, sepeda).
    Fitur:
      - Menampilkan daftar kendaraan dan harga.
      - Memilih kendaraan, warna, lama sewa.
      - Menghitung subtotal, pajak (10%), diskon durasi, voucher.
      - Metode pembayaran tunai atau transfer.
      - Mencetak dan menyimpan struk ke 'struk_penyewaan.txt'.
      - Interaksi dengan AI customer service (masyud) menggunakan model generative.

Requirements:
    - Python 3.8+
    - package: python-dotenv
    - package: google-generativeai (atau SDK yang sesuai dengan variable masyud)
    - File 'context.txt' harus ada di direktori yang sama (berisi konteks layanan rental)

Environment / Setup:
    1. Buat file .env di folder proyek:
        MASYUD_API_KEY=your_api_key_here
    2. Install dependencies:
        pip install python-dotenv google-generativeai
    3. Pastikan 'context.txt' berisi informasi layanan (nama usaha, daftar kendaraan, kebijakan, jam operasional, dsb.)
       - Context digunakan sebagai konteks untuk jawaban AI. Contoh singkat di context.txt:
         "Apen Al-wawi Rent adalah layanan rental kendaraan. Kami menyewakan mobil, motor, dan sepeda. Pajak 10%..."
    4. Jalankan program:
        python rent.py

File dan struktur data:
    - pilihan (dict): mapping kode -> (nama_kendaraan, harga_per_hari, list_warna)
      Contoh: "mb1": ("G-Class", 5000000, ["Hitam","Putih","Silver"])

Fungsi penting:
    - format_rupiah(angka): format int ke string rupiah menggunakan titik sebagai pemisah ribuan.
    - tabelAwal(): menampilkan tabel ringkasan kendaraan dan harga.
    - input_user(prompt_text, choices=None, capitalize=False):
        Membaca input user, mendukung validasi pilihan dan trigger AI lewat input 'halomas' (tanpa spasi).
    - pilih_warna(warnaTersedia): menampilkan warna dan meminta input valid.
    - tanya_masyud(): loop interaktif untuk bertanya ke AI menggunakan model yang dikonfigurasi.
      - Model dikonfigurasi dengan MASYUD_API_KEY dari .env; jawaban AI diharapkan berbasis context.txt.
    - Alur utama:
        1. Tampilkan tabelAwal
        2. Minta kode kendaraan
        3. Konfirmasi, jumlah hari, hitung subtotal + pajak
        4. Formulir penyewa (nama, alamat, telepon, jenis kelamin)
        5. Jenis jaminan (KTP/Pasport/SIM)
        6. Hitung diskon durasi otomatis: >=14 hari -> 10%, >=7 hari -> 5%
        7. Voucher: MERDEKA17 -> 17% tambahan, HEMAT5 -> 5% tambahan
        8. Metode pembayaran: tunai (menerima input sampai cukup), transfer (tampilkan instruksi)
        9. Cetak struk ke layar dan simpan ke file struk_penyewaan.txt (encoding utf-8)

Voucher & Diskon:
    - Diskon durasi dihitung dari total sebelum diskon (subtotal + pajak).
    - Voucher diterapkan setelah diskon durasi.
    - Voucher yang valid saat ini:
        - MERDEKA17  -> 17% dari total setelah diskon durasi
        - HEMAT5     -> 5% dari total setelah diskon durasi

File keluaran:
    - struk_penyewaan.txt (tersimpan di direktori kerja saat ini)
    - context.txt harus berada di lokasi yang sama agar AI mendapat konteks.

Catatan keamanan & privasi:
    - Program menyimpan data dasar penyewa (nama, alamat, telepon) ke file struk_penyewaan.txt.
      Jangan simpan informasi sensitif kecuali Anda paham konsekuensinya.
    - Pastikan MASYUD_API_KEY tidak dibagikan; simpan di .env dan jangan commit ke kontrol versi.

Troubleshooting:
    - Jika program gagal mengakses API AI, periksa MASYUD_API_KEY di .env dan koneksi internet.
    - Jika context.txt tidak ditemukan, program akan error saat membuka file; pastikan file ada.

Contoh penggunaan singkat:
    1. jalankan: python rent.py
    2. Pilih kode kendaraan: mb1
    3. Pilih warna dari daftar
    4. Konfirmasi Y
    5. Masukan jumlah hari (mis. 10)
    6. Isi data penyewa, pilih jaminan, masukan voucher bila ada
    7. Pilih pembayaran, jika tunai masukan jumlah uang hingga cukup
    8. Cek struk di layar dan file 'struk_penyewaan.txt'

License:
    - MIT
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
    SOFTWARE.


"""

from dotenv import load_dotenv
import os
import google.generativeai as masyud

# Load .env
load_dotenv()

# Ambil API key dari environment
api_key = os.getenv("MASYUD_API_KEY")

masyud.configure(api_key=api_key)
model = masyud.GenerativeModel(
    "gemini-1.5-flash", 
    system_instruction="Kamu adalah customer service untuk Apen Al-wawi Rent. Jawablah hanya seputar layanan rental kendaraan ini."
)

def format_rupiah(angka):
    """
    Mengubah angka menjadi format rupiah dengan titik sebagai pemisah ribuan.

    Args:
        angka (int): Nilai yang akan diformat.

    Returns:
        str: String angka dalam format rupiah.
    """
    return "{:,}".format(angka).replace(",", ".")

# =================== DATA KENDARAAN ===================
pilihan = {
    "mb1": ("G-Class", 5000000, ["Hitam", "Putih", "Silver"]),
    "mb2": ("BMW M4", 3450000, ["Biru", "Merah", "Hitam"]),
    "mb3": ("Porsche 911", 2800000, ["Kuning", "Putih"]),
    "mb4": ("McLaren Senna", 4250000, ["Oranye", "Abu-abu"]),
    "mb5": ("Toyota GR Supra", 3000000, ["Merah", "Putih", "Hijau"]),
    "mb6": ("Toyota Alphard Hybrid", 5000000, ["Hitam", "Putih"]),
    "mk1": ("Harley Davidson RG", 2500000, ["Hitam", "Coklat"]),
    "mk2": ("Yamaha R6", 700000, ["Biru", "Hitam"]),
    "mk3": ("Honda CBR 1000 RR", 1500000, ["Merah", "Putih"]),
    "mk4": ("Yamaha XSR 155", 550000, ["Hitam", "Hijau"]),
    "mk5": ("Sportster 48", 1500000, ["Hitam", "Silver"]),
    "s1": ("Sepeda Listrik", 20000, ["Hitam", "Putih"]),
    "s2": ("Sepeda", 10000, ["Biru", "Merah", "Hijau"]),
}

# =================== STATIC CONTEXT ===================
with open("context.txt", "r", encoding="utf-8") as f:
    base_context = f.read()

# =================== AI FUNCTION ===================
def tanya_masyud():
    """
    Fungsi interaktif untuk bertanya ke AI customer service seputar penyewaan kendaraan.
    User dapat keluar dengan mengetik 'keluar', 'exit', atau 'quit'.
    Jawaban AI berdasarkan data dan konteks rental.
    """
    print("")
    print("=" * 120)
    print("(C) Copyright 2025 Rayud All Rights Reserved.")
    print("Rayud Masyud | Version 0.8 | Powered by Gemini.")
    print("Anda memasuki mode AI customer service. AI bersifat eksperimental dan mungkin akan membuat kesalahan. \nHarap periksa info penting. Ketik 'Pelajari Masyud' untuk info lebih lanjut.")
    print("Ketik 'keluar', 'exit', 'quit' untuk berhenti interaksi.")
    print("=" * 120)
    print("Masyud: Halo! Mau tanya apa seputar penyewaan?")
    while True:
        pertanyaan = input("Anda: ")
        if pertanyaan.lower() in ["keluar", "exit", "quit"]:
            print("Masyud: Oke, sampai jumpa!")
            break
        if pertanyaan.lower() in ["pelajari masyud"]:
            print("=" * 120)
            print("Masyud adalah AI (Artificial Intelligence) atau Kecerdasan Buatan yang mungkin akan membuat kesalahan. Masyud berbasis pada LLM buatan Google, yakni Gemini 1.5 Flash. \nDiskusikan apapun yang anda inginkan bersama Masyud. \nBagaimana cara kami menggunakan data anda? Kami (Rayud) tidak mengambil data apapun dari program ini. Data yang anda kirimkan melalui program ini akan langsung dikirimkan ke Google Gemini tanpa adanya interupsi dari Kami.")
            print("=" * 120)
            continue
        print("Masyud: [berfikir...]")
        full_prompt = f"""
        {base_context}

        Tolong jawab pertanyaan user berdasarkan data di atas.
        Jika ada perhitungan harga (jumlah hari, pajak, diskon), lakukan perhitungan langsung.
        Gunakan format rupiah dengan titik pemisah ribuan. Jangan jawab di luar data.

        User: {pertanyaan}
        """
        response = model.generate_content(full_prompt)
        print("Masyud:", response.text)

# =================== INPUT FUNCTION ===================
def input_user(prompt_text, choices=None, capitalize=False):
    """
    Mengambil input dari user dengan validasi pilihan dan fitur tanya AI.

    Args:
        prompt_text (str): Teks prompt untuk input.
        choices (list, optional): Daftar pilihan yang valid.
        capitalize (bool, optional): Apakah input perlu dikapitalisasi.

    Returns:
        str: Input user yang sudah divalidasi.
    """
    while True:
        user_input = input(prompt_text).strip()

        # Trigger AI 
        if user_input.lower().replace(" ", "") == "halomas":
            tanya_masyud()
            continue

        # Kalau ada pilihan yang valid
        if choices:
            # Normalisasi input biar fleksibel (bisa kecil, besar, campur)
            if (user_input in choices or user_input.lower() in [c.lower() for c in choices]):
                return user_input
            print(f"Input tidak valid. Pilihan: {', '.join(choices)}")
            continue

        # Kalau tidak ada choices, langsung return input
        return user_input
# =================== TABEL AWAL ===================
def tabelAwal():
    """
    Menampilkan tabel daftar kendaraan, harga, dan kategori yang tersedia untuk disewa.

    Tabel berisi 6 baris dan 4 kolom. Kolom pertama berisi nomor urut,
    kolom kedua berisi kendaraan mobil, kolom ketiga berisi kendaraan motor,
    dan kolom keempat berisi kendaraan sepeda.
    """
    data = [
        # Baris 1
        ["1", "G-Class - Rp 5.000.000/hari", "Harley Davidson RG - Rp 2.500.000/hari", "Sepeda Listrik - Rp 20.000/hari"],
        # Baris 2
        ["2", "BMW M4 - Rp 3.450.000/hari", "Yamaha R6 - Rp 700.000/hari", "Sepeda - Rp 10.000/hari"],
        # Baris 3
        ["3", "Porsche 911 - Rp 2.800.000/hari", "Honda CBR 1000 RR - Rp 1.500.000/hari", ""],
        # Baris 4
        ["4", "McLaren Senna - Rp 4.250.000/hari", "Yamaha XSR 155 - Rp 550.000/hari", ""],
        # Baris 5
        ["5", "Toyota GR Supra - Rp 3.000.000/hari", "Sportster 48 - Rp 1.500.000/hari", ""],
        # Baris 6
        ["6", "Toyota Alphard Hybrid - Rp 5.000.000/hari", "", ""],
    ]
    print("="*120)
    print("\n{:^120}".format("Apen Al-wawi Rent\n"))
    print("="*120)
    print("-"*120)
    # Judul tabel
    print(f"{'No':<5} | {'Mobil':<50} | {'Motor':<40} | {'Sepeda':<20}")
    print("-"*120)
    # Isi tabel
    for row in data:
        print(f"{row[0]:<5} | {row[1]:<50} | {row[2]:<40} | {row[3]:<20}")
    print("-"*120)

# =================== PILIH WARNA ===================
def pilih_warna(warnaTersedia):
    """
    Menampilkan pilihan warna kendaraan dan mengambil input warna dari user.

    Args:
        warnaTersedia (list): Daftar warna yang tersedia.

    Returns:
        str: Warna kendaraan yang dipilih user.
    """
    print("Pilihan warna tersedia:", ", ".join(warnaTersedia))
    return input_user("Pilih warna kendaraan: ", choices=warnaTersedia, capitalize=True)

# =================== MAIN PROGRAM ===================
tabelAwal()
print("Masukan jenis kendaraan yang akan di sewa dengan kode: ")
print("mb = Mobil, mk = Motor, s = Sepeda")
print("Contoh: mb1 untuk sewa mobil G-Class (nomor 1)")
print("="*120)
print("Ragu? Tanya ai masyud dengan ketik 'halo mas' di input manapun!")

# Ambil input kendaraan
kendaraan = input_user("Masukan jenis kendaraan yang akan di sewa : ").lower().replace(" ", "")
if kendaraan in pilihan:
    jenisKendaraan, harga, warnaTersedia = pilihan[kendaraan]
    print(f"Anda memilih {jenisKendaraan} dengan harga Rp {format_rupiah(harga)} per hari.")
    warna = pilih_warna(warnaTersedia)
    print(f"Anda memilih warna {warna} untuk kendaraan {jenisKendaraan}.")
else:
    print("Kode kendaraan tidak valid!")
    exit()

# =================== KONFIRMASI ===================
print("\n" * 2)
print("=" * 40)
print("Konfirmasi sewa kendaraan")
print("=" * 40)
print("Jenis kendaraan yang akan di sewa : ", jenisKendaraan)
print("Warna                             : ", warna)
print("--------------------------------------------------")
print("Harga sewa per hari : Rp", format_rupiah(harga))
print("--------------------------------------------------")

konfirmasi = input_user("Yakin akan sewa kendaraan ini? (Y/T) : ", choices=["Y","T"], capitalize=True)
if konfirmasi == "T":
    exit()

# =================== SOPIR ===================
Sopir = 250000
print("\n" * 2)
print("=" * 40)
print("Sopir")
print("=" * 40)
print("Harga sopir per hari : Rp", format_rupiah(Sopir))
sopir = input_user("Apakah anda ingin sewa sopir? (Y/T) : ", choices=["Y","T"], capitalize=True)
if sopir.upper() == "Y":
    hargaSopir = 250000
elif sopir.upper() == "T":
    hargaSopir = 0
else:
    print("Input tidak valid!")
# =================== HITUNG SUBTOTAL + PAJAK ===================
jumlahHari = int(input_user("Masukan jumlah hari sewa kendaraan : "))
totalHargaSopir = jumlahHari * hargaSopir
subtotal = jumlahHari * harga + totalHargaSopir
pajak = int(subtotal * 0.10)
totalSebelumDiskon = subtotal + pajak

# =================== FORMULIR PENYEWA ===================
print("\n" * 2)
print("=" * 20)
print("Formulir ketentuan penyewaan")
print("=" * 20)
nama = input_user("Masukan nama anda        : ")
alamat = input_user("Masukan alamat anda      : ")
telepon = input_user("Masukan nomor telepon    : ")
jenisKelamin = input_user("Masukan jenis kelamin    : ")

# =================== JENIS JAMINAN ===================
print("\n" + "="*20)
print("Jenis Jaminan")
print("="*20)
print("1. KTP\n2. Pasport\n3. SIM")
jaminan = input_user("Masukan jenis jaminan (1/2/3) : ", choices=["1","2","3"])
if jaminan == "1":
    jaminan = "KTP"
    nik = input_user("Masukan NIK anda : ")
elif jaminan == "2":
    jaminan = "Pasport"
    nomorPasport = input_user("Masukan Nomor Pasport anda : ")
elif jaminan == "3":
    jaminan = "SIM"
    nomorSIM = input_user("Masukan Nomor SIM anda : ")

# =================== DISKON ===================
diskonPersen = 0
if jumlahHari >= 14:
    diskonPersen = 0.10
elif jumlahHari >= 7:
    diskonPersen = 0.05
diskon = int(totalSebelumDiskon * diskonPersen)
totalSetelahDiskon = totalSebelumDiskon - diskon

# =================== VOUCHER ===================
voucher = input_user("Masukkan kode voucher (atau kosong jika tidak ada): ").upper()
diskonVoucher = 0
if voucher == "MERDEKA17":
    diskonVoucher = int(totalSetelahDiskon * 0.17)
    print(f"Voucher MERDEKA17 berhasil! Diskon tambahan Rp{format_rupiah(diskonVoucher)}")
elif voucher == "HEMAT5":
    diskonVoucher = int(totalSetelahDiskon * 0.05)
    print(f"Voucher HEMAT5 berhasil! Diskon tambahan Rp{format_rupiah(diskonVoucher)}")
elif voucher != "":
    print("Kode voucher tidak valid.")

grandTotal = totalSetelahDiskon - diskonVoucher

# =================== STRUK TAGIHAN ===================
print("\n" + "=" * 120)
print("                                                    Apen Al-wawi Rent")
print("=" * 120)
print("                                                    Bukti Penyewaan")
print("-" * 120)
print("Nama                         :", nama)
print("Alamat                       :", alamat)
print("Telepon                      :", telepon)
print("Jenis Kelamin                :", jenisKelamin)
print("Jenis Kendaraan              :", jenisKendaraan)
print("Warna                        :", warna)
print("Jumlah Hari Sewa             :", jumlahHari)
print("Harga Sewa                   : Rp", format_rupiah(harga))
print("Harga Sopir (", jumlahHari, "x", format_rupiah(hargaSopir),"): Rp", format_rupiah(totalHargaSopir))
print("Jumlah yang harus dibayar    : Rp", format_rupiah(grandTotal))

# =================== METODE PEMBAYARAN ===================
print("\n" + "=" * 20)
print("             Metode Pembayaran")
print("=" * 20)
print("1. Tunai\n2. Transfer")
pembayaran = input_user("Masukan metode pembayaran (1/2) : ", choices=["1","2"])

if pembayaran == "1":
    uang = int(input_user("Silakan isi jumlah uang yang akan dibayar : Rp"))
    kembalian = uang - grandTotal
    while kembalian < 0:
        print(f"Uang tidak cukup! Masih kurang Rp{format_rupiah(-kembalian)}")
        tambahan = int(input_user(f"Masukkan uang tambahan sebesar Rp{format_rupiah(-kembalian)}: "))
        uang += tambahan
        kembalian = uang - grandTotal

    # =================== CETAK STRUK ===================
    print("\n" + "=" * 120)
    print("                                                    Apen Al-wawi Rent")
    print("=" * 120)
    print("                                                    Bukti Pembayaran")
    print("-" * 120)
    print("Nama                                     :", nama)
    print("Alamat                                   :", alamat)
    print("Jenis Kelamin                            :", jenisKelamin)
    print(f"Nomor Telepon                           : {telepon}")
    print("--------------------------------------------------------------------------------------")
    print("Pesanan Anda:")
    print("-------------------------------------------------------------------------------------")
    print(f"Jenis Kendaraan                         : {jenisKendaraan}")
    print(f"Jumlah Hari                             : {jumlahHari}")
    print(f"Subtotal                                : Rp{format_rupiah(subtotal)}")
    print(f"Pajak (10%)                             : Rp{format_rupiah(pajak)}")
    if diskonPersen > 0:
        print(f"Diskon Durasi                       : Rp{format_rupiah(diskon)}")
    if diskonVoucher > 0:
        print(f"Voucher Diskon                      : Rp{format_rupiah(diskonVoucher)}")
    print("Harga Sopir (", jumlahHari, "x", format_rupiah(hargaSopir),"): Rp", format_rupiah(totalHargaSopir))
    print(f"Total Bayar                             : Rp{format_rupiah(grandTotal)}")
    print("Metode Pembayaran                        : Tunai")
    print("Nominal Pembayaran                       : Rp", format_rupiah(uang))
    print("Kembalian                                : Rp", format_rupiah(kembalian))
    print("=" * 120)

    with open("struk_penyewaan.txt", "w", encoding="utf-8") as f:
        f.write("==================================================\n")
        f.write("                Apen Al-wawi Rent\n")
        f.write("==================================================\n")
        f.write("Bukti Pembayaran\n")
        f.write("--------------------------------------------------\n")
        f.write(f"Nama             : {nama}\n")
        f.write(f"Alamat           : {alamat}\n")
        f.write(f"Jenis Kelamin    : {jenisKelamin}\n")
        f.write(f"No. Telepon      : {telepon}\n")
        f.write("--------------------------------------------------\n")
        f.write("Pesanan Anda:\n")
        f.write(f"Jenis Kendaraan  : {jenisKendaraan}\n")
        f.write(f"Jumlah Hari      : {jumlahHari}\n")
        f.write(f"Subtotal         : Rp{format_rupiah(subtotal)}\n")
        f.write(f"Pajak (10%)      : Rp{format_rupiah(pajak)}\n")
        if diskonPersen > 0:
            f.write(f"Diskon Durasi     : Rp{format_rupiah(diskon)}\n")
        if diskonVoucher > 0:
            f.write(f"Voucher Diskon    : Rp{format_rupiah(diskonVoucher)}\n")
        f.write(f"Harga Sopir ({jumlahHari} x {format_rupiah(hargaSopir)}): Rp{format_rupiah(totalHargaSopir)}\n")
        f.write(f"Nominal Dibayar  : Rp{format_rupiah(uang)}\n")
        f.write(f"Kembalian        : Rp{format_rupiah(kembalian)}\n")
        f.write("==================================================\n")
        print("Struk berhasil disimpan ke file: struk_penyewaan.txt")

elif pembayaran == "2":
    # =================== PEMBAYARAN TRANSFER ===================
    print("Metode pembayaran transfer")
    print("Silakan transfer ke rekening berikut:")
    print("Bank ABC - 123456789 a.n Apen Al-wawi Rent")
    print(f"Total yang harus ditransfer: Rp{format_rupiah(grandTotal)}")
    print("=" * 120)
    print("                     Terima kasih atas penyewaan Anda!")
    print("=" * 120)
else:
    print("Metode pembayaran tidak tersedia")

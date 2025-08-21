# Manajer Zakat

Aplikasi web untuk mengelola data pembayar zakat, melacak jumlah zakat yang terkumpul, dan melakukan operasi CRUD pada data pembayar.

## Keterangan
Program ini dibuat untuk menyelesaikan tugas Mata Kuliah Praktikum Pemrograman Berorientasi Objek.

## Anggota Kelompok
- Adam Arias Jauhari
- MHD Aldy Syahputra
- Vicky Maulana Romadan

## Fitur

- Menampilkan daftar pembayar zakat
- Menambah data pembayar baru
- Mengubah data pembayar
- Menghapus data pembayar
- Menampilkan total zakat terkumpul
- Menampilkan jumlah pembayar
- Validasi input form
- Responsif untuk berbagai ukuran layar

## Persyaratan Sistem

- Python 3.8 atau lebih baru
- pip (Python package manager)

## Instalasi

1. Clone repositori ini atau download sebagai ZIP
2. Buka terminal/command prompt
3. Navigasi ke direktori proyek
4. Buat virtual environment (opsional tapi direkomendasikan):
   ```bash
   python -m venv venv
   ```
5. Aktifkan virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
6. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Menjalankan Aplikasi

1. Pastikan virtual environment aktif
2. Jalankan aplikasi:
   ```bash
   python app.py
   ```
3. Buka browser dan akses:
   ```
   http://localhost:5000
   ```

## Struktur Proyek

```
manajer-zakat/
├── app.py              # File utama aplikasi Flask
├── requirements.txt    # Daftar dependensi Python
├── static/            # File statis (CSS, JavaScript)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── templates/         # Template HTML
    ├── base.html
    ├── index.html
    └── form.html
```

## Penggunaan

1. Halaman Utama:
   - Menampilkan daftar pembayar zakat
   - Menampilkan total zakat terkumpul
   - Menampilkan jumlah pembayar
   - Tombol untuk menambah pembayar baru

2. Form Tambah/Ubah Pembayar:
   - Input nama (wajib)
   - Input nomor telepon (wajib)
   - Input email (opsional)
   - Input jumlah zakat (wajib)
   - Validasi input otomatis

3. Operasi pada Data:
   - Tombol "Ubah" untuk mengedit data
   - Tombol "Hapus" dengan konfirmasi
   - Notifikasi sukses/error

## Petunjuk penggunaan environment Python 3.12

### 1. Download & Install Python 3.12
- Kunjungi https://www.python.org/downloads/release/python-3120/
- Download installer sesuai OS Anda (Windows/macOS/Linux)
- Install dan pastikan opsi "Add Python to PATH" dicentang

### 2. Buat Virtual Environment (opsional tapi direkomendasikan)
Buka terminal di folder project, lalu jalankan:

```
python -m venv venv
```

Aktifkan environment:
- Windows:
  ```
  .\venv\Scripts\activate
  ```
- macOS/Linux:
  ```
  source venv/bin/activate
  ```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```
python app.py
```

---

> **Catatan:**
> Jika Anda tetap menggunakan Python 3.13, aplikasi kemungkinan besar tidak akan berjalan karena masalah kompatibilitas library.

## Lisensi

Hak Cipta © 2024 Manajer Zakat. Hak Cipta Dilindungi.
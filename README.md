# Manajer Zakat

Aplikasi web untuk mengelola data pembayar zakat, melacak jumlah zakat yang terkumpul, dan melakukan operasi CRUD pada data pembayar.

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

## Lisensi

Hak Cipta © 2024 Manajer Zakat. Hak Cipta Dilindungi. 
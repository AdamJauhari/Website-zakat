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

## Cara Instalasi dan Menjalankan Aplikasi

### Cara Mudah (Otomatis)

#### Windows
1. Klik dua kali pada file `install.bat`
2. Aplikasi akan otomatis terinstal dan berjalan

#### Linux/macOS
1. Buka terminal pada direktori aplikasi
2. Jalankan perintah: `chmod +x install.sh`
3. Jalankan perintah: `./install.sh`
4. Aplikasi akan otomatis terinstal dan berjalan

### Cara Manual

1. Pastikan Python 3.7 atau lebih baru sudah terinstal
2. Buka terminal/command prompt pada direktori aplikasi
3. Instal dependensi dengan perintah:
   ```
   pip install -e .
   ```
4. Jalankan aplikasi dengan perintah:
   ```
   python app.py
   ```
5. Buka browser dan akses `http://127.0.0.1:5000`

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
import sys
import subprocess
import os
import shutil
import sqlite3

# Cek versi Python
if sys.version_info >= (3, 13):
    print('ERROR: Aplikasi ini belum mendukung Python 3.13 atau lebih baru karena masalah kompatibilitas library SQLAlchemy.')
    print('Silakan gunakan Python 3.12 atau lebih rendah.')
    sys.exit(1)

if sys.version_info < (3, 7):
    print('ERROR: Aplikasi ini membutuhkan minimal Python 3.7.')
    sys.exit(1)

try:
    import flask
except ImportError:
    print('Flask belum terinstall. Menginstall requirements...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    print('Requirements terinstall. Silakan jalankan ulang script ini.')
    sys.exit(1)

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Hapus direktori instance jika ada
instance_dir = 'instance'
if os.path.exists(instance_dir):
    try:
        shutil.rmtree(instance_dir)
        print(f"Direktori instance dihapus: {instance_dir}")
    except Exception as e:
        print(f"Gagal menghapus direktori instance: {e}")
    
# Buat direktori instance baru
os.makedirs(instance_dir, exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zakat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definisi model
class PembayarZakat(db.Model):
    __tablename__ = 'pembayar_zakat'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    nomor_telepon = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100))
    jenis_zakat = db.Column(db.String(50), nullable=False)
    jumlah_zakat = db.Column(db.Float, nullable=False)
    metode_pembayaran = db.Column(db.String(50), nullable=False, default='Tunai')
    tanggal_ditambahkan = db.Column(db.DateTime, default=datetime.utcnow)

# Fungsi untuk memastikan database dibuat dengan benar
def reset_database():
    with app.app_context():
        # Hapus semua tabel terlebih dahulu
        db.drop_all()
        print("Semua tabel dihapus.")
        
        # Buat tabel baru
        db.create_all()
        print("Database berhasil dibuat dengan struktur terbaru.")
        
        # Verifikasi struktur tabel
        conn = sqlite3.connect(os.path.join(instance_dir, 'zakat.db'))
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(pembayar_zakat)")
        columns = cursor.fetchall()
        print("Struktur tabel pembayar_zakat:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        conn.close()

# Reset database saat aplikasi dimulai
reset_database()

@app.route('/')
def index():
    pembayar = PembayarZakat.query.all()
    total_zakat = sum(p.jumlah_zakat for p in pembayar)
    jumlah_pembayar = len(pembayar)
    return render_template('index.html', 
                         pembayar=pembayar,
                         total_zakat=total_zakat,
                         jumlah_pembayar=jumlah_pembayar)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah_pembayar():
    if request.method == 'POST':
        try:
            pembayar = PembayarZakat(
                nama=request.form['nama'],
                nomor_telepon=request.form['nomor_telepon'],
                email=request.form['email'],
                jenis_zakat=request.form['jenis_zakat'],
                jumlah_zakat=float(request.form['jumlah_zakat']),
                metode_pembayaran=request.form['metode_pembayaran']
            )
            db.session.add(pembayar)
            db.session.commit()
            flash('Data pembayar berhasil ditambahkan!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
    return render_template('form.html')

@app.route('/ubah/<int:id>', methods=['GET', 'POST'])
def ubah_pembayar(id):
    pembayar = PembayarZakat.query.get_or_404(id)
    if request.method == 'POST':
        try:
            pembayar.nama = request.form['nama']
            pembayar.nomor_telepon = request.form['nomor_telepon']
            pembayar.email = request.form['email']
            pembayar.jenis_zakat = request.form['jenis_zakat']
            pembayar.jumlah_zakat = float(request.form['jumlah_zakat'])
            pembayar.metode_pembayaran = request.form['metode_pembayaran']
            db.session.commit()
            flash('Data pembayar berhasil diperbarui!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
    return render_template('form.html', pembayar=pembayar)

@app.route('/hapus/<int:id>', methods=['POST'])
def hapus_pembayar(id):
    pembayar = PembayarZakat.query.get_or_404(id)
    try:
        db.session.delete(pembayar)
        db.session.commit()
        flash('Data pembayar berhasil dihapus!', 'success')
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
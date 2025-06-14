import sys
import subprocess

# Cek dan install requirements jika ada yang belum terinstall
try:
    import flask
    import pandas
    import sqlalchemy
except ImportError:
    print('Beberapa requirements belum terinstall. Menginstall requirements...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    print('Requirements terinstall. Silakan jalankan ulang script ini.')
    sys.exit(1)

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sqlite3
import io
import pandas as pd
from flask import send_file

# Hapus direktori instance jika ada
# instance_dir = 'instance'
# if os.path.exists(instance_dir):
#     try:
#         shutil.rmtree(instance_dir)
#         print(f"Direktori instance dihapus: {instance_dir}")
#     except Exception as e:
#         print(f"Gagal menghapus direktori instance: {e}")
    
# Buat direktori instance baru
instance_dir = 'instance'
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
    jumlah_beras = db.Column(db.Float)
    selected_harga_beras_id = db.Column(db.Integer, db.ForeignKey('harga_beras.id'))
    jumlah_jiwa = db.Column(db.Integer, nullable=False, default=1)
    metode_pembayaran = db.Column(db.String(50), nullable=False, default='Tunai')
    tanggal_ditambahkan = db.Column(db.DateTime, default=datetime.utcnow)
    tanggal_bayar = db.Column(db.Date, default=datetime.utcnow().date())
    nominal_dibayar = db.Column(db.Float, nullable=True)

    selected_harga_beras = db.relationship('HargaBeras', backref='pembayar_zakat')

class HargaBeras(db.Model):
    __tablename__ = 'harga_beras'
    id = db.Column(db.Integer, primary_key=True)
    harga = db.Column(db.Float, nullable=False)
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
        
        # Verifikasi struktur tabel harga_beras
        cursor.execute("PRAGMA table_info(harga_beras)")
        columns_beras = cursor.fetchall()
        print("Struktur tabel harga_beras:")
        for col in columns_beras:
            print(f"  - {col[1]} ({col[2]})")
        conn.close()

# Reset database saat aplikasi dimulai
# reset_database()

@app.route('/beras_data')
def beras_data():
    harga_beras_list = HargaBeras.query.order_by(HargaBeras.tanggal_ditambahkan.desc()).all()
    return render_template('beras_data.html', harga_beras_list=harga_beras_list)

@app.route('/tambah_beras', methods=['GET', 'POST'])
def tambah_beras():
    if request.method == 'POST':
        try:
            harga = float(request.form['harga'])
            new_harga_beras = HargaBeras(harga=harga)
            db.session.add(new_harga_beras)
            db.session.commit()
            flash('Data harga beras berhasil ditambahkan!', 'success')
            return redirect(url_for('beras_data'))
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
    return render_template('form_beras.html')

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
    harga_beras_list = HargaBeras.query.all()
    if request.method == 'POST':
        try:
            jenis_zakat = request.form['jenis_zakat']

            jumlah_zakat_value = 0.0
            jumlah_beras_value = None
            selected_harga_beras_id = None
            jumlah_jiwa_value = 1
            nominal_dibayar_value = None
            if 'jumlah_jiwa' in request.form and request.form['jumlah_jiwa']:
                jumlah_jiwa_value = int(request.form['jumlah_jiwa'])
            if jenis_zakat == 'Zakat Beras':
                if 'jumlah_beras' in request.form and request.form['jumlah_beras']:
                    jumlah_beras_value = float(request.form['jumlah_beras'])
                if 'selected_harga_beras' in request.form and request.form['selected_harga_beras']:
                    selected_harga_beras_id = int(request.form['selected_harga_beras'])
                    harga_beras_obj = HargaBeras.query.get(selected_harga_beras_id)
                    harga_per_kg = harga_beras_obj.harga if harga_beras_obj else 0
                    jumlah_zakat_value = jumlah_jiwa_value * jumlah_beras_value * harga_per_kg
                    nominal_dibayar_value = jumlah_zakat_value
            else:
                if 'jumlah_zakat' in request.form and request.form['jumlah_zakat']:
                    jumlah_zakat_value = float(request.form['jumlah_zakat'])
                nominal_dibayar_value = jumlah_zakat_value

            tanggal_bayar_str = request.form['tanggal_bayar']
            tanggal_bayar_obj = datetime.strptime(tanggal_bayar_str, '%Y-%m-%d').date() if tanggal_bayar_str else datetime.utcnow().date()

            pembayar = PembayarZakat(
                nama=request.form['nama'],
                nomor_telepon=request.form['nomor_telepon'],
                email=request.form['email'],
                jenis_zakat=jenis_zakat,
                jumlah_zakat=jumlah_zakat_value,
                jumlah_beras=jumlah_beras_value,
                selected_harga_beras_id=selected_harga_beras_id,
                jumlah_jiwa=jumlah_jiwa_value,
                metode_pembayaran=request.form['metode_pembayaran'],
                tanggal_bayar=tanggal_bayar_obj,
                nominal_dibayar=nominal_dibayar_value
            )
            db.session.add(pembayar)
            db.session.commit()
            flash('Data pembayar berhasil ditambahkan!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
    return render_template('form.html', harga_beras_list=harga_beras_list, datetime=datetime)

@app.route('/ubah/<int:id>', methods=['GET', 'POST'])
def ubah_pembayar(id):
    pembayar = PembayarZakat.query.get_or_404(id)
    harga_beras_list = HargaBeras.query.all()
    if request.method == 'POST':
        try:
            pembayar.nama = request.form['nama']
            pembayar.nomor_telepon = request.form['nomor_telepon']
            pembayar.email = request.form['email']
            pembayar.jenis_zakat = request.form['jenis_zakat']

            if 'jumlah_zakat' in request.form and request.form['jumlah_zakat']:
                pembayar.jumlah_zakat = float(request.form['jumlah_zakat'])
            else:
                pembayar.jumlah_zakat = 0.0 # Default or existing value if empty

            if pembayar.jenis_zakat == 'Zakat Beras' and 'jumlah_beras' in request.form and request.form['jumlah_beras']:
                pembayar.jumlah_beras = float(request.form['jumlah_beras'])
            else:
                pembayar.jumlah_beras = None

            if pembayar.jenis_zakat == 'Zakat Beras' and 'selected_harga_beras' in request.form and request.form['selected_harga_beras']:
                pembayar.selected_harga_beras_id = int(request.form['selected_harga_beras'])
            else:
                pembayar.selected_harga_beras_id = None

            if 'jumlah_jiwa' in request.form and request.form['jumlah_jiwa']:
                pembayar.jumlah_jiwa = int(request.form['jumlah_jiwa'])
            else:
                pembayar.jumlah_jiwa = 1 # Default or existing value if empty

            pembayar.metode_pembayaran = request.form['metode_pembayaran']
            tanggal_bayar_str = request.form['tanggal_bayar']
            pembayar.tanggal_bayar = datetime.strptime(tanggal_bayar_str, '%Y-%m-%d').date() if tanggal_bayar_str else datetime.utcnow().date()

            if 'nominal_dibayar' in request.form and request.form['nominal_dibayar']:
                pembayar.nominal_dibayar = float(request.form['nominal_dibayar'])
            else:
                if pembayar.jenis_zakat != 'Zakat Beras':
                    pembayar.nominal_dibayar = pembayar.jumlah_zakat
                else:
                    pembayar.nominal_dibayar = None # Set to None if empty

            db.session.commit()
            flash('Data pembayar berhasil diperbarui!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
    return render_template('form.html', pembayar=pembayar, harga_beras_list=harga_beras_list, datetime=datetime)

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

@app.route('/history_pembayaran')
def history_pembayaran():
    pembayar_history = PembayarZakat.query.order_by(PembayarZakat.tanggal_bayar.desc()).all()
    return render_template('history_pembayaran.html', pembayar_history=pembayar_history)

@app.route('/export_excel')
def export_excel():
    data = PembayarZakat.query.all()
    rows = []
    for p in data:
        rows.append({
            'ID': p.id,
            'Nama': p.nama,
            'Nomor Telepon': p.nomor_telepon,
            'Email': p.email,
            'Jenis Zakat': p.jenis_zakat,
            'Jumlah Zakat': p.jumlah_zakat,
            'Jumlah Beras': p.jumlah_beras,
            'Jumlah Jiwa': p.jumlah_jiwa,
            'Metode Pembayaran': p.metode_pembayaran,
            'Tanggal Bayar': p.tanggal_bayar.strftime('%d/%m/%Y'),
            'Tanggal Ditambahkan': p.tanggal_ditambahkan.strftime('%d/%m/%Y %H:%M'),
        })
    df = pd.DataFrame(rows)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='History Pembayaran')
    output.seek(0)
    return send_file(output, download_name='history_pembayaran.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
import io
import pandas as pd
from flask import send_file
from .app import app, PembayarZakat

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

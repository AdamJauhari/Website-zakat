// Form validation
(function () {
    'use strict'
    
    // Fetch all forms we want to apply validation to
    var forms = document.querySelectorAll('.needs-validation')
    
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            
            form.classList.add('was-validated')
        }, false)
    })
})()

// Delete confirmation
function konfirmasiHapus(id, nama) {
    const modal = new bootstrap.Modal(document.getElementById('modalHapus'))
    document.getElementById('namaPembayar').textContent = nama
    document.getElementById('formHapus').action = `/hapus/${id}`
    modal.show()
}

// Format currency input
document.addEventListener('DOMContentLoaded', function() {
    const jumlahZakatInput = document.getElementById('jumlah_zakat')
    if (jumlahZakatInput) {
        jumlahZakatInput.addEventListener('input', function(e) {
            // Remove non-numeric characters except decimal point
            let value = e.target.value.replace(/[^\d.]/g, '')
            
            // Ensure only one decimal point
            const parts = value.split('.')
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('')
            }
            
            // Limit to 2 decimal places
            if (parts.length > 1 && parts[1].length > 2) {
                value = parts[0] + '.' + parts[1].substring(0, 2)
            }
            
            e.target.value = value
        })
    }

    // Kalkulasi otomatis total bayar dan nominal dibayar untuk zakat beras berdasarkan jumlah jiwa dan jumlah kg
    const jumlahJiwaInput = document.getElementById('jumlah_jiwa');
    const jumlahBerasInput = document.getElementById('jumlah_beras');
    const hargaBerasSelect = document.getElementById('selected_harga_beras');
    const totalBayarInput = document.getElementById('total_bayar');
    const nominalDibayarInput = document.getElementById('nominal_dibayar');

    function updateTotalBayarDanNominal() {
        if (jumlahJiwaInput && jumlahBerasInput && hargaBerasSelect) {
            const jumlahJiwa = parseInt(jumlahJiwaInput.value) || 0;
            const jumlahBeras = parseFloat(jumlahBerasInput.value) || 0;
            const selectedOption = hargaBerasSelect.options[hargaBerasSelect.selectedIndex];
            const hargaPerKg = selectedOption ? parseFloat(selectedOption.getAttribute('data-harga')) || 0 : 0;
            const total = jumlahJiwa * jumlahBeras * hargaPerKg;
            if (totalBayarInput) totalBayarInput.value = total ? total.toLocaleString('id-ID', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : '';
            if (nominalDibayarInput) nominalDibayarInput.value = total ? total.toFixed(2) : '';
        }
    }

    if (jumlahJiwaInput) jumlahJiwaInput.addEventListener('input', updateTotalBayarDanNominal);
    if (jumlahBerasInput) jumlahBerasInput.addEventListener('input', updateTotalBayarDanNominal);
    if (hargaBerasSelect) hargaBerasSelect.addEventListener('change', updateTotalBayarDanNominal);

    // Inisialisasi saat halaman load
    updateTotalBayarDanNominal();
})
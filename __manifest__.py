# -*- coding: utf-8 -*-
{
    'name': 'AIRIV Payroll Indonesia - PPh 21 TER & BPJS Calculation Engine',
    'version': '18.0.1.0.0',
    'category': 'AIRIV/People & Payroll',
    'summary': 'Kalkulasi Otomatis PPh 21 Tarif Efektif Rata-rata (TER PP 58/2023) & BPJS Ketenagakerjaan/Kesehatan',
    'description': """
Modul Penggajian dan PPh 21 Indonesia Terintegrasi Sesuai PP 58/2023 & PMK 168/2023:
- Perhitungan Otomatis PPh 21 TER (Kategori A, B, C) untuk Pegawai Tetap & Tidak Tetap.
- Perhitungan BPJS Ketenagakerjaan (JKK, JKM, JHT, JP) & BPJS Kesehatan.
- Batch Penggajian (Payslip Batch) dengan Rekonsiliasi Finansial.
- Export Bukti Potong 1721-A1 & Rekap Gaji Transfer Bank.
""",
    'author': 'AIRIV',
    'website': 'https://airiv.id',
    'url': 'https://github.com/arivonto/airiv_payroll_indonesia/blob/18.0/static/description/index.html',
    'license': 'LGPL-3',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'price': 0.0,
    'currency': 'EUR',
    'depends': [
        'base',
        'hr',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/pph21_ter_data.xml',
        'views/payroll_views.xml',
        'views/payslip_batch_views.xml',
        'views/payroll_menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# -*- coding: utf-8 -*-
{
    'name': 'Indonesian Payroll & Tax Compliance (PPh 21 TER & BPJS)',
    'version': '18.0.1.0.0',
    'category': 'Human Resources/Payroll',
    'summary': 'Indonesian Payroll Localization: PPh 21 TER, BPJS Kesehatan & Ketenagakerjaan Compliance for Odoo 18',
    'description': '\nIndonesian Payroll & Tax Compliance (PPh 21 TER & BPJS)\n======================================================\nComprehensive Indonesian payroll localization compliant with Directorate General of Taxes (DJP) PP 58/2023 & PMK 168/2023.\n\nKey Features:\n-------------\n* **PPh 21 TER Calculation:** Automatically applies TER Categories (A, B, C) for monthly withholding and December gross-up / regular reconciliation.\n* **BPJS Integration:**\n  - BPJS Kesehatan (4% Company, 1% Employee with maximum cap).\n  - BPJS Ketenagakerjaan: JHT (3.7% / 2%), JKK (Risk-graded), JKM (0.3%), and JP (2% / 1% with capped base).\n* **Indonesian PTKP Rules:** Full support for TK/0-TK/3, K/0-K/3, and KI/0-KI/3 classifications.\n* **Automated Payslip Slip PDF:** Ready-to-print salary slips formatted in IDR currency (Rp) and Indonesian standard terminology.\n* **DJP e-Bupot & Coretax Ready:** Structured exports for Indonesian withholding tax reporting.\n    ',
    'author': 'Riv Cloud Management',
    'website': 'https://airiv.id',
    'license': 'LGPL-3',
    'depends': ['base', 'hr'],
    'data': ['security/ir.model.access.csv', 'wizard/ebupot_export_wizard_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 0.0,
}

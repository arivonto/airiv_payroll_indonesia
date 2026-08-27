# -*- coding: utf-8 -*-
import io
import csv
import base64
from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class EbupotExportWizard(models.TransientModel):
    _name = 'airiv.ebupot.export'
    _description = 'DJP Coretax / e-Bupot 21/26 CSV Export Wizard'

    month = fields.Selection([
        ('01', 'Januari'), ('02', 'Februari'), ('03', 'Maret'),
        ('04', 'April'),   ('05', 'Mei'),      ('06', 'Juni'),
        ('07', 'Juli'),    ('08', 'Agustus'),  ('09', 'September'),
        ('10', 'Oktober'), ('11', 'November'), ('12', 'Desember'),
    ], string='Masa Pajak', required=True, default=lambda self: f"{date.today().month:02d}")
    
    year = fields.Char(string='Tahun Pajak', required=True, default=lambda self: str(date.today().year))
    tax_object_code = fields.Selection([
        ('21-100-01', '21-100-01 (Pegawai Tetap / Bulanan)'),
        ('21-100-02', '21-100-02 (Pensiunan Berkala)'),
        ('21-100-03', '21-100-03 (Pegawai Tidak Tetap / Harian)'),
    ], string='Kode Objek Pajak', required=True, default='21-100-01')
    
    tax_period_type = fields.Selection([
        ('monthly', 'Masa Bulanan (Jan - Nov)'),
        ('december', 'Masa Pajak Terakhir (Desember / Tahunan)'),
    ], string='Jenis Masa Pajak', default='monthly', required=True)

    data_file = fields.Binary(string='File CSV e-Bupot', readonly=True)
    file_name = fields.Char(string='Nama File', readonly=True)
    total_records = fields.Integer(string='Jumlah Record', readonly=True)
    total_gross = fields.Monetary(string='Total Bruto (IDR)', readonly=True, currency_field='currency_id')
    total_tax = fields.Monetary(string='Total PPh 21 (IDR)', readonly=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], default='draft')

    def action_generate_csv(self):
        self.ensure_one()
        Payslip = self.env['airiv.payslip']
        
        domain = []
        if 'month' in Payslip._fields and 'year' in Payslip._fields:
            domain = [('month', '=', self.month), ('year', '=', self.year)]
        elif 'date_from' in Payslip._fields:
            domain = [('date_from', '>=', f"{self.year}-{self.month}-01")]
        
        slips = Payslip.search(domain)
        if not slips:
            slips = Payslip.search([])

        if not slips:
            raise UserError(_("Tidak ditemukan data payslip aktif untuk Masa %s Tahun %s.") % (self.month, self.year))

        output = io.StringIO()
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        headers = [
            'Masa Pajak', 'Tahun Pajak', 'Pembetulan',
            'NPWP Pemotong', 'NPWP / NIK Penerima', 'Nama Penerima',
            'Kode Objek Pajak', 'Penghasilan Bruto', 'Tarif TER / Efektif (%)',
            'Jumlah PPh Dipotong', 'Kode PTKP', 'Nomor Bukti Potong'
        ]
        writer.writerow(headers)

        company_npwp = self.env.company.vat or '0000000000000000'
        tot_gross = 0.0
        tot_tax = 0.0
        rec_count = 0

        for slip in slips:
            emp = slip.employee_id
            emp_tax_id = getattr(emp, 'identification_id', False) or getattr(emp, 'vat', False) or '0000000000000000'
            ptkp = getattr(slip, 'ptkp_status', False) or getattr(emp, 'ptkp_status', 'TK/0')
            gross = getattr(slip, 'gross_salary', getattr(slip, 'wage_basic', 0.0))
            tax = getattr(slip, 'pph21_amount', 0.0)

            rate_pct = round((tax / gross * 100), 2) if gross > 0 else 0.0
            bupot_no = f"BP21-{self.year}{self.month}-{emp.id:04d}"

            writer.writerow([
                int(self.month),
                int(self.year),
                0,
                company_npwp.replace('.', '').replace('-', ''),
                str(emp_tax_id).replace('.', '').replace('-', ''),
                emp.name,
                self.tax_object_code.split(' ')[0],
                int(round(gross)),
                rate_pct,
                int(round(tax)),
                ptkp,
                bupot_no
            ])

            tot_gross += gross
            tot_tax += tax
            rec_count += 1

        csv_data = output.getvalue().encode('utf-8')
        output.close()

        self.write({
            'data_file': base64.b64encode(csv_data),
            'file_name': f"ebupot_2126_masa_{self.month}_{self.year}.csv",
            'total_records': rec_count,
            'total_gross': tot_gross,
            'total_tax': tot_tax,
            'state': 'done'
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'airiv.ebupot.export',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

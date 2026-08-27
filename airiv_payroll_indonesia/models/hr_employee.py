# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    nik = fields.Char(string="NIK (Nomor Induk Kependudukan)", size=16, index=True, tracking=True)
    npwp = fields.Char(string="NPWP", size=20, index=True, tracking=True)
    
    # BPJS Numbers & Aliases
    bpjs_tk_number = fields.Char(string="Nomor KPJ BPJS TK", tracking=True)
    bpjs_tk_no = fields.Char(string="No. BPJS TK (Alias)", related="bpjs_tk_number", store=True, readonly=False)
    
    bpjs_kes_number = fields.Char(string="Nomor BPJS Kesehatan", tracking=True)
    bpjs_kes_no = fields.Char(string="No. BPJS Kesehatan (Alias)", related="bpjs_kes_number", store=True, readonly=False)
    
    # Salary & Allowance Fields expected by core/extended views
    wage_basic = fields.Monetary(string="Gaji Pokok Dasar", default=5000000.0, tracking=True)
    wage = fields.Monetary(string="Gaji Pokok (Alias)", related="wage_basic", store=True, readonly=False)
    allowance_fixed = fields.Monetary(string="Tunjangan Tetap", default=0.0, tracking=True)
    allowance_variable = fields.Monetary(string="Tunjangan Tidak Tetap", default=0.0, tracking=True)
    allowance_transport = fields.Monetary(string="Tunjangan Transportasi", default=0.0, tracking=True)
    allowance_meal = fields.Monetary(string="Tunjangan Makan", default=0.0, tracking=True)
    
    # Currency for monetary fields
    currency_id = fields.Many2one('res.currency', string="Mata Uang", default=lambda self: self.env.company.currency_id)

    # BPJS Participation Flags
    ikut_jp = fields.Boolean(string="Ikut BPJS Jaminan Pensiun (JP)", default=True, tracking=True)
    ikut_jht = fields.Boolean(string="Ikut BPJS Jaminan Hari Tua (JHT)", default=True, tracking=True)
    ikut_jkk = fields.Boolean(string="Ikut BPJS JKK", default=True, tracking=True)
    ikut_jkm = fields.Boolean(string="Ikut BPJS JKM", default=True, tracking=True)
    ikut_bpjs_kes = fields.Boolean(string="Ikut BPJS Kesehatan", default=True, tracking=True)
    
    # JKK Risk Group
    jkk_risk_group = fields.Selection([
        ('very_low', 'Sangat Rendah (0.24%)'),
        ('low', 'Rendah (0.54%)'),
        ('medium', 'Sedang (0.89%)'),
        ('high', 'Tinggi (1.27%)'),
        ('very_high', 'Sangat Tinggi (1.74%)'),
    ], string="Kelompok Risiko JKK", default='low', tracking=True)
    
    ptkp_status = fields.Selection([
        ('tk0', 'TK/0'), ('tk1', 'TK/1'), ('tk2', 'TK/2'), ('tk3', 'TK/3'),
        ('k0', 'K/0'), ('k1', 'K/1'), ('k2', 'K/2'), ('k3', 'K/3'),
    ], string="Status PTKP", default='tk0', tracking=True)
    
    metode_pph21 = fields.Selection([
        ('gross', 'Gross (Karyawan Tanggung Sendiri)'),
        ('net', 'Net (Ditanggung Perusahaan)'),
        ('gross_up', 'Gross Up (Tunjangan Pajak)'),
    ], string="Metode Pemotongan PPh 21", default='gross', tracking=True)

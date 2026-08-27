# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date

class AirivPayroll(models.Model):
    _name = 'airiv.payroll'
    _description = 'Slip Gaji Karyawan & Kalkulasi PPh 21 TER / BPJS'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_to desc, id desc'

    name = fields.Char(string="Nomor Slip", default="New", copy=False, readonly=True)
    employee_id = fields.Many2one('hr.employee', string="Karyawan", required=True, tracking=True)
    nik = fields.Char(string="NIK (KTP)", related="employee_id.identification_id", readonly=True)
    npwp = fields.Char(string="NPWP", tracking=True)
    
    company_id = fields.Many2one('res.company', string="Perusahaan", default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one('res.currency', string="Mata Uang", related='company_id.currency_id', readonly=True)
    
    batch_id = fields.Many2one('airiv.payslip.batch', string="Batch Gaji", ondelete='cascade')
    date_from = fields.Date(string="Periode Dari", required=True, default=lambda self: date.today().replace(day=1))
    date_to = fields.Date(string="Periode Sampai", required=True, default=lambda self: date.today())
    
    # PTKP & TER Mapping (PP 58/2023)
    ptkp_status = fields.Selection([
        ('tk0', 'TK/0 (Rp 54.000.000)'),
        ('tk1', 'TK/1 (Rp 58.500.000)'),
        ('tk2', 'TK/2 (Rp 63.000.000)'),
        ('tk3', 'TK/3 (Rp 67.500.000)'),
        ('k0', 'K/0 (Rp 58.500.000)'),
        ('k1', 'K/1 (Rp 63.000.000)'),
        ('k2', 'K/2 (Rp 67.500.000)'),
        ('k3', 'K/3 (Rp 72.000.000)'),
    ], string="Status PTKP", default='tk0', required=True, tracking=True)
    
    ter_category = fields.Selection([
        ('A', 'Kategori TER A (TK/0, TK/1, K/0)'),
        ('B', 'Kategori TER B (TK/2, TK/3, K/1, K/2)'),
        ('C', 'Kategori TER C (K/3)'),
    ], string="Kategori TER", compute="_compute_ter_category", store=True)

    # Earnings (Penghasilan Bruto)
    basic_salary = fields.Monetary(string="Gaji Pokok", required=True, tracking=True)
    allowance_fixed = fields.Monetary(string="Tunjangan Tetap", default=0.0)
    allowance_variable = fields.Monetary(string="Tunjangan Tidak Tetap / Lembur", default=0.0)
    overtime_amount = fields.Monetary(string="Uang Lembur", default=0.0)
    bonus_thr = fields.Monetary(string="Bonus / THR", default=0.0)
    
    # BPJS Perusahaan (Komponen Bruto Pajak)
    bpjs_jkk_company = fields.Monetary(string="JKK Perusahaan (0.24% - 1.74%)", compute="_compute_bpjs", store=True)
    bpjs_jkm_company = fields.Monetary(string="JKM Perusahaan (0.30%)", compute="_compute_bpjs", store=True)
    bpjs_kes_company = fields.Monetary(string="BPJS Kes Perusahaan (4.0%)", compute="_compute_bpjs", store=True)
    
    gross_wage = fields.Monetary(string="Penghasilan Bruto (PPh 21)", compute="_compute_gross_wage", store=True, tracking=True)
    
    # PPh 21 Calculation
    ter_rate = fields.Float(string="Tarif Efektif (TER %)", compute="_compute_pph21", store=True, digits=(5, 3))
    pph21_amount = fields.Monetary(string="Potongan PPh 21", compute="_compute_pph21", store=True, tracking=True)
    
    # BPJS Karyawan (Deductions)
    bpjs_jht_employee = fields.Monetary(string="JHT Karyawan (2.0%)", compute="_compute_bpjs", store=True)
    bpjs_jp_employee = fields.Monetary(string="JP Karyawan (1.0%)", compute="_compute_bpjs", store=True)
    bpjs_kes_employee = fields.Monetary(string="BPJS Kes Karyawan (1.0%)", compute="_compute_bpjs", store=True)
    
    bpjs_tk_total = fields.Monetary(string="Total BPJS TK (Karyawan)", compute="_compute_bpjs", store=True)
    bpjs_kes_total = fields.Monetary(string="Total BPJS Kes (Karyawan)", compute="_compute_bpjs", store=True)
    
    other_deductions = fields.Monetary(string="Potongan Lainnya / Kasbon", default=0.0)
    total_deductions = fields.Monetary(string="Total Potongan", compute="_compute_net_wage", store=True)
    net_wage = fields.Monetary(string="Gaji Bersih Diterima (THP)", compute="_compute_net_wage", store=True, tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('calculated', 'Dihitung'),
        ('verified', 'Diverifikasi HR'),
        ('paid', 'Lunas / Ditransfer'),
        ('cancel', 'Dibatalkan'),
    ], string="Status", default='draft', required=True, tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('airiv.payroll') or _('SLIP/%s') % fields.Date.today().strftime('%Y%m%d')
        return super().create(vals_list)

    @api.depends('ptkp_status')
    def _compute_ter_category(self):
        for rec in self:
            if rec.ptkp_status in ['tk0', 'tk1', 'k0']:
                rec.ter_category = 'A'
            elif rec.ptkp_status in ['tk2', 'tk3', 'k1', 'k2']:
                rec.ter_category = 'B'
            elif rec.ptkp_status == 'k3':
                rec.ter_category = 'C'
            else:
                rec.ter_category = 'A'

    @api.depends('basic_salary', 'allowance_fixed')
    def _compute_bpjs(self):
        for rec in self:
            base_wage = rec.basic_salary + rec.allowance_fixed
            cap_kes = min(base_wage, 12000000.0)
            cap_jp = min(base_wage, 10042300.0)
            
            rec.bpjs_jkk_company = base_wage * 0.0024
            rec.bpjs_jkm_company = base_wage * 0.0030
            rec.bpjs_kes_company = cap_kes * 0.0400
            
            rec.bpjs_jht_employee = base_wage * 0.0200
            rec.bpjs_jp_employee = cap_jp * 0.0100
            rec.bpjs_kes_employee = cap_kes * 0.0100
            
            rec.bpjs_tk_total = rec.bpjs_jht_employee + rec.bpjs_jp_employee
            rec.bpjs_kes_total = rec.bpjs_kes_employee

    @api.depends('basic_salary', 'allowance_fixed', 'allowance_variable', 'overtime_amount', 'bonus_thr', 'bpjs_jkk_company', 'bpjs_jkm_company', 'bpjs_kes_company')
    def _compute_gross_wage(self):
        for rec in self:
            rec.gross_wage = (rec.basic_salary + rec.allowance_fixed + rec.allowance_variable + 
                              rec.overtime_amount + rec.bonus_thr + rec.bpjs_jkk_company + 
                              rec.bpjs_jkm_company + rec.bpjs_kes_company)

    @api.depends('gross_wage', 'ter_category')
    def _compute_pph21(self):
        for rec in self:
            g = rec.gross_wage
            rate = 0.0
            cat = rec.ter_category or 'A'
            
            if cat == 'A':
                if g <= 5400000: rate = 0.0
                elif g <= 5650000: rate = 0.0025
                elif g <= 5950000: rate = 0.005
                elif g <= 6300000: rate = 0.0075
                elif g <= 6750000: rate = 0.01
                elif g <= 7500000: rate = 0.0125
                elif g <= 8550000: rate = 0.015
                elif g <= 9650000: rate = 0.0175
                elif g <= 10050000: rate = 0.02
                elif g <= 10350000: rate = 0.0225
                elif g <= 10700000: rate = 0.025
                elif g <= 11050000: rate = 0.03
                elif g <= 11600000: rate = 0.035
                elif g <= 12500000: rate = 0.04
                elif g <= 13750000: rate = 0.05
                elif g <= 15100000: rate = 0.06
                elif g <= 16950000: rate = 0.07
                elif g <= 19750000: rate = 0.08
                elif g <= 24150000: rate = 0.09
                elif g <= 26450000: rate = 0.10
                else: rate = 0.15
            elif cat == 'B':
                if g <= 6200000: rate = 0.0
                elif g <= 6500000: rate = 0.0025
                elif g <= 6850000: rate = 0.005
                elif g <= 7300000: rate = 0.0075
                elif g <= 9200000: rate = 0.01
                elif g <= 10750000: rate = 0.015
                elif g <= 12550000: rate = 0.02
                elif g <= 14950000: rate = 0.04
                elif g <= 17650000: rate = 0.06
                elif g <= 20150000: rate = 0.08
                else: rate = 0.15
            else:
                if g <= 6600000: rate = 0.0
                elif g <= 6950000: rate = 0.0025
                elif g <= 7350000: rate = 0.005
                elif g <= 7800000: rate = 0.0075
                elif g <= 8850000: rate = 0.01
                elif g <= 10650000: rate = 0.015
                elif g <= 12600000: rate = 0.02
                elif g <= 15100000: rate = 0.04
                elif g <= 18050000: rate = 0.06
                elif g <= 20550000: rate = 0.08
                else: rate = 0.15
                
            rec.ter_rate = rate * 100.0
            rec.pph21_amount = g * rate

    @api.depends('gross_wage', 'pph21_amount', 'bpjs_jht_employee', 'bpjs_jp_employee', 'bpjs_kes_employee', 'other_deductions', 'bpjs_jkk_company', 'bpjs_jkm_company', 'bpjs_kes_company')
    def _compute_net_wage(self):
        for rec in self:
            rec.total_deductions = rec.pph21_amount + rec.bpjs_jht_employee + rec.bpjs_jp_employee + rec.bpjs_kes_employee + rec.other_deductions
            take_home_gross = rec.basic_salary + rec.allowance_fixed + rec.allowance_variable + rec.overtime_amount + rec.bonus_thr
            rec.net_wage = take_home_gross - rec.total_deductions

    def action_calculate(self):
        self._compute_ter_category()
        self._compute_bpjs()
        self._compute_gross_wage()
        self._compute_pph21()
        self._compute_net_wage()
        self.write({'state': 'calculated'})

    def action_verify(self):
        self.write({'state': 'verified'})

    def action_mark_paid(self):
        self.write({'state': 'paid'})

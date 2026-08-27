# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date
import calendar

class AirivPayslipBatch(models.Model):
    _name = 'airiv.payslip.batch'
    _description = 'Batch Penggajian Karyawan & Rekonsiliasi PPh 21 TER / BPJS'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_end desc, id desc'

    name = fields.Char(string="Nama Batch Penggajian", required=True, tracking=True)
    date_start = fields.Date(string="Periode Mulai", required=True, default=lambda self: date.today().replace(day=1), tracking=True)
    date_end = fields.Date(string="Periode Selesai", required=True, default=lambda self: date.today().replace(day=calendar.monthrange(date.today().year, date.today().month)[1]), tracking=True)
    
    company_id = fields.Many2one('res.company', string="Perusahaan", default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one('res.currency', string="Mata Uang", related='company_id.currency_id', readonly=True)
    
    payslip_ids = fields.One2many('airiv.payroll', 'batch_id', string="Daftar Slip Gaji")
    payslip_count = fields.Integer(string="Jumlah Karyawan", compute="_compute_totals", store=True)
    
    # Financial Totals (IDR)
    total_gross = fields.Monetary(string="Total Gaji Bruto", compute="_compute_totals", store=True, tracking=True)
    total_pph21 = fields.Monetary(string="Total PPh 21 TER", compute="_compute_totals", store=True, tracking=True)
    total_bpjs_tk = fields.Monetary(string="Total BPJS Ketenagakerjaan", compute="_compute_totals", store=True)
    total_bpjs_kes = fields.Monetary(string="Total BPJS Kesehatan", compute="_compute_totals", store=True)
    total_net = fields.Monetary(string="Total Gaji Bersih (THP)", compute="_compute_totals", store=True, tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('computed', 'Dihitung'),
        ('approved', 'Disetujui'),
        ('paid', 'Selesai / Dibayar'),
        ('cancel', 'Dibatalkan'),
    ], string="Status Batch", default='draft', required=True, tracking=True)

    @api.depends('payslip_ids.gross_wage', 'payslip_ids.pph21_amount', 'payslip_ids.bpjs_tk_total', 'payslip_ids.bpjs_kes_total', 'payslip_ids.net_wage')
    def _compute_totals(self):
        for batch in self:
            batch.payslip_count = len(batch.payslip_ids)
            batch.total_gross = sum(p.gross_wage for p in batch.payslip_ids)
            batch.total_pph21 = sum(p.pph21_amount for p in batch.payslip_ids)
            batch.total_bpjs_tk = sum(p.bpjs_tk_total for p in batch.payslip_ids)
            batch.total_bpjs_kes = sum(p.bpjs_kes_total for p in batch.payslip_ids)
            batch.total_net = sum(p.net_wage for p in batch.payslip_ids)

    def action_generate_payslips(self):
        self.ensure_one()
        Employee = self.env['hr.employee'].sudo()
        Payroll = self.env['airiv.payroll'].sudo()
        
        employees = Employee.search([('company_id', '=', self.company_id.id), ('active', '=', True)])
        
        for emp in employees:
            existing = Payroll.search([('batch_id', '=', self.id), ('employee_id', '=', emp.id)], limit=1)
            if not existing:
                wage = getattr(emp, 'wage', 5000000.0) or 5000000.0
                Payroll.create({
                    'name': f"Slip Gaji - {emp.name} - {self.name}",
                    'employee_id': emp.id,
                    'batch_id': self.id,
                    'company_id': self.company_id.id,
                    'basic_salary': wage,
                    'date_from': self.date_start,
                    'date_to': self.date_end,
                })
        self.write({'state': 'computed'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_mark_paid(self):
        self.payslip_ids.write({'state': 'paid'})
        self.write({'state': 'paid'})

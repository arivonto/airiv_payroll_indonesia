# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HrOvertimeIndonesia(models.Model):
    _name = 'hr.overtime.indonesia'
    _description = 'Kalkulasi Lembur Sesuai Kepmenakertrans 102/2004 & UU Cipta Kerja'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string="Referensi Lembur", required=True, default="Lembur")
    employee_id = fields.Many2one('hr.employee', string="Karyawan", required=True, tracking=True)
    date = fields.Date(string="Tanggal Lembur", required=True, default=fields.Date.today, tracking=True)
    
    company_id = fields.Many2one('res.company', string="Perusahaan", default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one('res.currency', string="Mata Uang", related='company_id.currency_id', readonly=True)
    
    hours = fields.Float(string="Jumlah Jam Lembur", required=True, default=1.0, tracking=True)
    is_holiday = fields.Boolean(string="Hari Libur / Weekend", default=False, tracking=True)
    
    depnaker_hourly_rate = fields.Monetary(string="Upah Per Jam (Depnaker)", default=50000.0, tracking=True)
    hourly_rate = fields.Monetary(string="Tarif Per Jam (Alias)", related="depnaker_hourly_rate", store=True, readonly=False)
    
    total_overtime_pay = fields.Monetary(string="Total Uang Lembur", compute="_compute_overtime_pay", store=True, tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Disetujui HR'),
        ('paid', 'Dibayar di Gaji'),
    ], string="Status", default='draft', required=True, tracking=True)

    @api.depends('hours', 'is_holiday', 'depnaker_hourly_rate', 'hourly_rate')
    def _compute_overtime_pay(self):
        for rec in self:
            rate = rec.depnaker_hourly_rate or rec.hourly_rate or 0.0
            total = 0.0
            h = rec.hours
            if not rec.is_holiday:
                if h <= 1.0:
                    total = h * rate * 1.5
                else:
                    total = (1.0 * rate * 1.5) + ((h - 1.0) * rate * 2.0)
            else:
                if h <= 7.0:
                    total = h * rate * 2.0
                elif h <= 8.0:
                    total = (7.0 * rate * 2.0) + ((h - 7.0) * rate * 3.0)
                else:
                    total = (7.0 * rate * 2.0) + (1.0 * rate * 3.0) + ((h - 8.0) * rate * 4.0)
            rec.total_overtime_pay = total

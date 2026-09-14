# AIRIV Payroll Indonesia - PPh 21 TER & BPJS Calculation Engine

Kalkulasi Otomatis PPh 21 Tarif Efektif Rata-rata (TER PP 58/2023) & BPJS Ketenagakerjaan/Kesehatan

## Odoo Apps Store

This repository contains the Odoo 18 module package for `airiv_payroll_indonesia`.

Required store assets are maintained in:

```text
airiv_payroll_indonesia/static/description/
  icon.png
  banner.png
  index.html
```

## Technical

- Odoo version: `18.0.1.0.0`
- License: `LGPL-3`
- Author: `AIRIV`
- Website: `https://airiv.id`

## Quality Gate

GitHub Actions runs the AIRIV Odoo Apps Store CI audit on branch `18.0`.

## Core Capabilities & Architecture

- Indonesian PPh 21 TER calculation context and gross-up support.
- BPJS employment and health contribution review.
- Gross-to-net payslip visibility with exceptions and approval status.

The module connects employees, contracts, salary structures, attendance, and leave to an AIRIV payroll calculation and review layer.

## Feature & Workflow Automation

1. Configure PPh 21 TER, BPJS, salary structures, and company policy.
2. Select payroll period, employees, contracts, attendance, and salary inputs.
3. Calculate gross, deductions, tax, contributions, and net pay.
4. Review exceptions, approve payslips, and retain payroll records.

## Installation Guidance

Clone branch `18.0` into the Odoo addons path, restart Odoo, update the Apps list, and install the module. Configure payroll rules and access groups before processing a period.

## Configuration Checklist

- Verify employee, contract, salary, attendance, and leave inputs.
- Confirm PPh 21 TER categories and payroll period rules.
- Review BPJS employment and health parameters.
- Inspect exceptions before approving payslips.

## Repository Layout

```text
airiv_payroll_indonesia/
  models/                 Payroll and tax models
  views/                  Payroll operations and menus
  security/               Access rules and groups
  static/description/     Apps Store assets
  __manifest__.py         Odoo metadata
```

## Contact Info

- Author: AIRIV
- Website: https://airiv.id
- GitHub: https://github.com/arivonto
- Repository: https://github.com/arivonto/airiv_payroll_indonesia
- Odoo series: `18.0`

# Indonesia Payroll & PPh 21 TER Compliance Engine (PP 58/2023, BPJS TK & Kes, e-Bupot)

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Odoo: 18.0 Community](https://img.shields.io/badge/Odoo-18.0%20Community-purple.svg)](https://www.odoo.com)
[![Price: Free ($0.00)](https://img.shields.io/badge/Price-%240.00%20(Free)-green.svg)](https://airiv.id)
[![Compliance: PP 58/2023](https://img.shields.io/badge/Tax-PP%2058%2F2023%20%26%20PMK%20168%2F2023-purple.svg)](https://airiv.id)

A comprehensive, standalone Indonesian Payroll and Personal Income Tax (**PPh 21 / PPh 26**) calculation engine built specifically for **Odoo 18.0 Community Edition**. Operates without Enterprise `hr_payroll` dependencies by providing native Community salary computation models (`airiv.payslip`, `airiv.payslip.batch`), statutory BPJS deductions, and e-Bupot 21/26 batch export.

---

## Detailed Statutory Capabilities

### 1. PPh 21 TER Engine (PP 58/2023 & PMK 168/2023)
* **TER Rate Matrix (Jan–Nov)**: Implements monthly Effective Average Tax Rates (*Tarif Efektif Rata-Rata*) across Categories A, B, and C automatically mapped to employee PTKP status (TK/0 to K/3).
* **December True-Up Calculation**: Computes annual taxable income using progressive tax brackets (Pasal 17 UU HPP: 5%, 15%, 25%, 30%, 35%) and calculates the December adjustment.
* **Non-Employee & Freelance Withholding**: Withholding calculation for experts, consultants, and freelance workers using the 50% DPP non-cumulative method.

### 2. Statutory BPJS Compliance
* **BPJS Ketenagakerjaan**:
  * Jaminan Kecelakaan Kerja (JKK): 0.24% – 1.74% (employer-paid).
  * Jaminan Kematian (JKM): 0.30% (employer-paid).
  * Jaminan Hari Tua (JHT): 3.70% (employer) + 2.00% (employee).
  * Jaminan Pensiun (JP): 2.00% (employer) + 1.00% (employee), enforced against the statutory monthly ceiling.
* **BPJS Kesehatan**:
  * 4.00% (employer) + 1.00% (employee), enforced against the statutory ceiling of Rp 12.000.000/month.

### 3. DJP e-Bupot 21/26 & 16-Digit NIK Integration
* **16-Digit Single Identity Number (NIK)**: Integrated tax identification under DJP Coretax.
* **Formulir 1721-A1 Generator**: Automated withholding tax slip generation for permanent employees.
* **e-Bupot CSV Batch Export**: Standard CSV schema export ready for direct batch upload to DJP Online.

---

## Validated Commercial Test Benchmark (Scrutinized)

The payroll calculation engine was verified under live Odoo 18 Community conditions:

1. **Employee Profile**: `Budi Santoso (Test Staff)` (NIK: `3171012345670001`, Status: `K/0` $\rightarrow$ TER Category A).
2. **Gross Earnings**: Basic Wage Rp 12.000.000 + Fixed Allowance Rp 3.000.000 = **Gross Rp 15.000.000,00**.
3. **Statutory Deductions Computed**:
   * BPJS TK JHT (2.0%): **Rp 300.000,00**
   * BPJS TK JP (1.0% Capped @ Rp 10.042.300): **Rp 100.423,00**
   * BPJS Kesehatan (1.0% Capped @ Rp 12.000.000): **Rp 120.000,00**
   * PPh 21 TER Category A (6.0%): **Rp 900.000,00**
4. **Net Take-Home-Pay (THP)**: **Rp 13.579.577,00** verified with zero computation discrepancies.

---

## Installation & Odoo Configuration Guide

1. **Deploy Module**:
   Place `airiv_payroll_indonesia` inside your Odoo `custom_addons` directory.

2. **Activate Module**:
   * Navigate to **Apps > Update Apps List**.
   * Search for `Indonesia Payroll & PPh 21 TER Engine` and click **Activate**.

3. **Configure Employee PTKP & Tax Data**:
   * Open **Employees** and select an employee record.
   * Under the **Indonesian Payroll & Tax** tab, configure the 16-digit NIK, PTKP status (`TK/0` to `K/3`), and BPJS membership numbers.

4. **Generate Monthly Payslips**:
   * Navigate to **Payroll Center > Payslips** or **Payslip Batches**.
   * Create a batch for the monthly period and click **Compute Sheet**; the engine automatically applies the matching TER percentage and statutory BPJS ceilings.

---

## Module Specifications

| Specification | Details |
| :--- | :--- |
| **Framework Version** | Odoo 18.0 Community Edition (OWL client & App Drawer compliant) |
| **License** | GNU Lesser General Public License v3.0 (LGPL-3) |
| **Price** | Free ($0.00) |
| **Dependencies** | `base`, `hr`, `mail` |
| **Server Overhead** | Zero (Native ORM calculations, direct CSV streams) |
| **Tax Standard** | PP 58/2023, PMK 168/2023, DJP e-Bupot 21/26 |

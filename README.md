# Indonesia Statutory Payroll & PPh 21 TER Engine (PP 58/2023 & PMK 168/2023)

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Odoo: 18.0 Community](https://img.shields.io/badge/Odoo-18.0%20Community-purple.svg)](https://www.odoo.com)
[![Price: Free ($0.00)](https://img.shields.io/badge/Price-%240.00%20(Free)-green.svg)](https://airiv.id)
[![Tax Compliance: DJP Coretax](https://img.shields.io/badge/DJP-Coretax%20%7C%20e--Bupot%2021-red.svg)](https://pajak.go.id)

A complete, zero-overhead Indonesian statutory payroll and tax calculation engine developed natively for **Odoo 18.0 Community Edition**. Built to empower Indonesian UMKM, SMBs, and local enterprises with automated PPh 21 TER calculations, complete BPJS contributions, PTKP auto-mapping, and DJP Coretax / e-Bupot 21/26 compliant exports.

---

## Detailed Features & Statutory Capabilities

### 1. PPh 21 TER Engine (PP 58/2023 & PMK 168/2023)
* **Monthly Effective Rate (TER Bulanan)**: Automated rate lookup across Category A, Category B, and Category C based on monthly gross taxable income.
* **Annualized December Reconciliation (Pasal 17 UU PPh / HPP)**: Automatic true-up calculation in the final tax period (December or employee resignation month) using standard progressive tax brackets (5% up to 35%) minus previously withheld monthly TER deductions.
* **Non-Permanent Workers & Freelancers (Bukan Pegawai)**: Native support for daily TER or 50% non-cumulative gross income calculations.
* **Tax Schemes**: Flexible salary rules for **Gross**, **Gross-Up** (Tunjangan Pajak PPh 21), and **Nett** tax policies.

### 2. Full BPJS Ketenagakerjaan Coverage
* **Jaminan Kecelakaan Kerja (JKK)**: Configurable company-borne risk tiers (0.24%, 0.54%, 0.89%, 1.27%, and 1.74%).
* **Jaminan Kematian (JKM)**: Fixed 0.30% company contribution included in gross taxable income for PPh 21.
* **Jaminan Hari Tua (JHT)**: 3.70% company contribution + 2.00% employee salary deduction (tax-deductible).
* **Jaminan Pensiun (JP)**: 2.00% company contribution + 1.00% employee salary deduction with automated statutory wage ceiling capping.

### 3. BPJS Kesehatan Integration
* **Standard 5% Split**: 4.00% employer contribution + 1.00% employee deduction.
* **Statutory Upper Limit Validation**: Automatic capping based on the national maximum wage base (Rp 12.000.000).
* **Tax Base Inclusion**: Employer health premium automatically integrated into the employee's gross tax base per tax law.

### 4. DJP Coretax & e-Bupot 21/26 Export
* **Pre-formatted Tax Export**: Instant CSV / Excel generation formatted for direct batch upload into DJP Coretax and e-Bupot 21/26 portals.
* **16-Digit NPWP / NIK Alignment**: Automated verification of 16-digit unified NIK/NPWP format.
* **Tax Exemption Tracking**: Automated handling of non-taxable allowances, religious holiday allowances (THR), and bonuses.

### 5. Indonesian Payslip (Slip Gaji) & Bank Transfer
* **Bilingual Standard Payslips**: Clean PDF payslips generated with Indonesian Rupiah (Rp) formatting and WIB timestamps.
* **Direct Bank Batch Transfer**: Generates payment distribution files for major Indonesian banks (BCA KlikBCA Bisnis, Mandiri MCM/MIB, BRI, BNI).

---

## Statutory Configuration & Tax Setup Guide

### A. PTKP & TER Category Matrix

| PTKP Status | Marital & Dependent Status | TER Category (PP 58/2023) | Annual PTKP (IDR) |
| :--- | :--- | :---: | :--- |
| **TK/0** | Single, 0 Dependents | **Category A** | Rp 54.000.000 |
| **TK/1** | Single, 1 Dependent | **Category A** | Rp 58.500.000 |
| **K/0** | Married, 0 Dependents | **Category A** | Rp 58.500.000 |
| **TK/2** | Single, 2 Dependents | **Category B** | Rp 63.000.000 |
| **TK/3** | Single, 3 Dependents | **Category B** | Rp 67.500.000 |
| **K/1** | Married, 1 Dependent | **Category B** | Rp 63.000.000 |
| **K/2** | Married, 2 Dependents | **Category B** | Rp 67.500.000 |
| **K/3** | Married, 3 Dependents | **Category C** | Rp 72.000.000 |

---

### B. BPJS Contribution Reference Matrix

| Program | Employer Contribution | Employee Deduction | Max Wage Base (Cap) | Tax Treatment (PPh 21) |
| :--- | :---: | :---: | :--- | :--- |
| **BPJS Kesehatan** | 4.00% | 1.00% | Rp 12.000.000 | Employer part adds to Gross Tax Base |
| **BPJS TK - JKK** | 0.24% - 1.74% | - | No Cap | Employer part adds to Gross Tax Base |
| **BPJS TK - JKM** | 0.30% | - | No Cap | Employer part adds to Gross Tax Base |
| **BPJS TK - JHT** | 3.70% | 2.00% | No Cap | Employee part reduces Gross Tax Base |
| **BPJS TK - JP** | 2.00% | 1.00% | Statutory Cap | Employee part reduces Gross Tax Base |

---

## Installation & Odoo Configuration

1. **Deploy Module Files**:
   Ensure `airiv_payroll_indonesia` is placed within your Odoo `custom_addons` directory.

2. **Install in Odoo**:
   * Activate Developer Mode (`?debug=1`).
   * Navigate to **Apps > Update Apps List**.
   * Search for `Indonesian Payroll & PPh 21 TER Engine` and click **Activate**.

3. **Employee Setup**:
   * Open **Employees** and edit employee profiles.
   * Under the **Indonesian Payroll & Tax** tab, specify:
     * **NIK / NPWP 16-Digit**
     * **PTKP Status** (e.g., `TK/0`, `K/1`, `K/2`)
     * **BPJS TK & BPJS Kesehatan Numbers**
     * **JKK Risk Level** (Group I to Group V)

4. **Generating Monthly Payslips**:
   * Open the **9-dot App Switcher** and select **Indonesian Payroll**.
   * Go to **Payslips > Create** (or run **Payslip Batches** for company-wide processing).
   * Compute sheet to calculate gross earnings, TER PPh 21 deductions, BPJS contributions, and take-home pay.

---

## Module Specifications

| Specification | Details |
| :--- | :--- |
| **Framework Version** | Odoo 18.0 Community Edition (100% LGPL-3 compatible) |
| **License** | GNU Lesser General Public License v3.0 (LGPL-3) |
| **Price** | Free ($0.00) |
| **Dependencies** | `hr`, `base` |
| **Statutory Standards** | PP 58/2023, PMK 168/2023, UU 7/2021 (HPP), BPJS Regulations |
| **Tax Reporting** | DJP Coretax, e-Bupot 21/26 CSV Export |
| **Currency & Locale** | IDR (Rp), WIB (UTC+7) |

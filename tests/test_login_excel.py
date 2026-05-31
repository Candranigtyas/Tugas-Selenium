# tests/test_login_excel.py
import pytest
import os
import openpyxl
from pages.login_page import LoginPage

# Fungsi helper untuk membaca data dari file Excel (.xlsx)
def load_excel(filename):
    filepath = os.path.join('data', filename)
    wb = openpyxl.load_workbook(filepath)
    sheet = wb.active
    
    # Ambil nama kolom dari baris pertama (header)
    headers = [cell.value for cell in sheet[1]]
    
    data = []
    # Ambil data dari baris kedua sampai akhir
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if any(row):  # Pastikan baris tidak kosong
            data.append(dict(zip(headers, row)))
    return data

class TestLoginExcel:

    # Membaca data baris demi baris dari file Excel
    @pytest.mark.parametrize('row', load_excel('login_data.xlsx'))
    def test_login_from_excel(self, driver, row):
        page = LoginPage(driver)
        
        # Atasi jika ada nilai None (kolom kosong di Excel) diubah jadi string kosong
        username = row['username'] if row['username'] is not None else ""
        password = row['password'] if row['password'] is not None else ""
        
        # Robot menjalankan aksi login menggunakan data dari Excel
        page.login(username, password)
        
        # Pengecekan status sukses/gagal sesuai kolom 'expected' di Excel
        if row['expected'] == 'PASS':
            assert page.is_login_successful(), f"Harusnya login sukses untuk: {row['description']}"
        else:
            assert page.is_login_failed(), f"Harusnya login gagal untuk: {row['description']}"
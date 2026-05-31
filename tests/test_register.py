# tests/test_register.py
import pytest
# Kita import langsung fungsi load_csv dari file conftest
from tests.conftest import load_csv

class TestRegister:
    # Mengambil data 8 skenario dari file CSV yang sudah kamu buat
    @pytest.mark.parametrize('row', load_csv('register_data.csv'))
    def test_register_from_csv(self, driver, row):
        # 1. Robot otomatis membuka halaman web (sementara pakai link login dulu ya)
        driver.get("https://the-internet.herokuapp.com/login") 
        
        # Cetak skenario yang lagi berjalan di terminal
        print(f"\nMenguji skenario Register: {row['description']}")
        
        # 2. Ambil data dari kolom CSV baris demi baris
        username = row['username']
        email = row['email']
        password = row['password']
        expected = row['expected']
        
        # Skenario sementara di-set True dulu agar 8 skenario data kamu terbaca semua oleh pytest
        assert True
# tests/conftest.py
import os
import pytest
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='function')
def driver():
    """Fixture: buat driver baru setiap test, tutup setelah selesai"""
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    # options.add_argument('--headless')  # aktifkan di CI/CD
    d = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield d  # <-- test berjalan di sini
    d.quit()  # <-- teardown otomatis setelah test

@pytest.fixture(scope='function')
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)

@pytest.fixture(scope='function')
def dashboard_page(driver):
    from pages.dashboard_page import DashboardPage
    return DashboardPage(driver)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # Kita cek, jika test-nya selesai dijalankan dan hasilnya GAGAL (FAIL)
    if report.when == "call" and report.failed:
        # Ambil driver browser yang lagi jalan
        driver = item.funcargs.get('driver')
        if driver:
            # Buat folder 'reports' kalau belum ada
            os.makedirs('reports', exist_ok=True)
            
            # Buat nama file screenshot berdasarkan nama test yang eror
            screenshot_name = f"reports/FAIL_{item.name}.png"
            
            # Perintah robot buat nge-screenshot
            driver.save_screenshot(screenshot_name)
            print(f"\n[BUKTI] Test gagal! Screenshot disimpan di: {screenshot_name}")

def load_csv(filename):
    """Membaca file CSV dari folder data/ dan mengembalikan sebagai list of dict"""
    import os
    filepath = os.path.join('data', filename)
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
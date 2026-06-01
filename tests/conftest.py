import os
import pytest
import csv
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='function')
def driver():
    """Fixture: buat driver baru setiap test, tutup setelah selesai"""
    options = Options()
    options.add_argument('--start-maximized')
    
    # KUNCI UTAMA: Tambahkan opsi ini agar jalan di GitHub Actions
    options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    d = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield d 
    d.quit()

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
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            os.makedirs('reports', exist_ok=True)
            screenshot_name = f"reports/FAIL_{item.name}.png"
            driver.save_screenshot(screenshot_name)
            print(f"\n[BUKTI] Test gagal! Screenshot disimpan di: {screenshot_name}")

def load_csv(filename):
    filepath = os.path.join('data', filename)
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
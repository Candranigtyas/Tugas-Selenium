from selenium import webdriver
import time

# Membuka browser Chrome otomatis
driver = webdriver.Chrome()

# Masuk ke website Google
driver.get("https://www.google.com")

# Kasih jeda 5 detik biar kelihatan di video
time.sleep(5)

# Tutup browser
driver.quit()
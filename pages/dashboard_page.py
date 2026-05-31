# pages/dashboard_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    # Locator tombol logout (biasanya ada di page setelah login)
    LOGOUT_BTN = (By.CSS_SELECTOR, 'a.button.secondary.radius')

    def logout(self):
        """Method untuk melakukan klik pada tombol logout"""
        self.click(self.LOGOUT_BTN)

    def is_on_dashboard(self):
        """Method untuk mengecek apakah user benar-benar sedang di dashboard"""
        # Kita cek apakah tombol logout-nya kelihatan atau URL-nya mengandung '/secure'
        return '/secure' in self.get_current_url()
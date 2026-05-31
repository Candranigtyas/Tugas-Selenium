# tests/test_login.py
import pytest

class TestLogin:

    def test_login_valid(self, login_page):
        login_page.login('tomsmith', 'SuperSecretPassword!')
        assert login_page.is_login_successful(), 'Login valid harus berhasil'

    def test_login_invalid_password(self, login_page):
        login_page.login('tomsmith', 'wrongpassword')
        assert login_page.is_login_failed(), 'Login dengan password salah harus gagal'

    def test_login_empty_username(self, login_page):
        login_page.login('', 'SuperSecretPassword!')
        assert login_page.is_login_failed(), 'Login tanpa username harus gagal'

    def test_flash_message_content(self, login_page):
        login_page.login('wronguser', 'wrongpass')
        msg = login_page.get_flash_message()
        assert 'invalid' in msg.lower(), f'Pesan error tidak sesuai: {msg}'

    def test_login_and_logout(self, login_page, dashboard_page):
        # 1. Alur Login dengan akun yang valid
        login_page.login('tomsmith', 'SuperSecretPassword!')
        
        # 2. Memastikan masuk ke halaman secure/dashboard
        assert dashboard_page.is_on_dashboard(), 'Harusnya user berada di halaman dashboard setelah login'
        
        # 3. Melakukan aksi klik tombol Logout
        dashboard_page.logout()
        
        # 4. Memastikan user berhasil keluar dan kembali ke halaman login
        assert 'login' in login_page.get_current_url(), 'User harusnya dialihkan kembali ke halaman login'
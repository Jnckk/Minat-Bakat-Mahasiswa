import tkinter as tk
from typing import Any
from ..config.database import db_config
from ..views import (
    LoginWindow,
    MahasiswaDashboard,
    AdminDashboard,
    KemahasiswaanDashboard,
)
from ..models import Mahasiswa, Admin, Kemahasiswaan
from ..utils import DialogUtils


class ApplicationController:
    __slots__ = ("current_window", "current_user", "user_role")

    def __init__(self):
        self.current_window = None
        self.current_user = None
        self.user_role = None
        self._init_database()

    def _init_database(self) -> None:
        try:
            db_config.init_database()
        except Exception as e:
            DialogUtils.show_error(
                "Database Error",
                "Gagal menginisialisasi database. Aplikasi akan ditutup.",
            )
            raise SystemExit(1) from e

    def start_application(self) -> None:
        self._show_login_window()

    def _show_login_window(self) -> None:
        self._close_current_window()
        login_window = LoginWindow(self._on_login_success)
        self.current_window = login_window.window
        login_window.show()

    def _close_current_window(self) -> None:
        if self.current_window:
            try:
                self.current_window.destroy()
            except tk.TclError:
                pass
            finally:
                self.current_window = None

    def _on_login_success(self, role: str, user: Any) -> None:
        self.current_user = user
        self.user_role = role
        dashboard_map = {
            "mahasiswa": self._show_mahasiswa_dashboard,
            "admin": self._show_admin_dashboard,
            "kemahasiswaan": self._show_kemahasiswaan_dashboard,
        }
        dashboard_handler = dashboard_map.get(role)
        if dashboard_handler:
            dashboard_handler(user)

    def _show_mahasiswa_dashboard(self, mahasiswa: Mahasiswa) -> None:
        self._close_current_window()
        dashboard = MahasiswaDashboard(mahasiswa, self._on_logout)
        self.current_window = dashboard.window
        dashboard.show()

    def _show_admin_dashboard(self, admin: Admin) -> None:
        self._close_current_window()
        dashboard = AdminDashboard(admin, self._on_logout)
        self.current_window = dashboard.window
        dashboard.show()

    def _show_kemahasiswaan_dashboard(self, kemahasiswaan: Kemahasiswaan) -> None:
        self._close_current_window()
        dashboard = KemahasiswaanDashboard(kemahasiswaan, self._on_logout)
        self.current_window = dashboard.window
        dashboard.show()

    def _on_logout(self) -> None:
        self.current_user = None
        self.user_role = None
        self._show_login_window()

    def shutdown(self) -> None:
        self._close_current_window()


def main() -> None:
    app = ApplicationController()
    try:
        app.start_application()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        DialogUtils.show_error("Application Error", str(e))
    finally:
        app.shutdown()


if __name__ == "__main__":
    main()

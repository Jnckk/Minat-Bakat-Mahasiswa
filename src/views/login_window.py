import tkinter as tk
from typing import Callable, Any
from ..utils import DarkBlueTheme, WidgetUtils, DialogUtils
from ..models import Mahasiswa, Admin, Kemahasiswaan


class LoginWindow:
    def __init__(self, on_login_success: Callable[[str, Any], None]):
        self.on_login_success = on_login_success
        self.current_user = None
        self.window = tk.Tk()
        self.window.title("Sistem Manajemen Minat Olahraga - Login")
        self.window.configure(bg=DarkBlueTheme.get_color("bg_primary"))
        self.window.state("zoomed")
        self.window.resizable(True, True)
        self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.window.minsize(900, 600)
        self.setup_ui()

    def setup_ui(self) -> None:
        main_container = WidgetUtils.create_styled_frame(
            self.window, bg=DarkBlueTheme.get_color("bg_primary")
        )
        main_container.pack(fill="both", expand=True)
        left_panel = WidgetUtils.create_styled_frame(
            main_container, bg=DarkBlueTheme.get_color("primary")
        )
        left_panel.pack(side="left", fill="y")
        left_panel.configure(width=500)
        gradient_frame1 = WidgetUtils.create_styled_frame(
            left_panel, bg=DarkBlueTheme.get_color("primary_dark")
        )
        gradient_frame1.pack(fill="both", expand=True)
        gradient_frame2 = WidgetUtils.create_styled_frame(
            gradient_frame1, bg=DarkBlueTheme.get_color("primary")
        )
        gradient_frame2.pack(fill="both", expand=True, padx=2, pady=2)
        logo_frame = WidgetUtils.create_styled_frame(
            gradient_frame2, bg=DarkBlueTheme.get_color("primary")
        )
        logo_frame.pack(fill="both", expand=True, padx=30, pady=40)
        WidgetUtils.create_styled_label(
            logo_frame,
            "⚽",
            font=("Segoe UI Emoji", 64),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        ).pack(pady=(40, 30))
        WidgetUtils.create_styled_label(
            logo_frame,
            "SISTEM MANAJEMEN\nOLAHRAGA",
            font=("Segoe UI", 18, "bold"),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_primary"),
            justify="center",
        ).pack(pady=(0, 20))
        WidgetUtils.create_styled_label(
            logo_frame,
            "Kelola Minat Olahraga\nMahasiswa dengan Mudah\n\n✓ Pendaftaran Online\n✓ Manajemen Data\n✓ Laporan Terintegrasi",
            font=("Segoe UI", 11),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_secondary"),
            justify="center",
        ).pack(pady=20)
        WidgetUtils.create_styled_label(
            logo_frame,
            "Version 2.0",
            font=("Segoe UI", 9),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_muted"),
            justify="center",
        ).pack(side="bottom", pady=(0, 20))
        right_panel = WidgetUtils.create_styled_frame(
            main_container, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        right_panel.pack(side="right", fill="both", expand=True)
        login_container = WidgetUtils.create_styled_frame(
            right_panel, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        login_container.pack(fill="both", expand=True, padx=40, pady=40)
        WidgetUtils.create_styled_label(
            login_container,
            "Selamat Datang! 👋",
            font=("Segoe UI", 28, "bold"),
            bg=DarkBlueTheme.get_color("bg_secondary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        ).pack(pady=(0, 10))
        WidgetUtils.create_styled_label(
            login_container,
            "Silakan masuk untuk melanjutkan ke sistem",
            font=("Segoe UI", 13),
            bg=DarkBlueTheme.get_color("bg_secondary"),
            fg=DarkBlueTheme.get_color("text_muted"),
        ).pack(pady=(0, 40))
        self.setup_role_selection(login_container)
        self.forms_frame = WidgetUtils.create_styled_frame(
            login_container, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        self.forms_frame.pack(fill="both", expand=True, pady=10)
        footer_frame = WidgetUtils.create_styled_frame(
            login_container, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        footer_frame.pack(side="bottom", fill="x", pady=(20, 0))
        WidgetUtils.create_styled_label(
            footer_frame,
            "© 2025 Sistem Manajemen Olahraga | Universitas",
            font=("Segoe UI", 9),
            bg=DarkBlueTheme.get_color("bg_secondary"),
            fg=DarkBlueTheme.get_color("text_muted"),
            justify="center",
        ).pack(pady=10)
        self.current_form = None
        self.show_mahasiswa_form()

    def setup_role_selection(self, parent) -> None:
        role_frame = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        role_frame.pack(fill="x", pady=(0, 35))
        WidgetUtils.create_styled_label(
            role_frame,
            "Pilih Jenis Pengguna",
            font=("Segoe UI", 14, "bold"),
            bg=DarkBlueTheme.get_color("bg_secondary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        ).pack(pady=(0, 15))
        tabs_container = WidgetUtils.create_styled_frame(
            role_frame, bg=DarkBlueTheme.get_color("bg_tertiary"), relief="flat", bd=0
        )
        tabs_container.pack(fill="x")
        tabs_container.configure(height=55)
        self.role_buttons = {}
        roles = [
            ("mahasiswa", "🎓 Mahasiswa", "button_primary"),
            ("admin", "👨‍💼 Admin", "button_secondary"),
            ("kemahasiswaan", "🏢 Kemahasiswaan", "button_secondary"),
        ]
        for role, label, style in roles:
            self.role_buttons[role] = WidgetUtils.create_styled_button(
                tabs_container,
                label,
                command=lambda r=role: self.switch_role(r),
                style_name=style,
                font=("Segoe UI", 12, "bold"),
            )
            self.role_buttons[role].pack(
                side="left", fill="both", expand=True, padx=2, pady=2
            )
        self.active_role = "mahasiswa"

    def switch_role(self, role: str) -> None:
        self.active_role = role
        for role_name, button in self.role_buttons.items():
            if role_name == role:
                button.configure(
                    bg=DarkBlueTheme.get_color("btn_primary"),
                    fg=DarkBlueTheme.get_color("text_primary"),
                    relief="solid",
                    bd=2,
                )
            else:
                button.configure(
                    bg=DarkBlueTheme.get_color("btn_secondary"),
                    fg=DarkBlueTheme.get_color("text_secondary"),
                    relief="flat",
                    bd=0,
                )
        if role == "mahasiswa":
            self.show_mahasiswa_form()
        elif role == "admin":
            self.show_admin_form()
        elif role == "kemahasiswaan":
            self.show_kemahasiswaan_form()

    def clear_forms(self) -> None:
        for widget in self.forms_frame.winfo_children():
            widget.destroy()

    def show_mahasiswa_form(self) -> None:
        self.clear_forms()
        self.current_form = "mahasiswa"
        form_card = WidgetUtils.create_styled_frame(
            self.forms_frame, bg=DarkBlueTheme.get_color("bg_card")
        )
        form_card.pack(fill="both", expand=True, padx=5, pady=5)
        form_inner = WidgetUtils.create_styled_frame(
            form_card, bg=DarkBlueTheme.get_color("bg_card")
        )
        form_inner.pack(fill="both", expand=True, padx=25, pady=20)
        WidgetUtils.create_styled_label(
            form_inner,
            "🎓 Login Mahasiswa",
            font=("Segoe UI", 16, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        ).pack(pady=(0, 25))
        WidgetUtils.create_styled_label(
            form_inner,
            "📝 Nomor Induk Mahasiswa (NIM)",
            font=("Segoe UI", 11, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        ).pack(anchor="w", pady=(0, 8))
        self.nim_entry = WidgetUtils.create_styled_entry(
            form_inner,
            font=("Segoe UI", 12),
            bg=DarkBlueTheme.get_color("input_bg"),
            fg=DarkBlueTheme.get_color("text_primary"),
            insertbackground=DarkBlueTheme.get_color("accent_info"),
        )
        self.nim_entry.pack(fill="x", pady=(0, 20), ipady=8)
        self.add_placeholder(self.nim_entry, "Masukkan NIM Anda")
        WidgetUtils.create_styled_label(
            form_inner,
            "🔐 Password (PIC)",
            font=("Segoe UI", 11, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        ).pack(anchor="w", pady=(0, 8))
        self.pic_entry = WidgetUtils.create_styled_entry(
            form_inner,
            show="*",
            font=("Segoe UI", 12),
            bg=DarkBlueTheme.get_color("input_bg"),
            fg=DarkBlueTheme.get_color("text_primary"),
            insertbackground=DarkBlueTheme.get_color("accent_info"),
        )
        self.pic_entry.pack(fill="x", pady=(0, 25), ipady=8)
        self.bind_enter_key(self.nim_entry, self.login_mahasiswa)
        self.bind_enter_key(self.pic_entry, self.login_mahasiswa)
        buttons_frame = WidgetUtils.create_styled_frame(
            form_inner, bg=DarkBlueTheme.get_color("bg_card")
        )
        buttons_frame.pack(fill="x", pady=(0, 15))
        WidgetUtils.create_styled_button(
            buttons_frame,
            "🚀 MASUK SEKARANG",
            command=self.login_mahasiswa,
            style_name="button_success",
            font=("Segoe UI", 12, "bold"),
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        WidgetUtils.create_styled_button(
            buttons_frame,
            "📝 DAFTAR",
            command=self.show_register_form,
            style_name="button_primary",
            font=("Segoe UI", 12, "bold"),
        ).pack(side="right", fill="x", expand=True, padx=(5, 0))
        WidgetUtils.create_styled_frame(
            form_inner, bg=DarkBlueTheme.get_color("border_primary"), height=1
        ).pack(fill="x", pady=15)
        info_frame = WidgetUtils.create_styled_frame(
            form_inner, bg=DarkBlueTheme.get_color("bg_card")
        )
        info_frame.pack(fill="x", pady=5)
        WidgetUtils.create_styled_label(
            info_frame,
            "ℹ️ Belum punya akun? Klik tombol DAFTAR di atas",
            font=("Segoe UI", 10),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_muted"),
            justify="center",
        ).pack(pady=5)
        self.nim_entry.focus()

    def show_admin_form(self) -> None:
        self.clear_forms()
        self.current_form = "admin"
        form_card = WidgetUtils.create_styled_frame(
            self.forms_frame, bg=DarkBlueTheme.get_color("bg_card")
        )
        form_card.pack(fill="both", expand=True, padx=5, pady=5)
        form_inner = WidgetUtils.create_styled_frame(
            form_card, bg=DarkBlueTheme.get_color("bg_card")
        )
        form_inner.pack(fill="both", expand=True, padx=25, pady=20)
        WidgetUtils.create_styled_label(
            form_inner,
            "👨‍💼 Login Admin",
            font=("Segoe UI", 16, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        ).pack(pady=(0, 25))
        WidgetUtils.create_styled_label(
            form_inner,
            "👤 Username",
            font=("Segoe UI", 11, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        ).pack(anchor="w", pady=(0, 8))
        self.admin_username_entry = WidgetUtils.create_styled_entry(
            form_inner,
            font=("Segoe UI", 12),
            bg=DarkBlueTheme.get_color("input_bg"),
            fg=DarkBlueTheme.get_color("text_primary"),
            insertbackground=DarkBlueTheme.get_color("accent_info"),
        )
        self.admin_username_entry.pack(fill="x", pady=(0, 20), ipady=8)
        WidgetUtils.create_styled_label(
            form_inner,
            "🔐 Password",
            font=("Segoe UI", 11, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        ).pack(anchor="w", pady=(0, 8))
        self.admin_password_entry = WidgetUtils.create_styled_entry(
            form_inner,
            show="*",
            font=("Segoe UI", 12),
            bg=DarkBlueTheme.get_color("input_bg"),
            fg=DarkBlueTheme.get_color("text_primary"),
            insertbackground=DarkBlueTheme.get_color("accent_info"),
        )
        self.admin_password_entry.pack(fill="x", pady=(0, 25), ipady=8)
        self.bind_enter_key(self.admin_username_entry, self.login_admin)
        self.bind_enter_key(self.admin_password_entry, self.login_admin)
        WidgetUtils.create_styled_button(
            form_inner,
            "🚀 MASUK SEBAGAI ADMIN",
            command=self.login_admin,
            style_name="button_success",
            font=("Segoe UI", 12, "bold"),
        ).pack(fill="x", pady=(0, 15))
        WidgetUtils.create_styled_frame(
            form_inner, bg=DarkBlueTheme.get_color("border_primary"), height=1
        ).pack(fill="x", pady=10)
        info_frame = WidgetUtils.create_styled_frame(
            form_inner, bg=DarkBlueTheme.get_color("bg_card")
        )
        info_frame.pack(fill="x", pady=5)
        WidgetUtils.create_styled_label(
            info_frame,
            "ℹ️ Kredensial Default: admin / admin123",
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_muted"),
            font=("Segoe UI", 10),
        ).pack()
        self.admin_username_entry.focus()

    def show_kemahasiswaan_form(self) -> None:
        self.clear_forms()
        self.current_form = "kemahasiswaan"
        form_card = WidgetUtils.create_styled_frame(
            self.forms_frame, bg=DarkBlueTheme.get_color("bg_card")
        )
        form_card.pack(fill="both", expand=True, padx=5, pady=5)
        form_inner = WidgetUtils.create_styled_frame(
            form_card, bg=DarkBlueTheme.get_color("bg_card")
        )
        form_inner.pack(fill="both", expand=True, padx=25, pady=20)
        WidgetUtils.create_styled_label(
            form_inner,
            "🏢 Login Kemahasiswaan",
            font=("Segoe UI", 16, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        ).pack(pady=(0, 25))
        WidgetUtils.create_styled_label(
            form_inner,
            "👤 Username",
            font=("Segoe UI", 11, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        ).pack(anchor="w", pady=(0, 8))
        self.kemahasiswaan_username_entry = WidgetUtils.create_styled_entry(
            form_inner,
            font=("Segoe UI", 12),
            bg=DarkBlueTheme.get_color("input_bg"),
            fg=DarkBlueTheme.get_color("text_primary"),
            insertbackground=DarkBlueTheme.get_color("accent_info"),
        )
        self.kemahasiswaan_username_entry.pack(fill="x", pady=(0, 20), ipady=8)
        WidgetUtils.create_styled_label(
            form_inner,
            "🔐 Password",
            font=("Segoe UI", 11, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        ).pack(anchor="w", pady=(0, 8))
        self.kemahasiswaan_password_entry = WidgetUtils.create_styled_entry(
            form_inner,
            show="*",
            font=("Segoe UI", 12),
            bg=DarkBlueTheme.get_color("input_bg"),
            fg=DarkBlueTheme.get_color("text_primary"),
            insertbackground=DarkBlueTheme.get_color("accent_info"),
        )
        self.kemahasiswaan_password_entry.pack(fill="x", pady=(0, 25), ipady=8)
        self.bind_enter_key(self.kemahasiswaan_username_entry, self.login_kemahasiswaan)
        self.bind_enter_key(self.kemahasiswaan_password_entry, self.login_kemahasiswaan)
        WidgetUtils.create_styled_button(
            form_inner,
            "🚀 MASUK SEBAGAI KEMAHASISWAAN",
            command=self.login_kemahasiswaan,
            style_name="button_success",
            font=("Segoe UI", 12, "bold"),
        ).pack(fill="x", pady=(0, 15))
        WidgetUtils.create_styled_frame(
            form_inner, bg=DarkBlueTheme.get_color("border_primary"), height=1
        ).pack(fill="x", pady=10)
        info_frame = WidgetUtils.create_styled_frame(
            form_inner, bg=DarkBlueTheme.get_color("bg_card")
        )
        info_frame.pack(fill="x", pady=5)
        WidgetUtils.create_styled_label(
            info_frame,
            "ℹ️ Kredensial Default: kemahasiswaan / kemahasiswaan123",
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_muted"),
            font=("Segoe UI", 10),
        ).pack()
        self.kemahasiswaan_username_entry.focus()

    def show_register_form(self) -> None:
        try:
            from .registration_window import RegistrationWindow

            self.window.withdraw()
            registration_window = RegistrationWindow(
                on_registration_success=self.on_registration_complete
            )
            registration_window.show()
        except Exception as e:
            DialogUtils.show_error("Error", f"Gagal membuka form registrasi: {str(e)}")

    def on_registration_complete(self) -> None:
        self.window.deiconify()
        self.show_mahasiswa_form()

    def login_mahasiswa(self) -> None:
        nim = self.nim_entry.get().strip()
        pic = self.pic_entry.get().strip()
        if not nim:
            DialogUtils.show_error("Error", "NIM harus diisi!")
            self.nim_entry.focus()
            return
        if not pic:
            DialogUtils.show_error("Error", "PIC harus diisi!")
            self.pic_entry.focus()
            return
        try:
            mahasiswa = Mahasiswa(nim=nim, pic=pic)
            if mahasiswa.login():
                self.current_user = mahasiswa
                self.window.destroy()
                self.on_login_success("mahasiswa", mahasiswa)
            else:
                DialogUtils.show_error("Login Gagal", "NIM atau PIC salah!")
        except Exception as e:
            DialogUtils.show_error("Error", f"Terjadi kesalahan saat login: {str(e)}")

    def login_admin(self) -> None:
        username = self.admin_username_entry.get().strip()
        password = self.admin_password_entry.get().strip()
        if not username or not password:
            DialogUtils.show_error("Error", "Username dan password harus diisi!")
            return
        admin = Admin(username=username, password=password)
        if admin.login():
            self.current_user = admin
            self.window.destroy()
            self.on_login_success("admin", admin)
        else:
            DialogUtils.show_error("Login Gagal", "Username atau password salah!")

    def login_kemahasiswaan(self) -> None:
        username = self.kemahasiswaan_username_entry.get().strip()
        password = self.kemahasiswaan_password_entry.get().strip()
        if not username or not password:
            DialogUtils.show_error("Error", "Username dan password harus diisi!")
            return
        kemahasiswaan = Kemahasiswaan(username=username, password=password)
        if kemahasiswaan.login():
            self.current_user = kemahasiswaan
            self.window.destroy()
            self.on_login_success("kemahasiswaan", kemahasiswaan)
        else:
            DialogUtils.show_error("Login Gagal", "Username atau password salah!")

    def add_placeholder(self, entry: tk.Entry, placeholder_text: str) -> None:
        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.configure(fg=DarkBlueTheme.get_color("text_primary"))

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder_text)
                entry.configure(fg=DarkBlueTheme.get_color("text_muted"))

        entry.insert(0, placeholder_text)
        entry.configure(fg=DarkBlueTheme.get_color("text_muted"))
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def bind_enter_key(
        self, entry: tk.Entry, login_function: Callable[[], None]
    ) -> None:
        entry.bind("<Return>", lambda event: login_function())

    def on_window_close(self) -> None:
        self.window.quit()
        self.window.destroy()

    def show(self) -> None:
        self.window.mainloop()

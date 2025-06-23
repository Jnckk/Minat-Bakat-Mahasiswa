import tkinter as tk
from tkinter import ttk
from typing import Callable
from ..utils import DarkBlueTheme, WidgetUtils, ValidationUtils, DialogUtils
from ..models import Mahasiswa


class RegistrationWindow:
    def __init__(self, on_registration_success: Callable = None):
        self.on_registration_success = on_registration_success

        self.window = tk.Tk()
        self.window.title("Sistem Manajemen Minat Olahraga - Registrasi")
        self.window.configure(bg=DarkBlueTheme.get_color("bg_primary"))
        self.window.state("zoomed")
        self.window.resizable(True, True)
        self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.window.minsize(900, 600)

        self.setup_ui()

    def setup_ui(self):
        main_container = WidgetUtils.create_styled_frame(
            self.window, bg=DarkBlueTheme.get_color("bg_primary")
        )
        main_container.pack(fill="both", expand=True)

        left_panel = WidgetUtils.create_styled_frame(
            main_container, bg=DarkBlueTheme.get_color("primary")
        )
        left_panel.pack(side="left", fill="y", padx=0, pady=0)
        left_panel.configure(width=500)

        gradient_frame1 = WidgetUtils.create_styled_frame(
            left_panel, bg=DarkBlueTheme.get_color("primary_dark")
        )
        gradient_frame1.pack(fill="both", expand=True, padx=0, pady=0)

        gradient_frame2 = WidgetUtils.create_styled_frame(
            gradient_frame1, bg=DarkBlueTheme.get_color("primary")
        )
        gradient_frame2.pack(fill="both", expand=True, padx=2, pady=2)

        logo_frame = WidgetUtils.create_styled_frame(
            gradient_frame2, bg=DarkBlueTheme.get_color("primary")
        )
        logo_frame.pack(fill="both", expand=True, padx=30, pady=40)

        logo_label = WidgetUtils.create_styled_label(
            logo_frame,
            "⚽",
            font=("Segoe UI Emoji", 64),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        logo_label.pack(pady=(40, 30))

        app_name = WidgetUtils.create_styled_label(
            logo_frame,
            "PENDAFTARAN\nMAHASISWA BARU",
            font=("Segoe UI", 18, "bold"),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_primary"),
            justify="center",
        )
        app_name.pack(pady=(0, 20))

        subtitle = WidgetUtils.create_styled_label(
            logo_frame,
            "Bergabunglah dengan\nSistem Manajemen Olahraga\n\n✓ Registrasi Mudah\n✓ Data Aman\n✓ Akses Langsung",
            font=("Segoe UI", 11),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_secondary"),
            justify="center",
        )
        subtitle.pack(pady=20)

        version_label = WidgetUtils.create_styled_label(
            logo_frame,
            "Registration Portal v2.0",
            font=("Segoe UI", 9),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_muted"),
            justify="center",
        )
        version_label.pack(side="bottom", pady=(0, 20))

        right_panel = WidgetUtils.create_styled_frame(
            main_container, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        right_panel.pack(side="right", fill="both", expand=True, padx=0, pady=0)

        registration_container = WidgetUtils.create_styled_frame(
            right_panel, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        registration_container.pack(fill="both", expand=True, padx=40, pady=40)

        welcome_label = WidgetUtils.create_styled_label(
            registration_container,
            "Daftar Sekarang! 📝",
            font=("Segoe UI", 28, "bold"),
            bg=DarkBlueTheme.get_color("bg_secondary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        welcome_label.pack(pady=(0, 10))

        welcome_subtitle = WidgetUtils.create_styled_label(
            registration_container,
            "Lengkapi data diri untuk membuat akun baru",
            font=("Segoe UI", 13),
            bg=DarkBlueTheme.get_color("bg_secondary"),
            fg=DarkBlueTheme.get_color("text_muted"),
        )
        welcome_subtitle.pack(pady=(0, 30))

        self.setup_registration_form(registration_container)

        footer_frame = WidgetUtils.create_styled_frame(
            registration_container, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        footer_frame.pack(side="bottom", fill="x", pady=(20, 0))

        footer_text = WidgetUtils.create_styled_label(
            footer_frame,
            "© 2025 Sistem Manajemen Olahraga | Universitas",
            font=("Segoe UI", 9),
            bg=DarkBlueTheme.get_color("bg_secondary"),
            fg=DarkBlueTheme.get_color("text_muted"),
            justify="center",
        )
        footer_text.pack(pady=10)

    def setup_registration_form(self, parent):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Custom.TCombobox",
            fieldbackground=DarkBlueTheme.get_color("input_bg"),
            background=DarkBlueTheme.get_color("input_bg"),
            foreground=DarkBlueTheme.get_color("text_primary"),
            bordercolor=DarkBlueTheme.get_color("border_primary"),
            darkcolor=DarkBlueTheme.get_color("input_bg"),
            lightcolor=DarkBlueTheme.get_color("input_bg"),
            borderwidth=1,
            focuscolor=DarkBlueTheme.get_color("accent_info"),
            relief="flat",
            padding=(8, 8),
        )

        style.map(
            "Custom.TCombobox",
            fieldbackground=[
                ("readonly", DarkBlueTheme.get_color("input_bg")),
                ("focus", DarkBlueTheme.get_color("input_bg")),
            ],
            foreground=[
                ("readonly", DarkBlueTheme.get_color("text_primary")),
                ("focus", DarkBlueTheme.get_color("text_primary")),
            ],
            selectbackground=[("readonly", DarkBlueTheme.get_color("accent_info"))],
        )

        form_card = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("bg_card")
        )
        form_card.pack(fill="both", expand=True, padx=5, pady=5)

        form_inner = WidgetUtils.create_styled_frame(
            form_card, bg=DarkBlueTheme.get_color("bg_card")
        )
        form_inner.pack(fill="both", expand=True, padx=25, pady=20)

        title = WidgetUtils.create_styled_label(
            form_inner,
            "📋 Data Mahasiswa",
            font=("Segoe UI", 16, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        title.pack(pady=(0, 25))

        nim_label = WidgetUtils.create_styled_label(
            form_inner,
            "📝 Nomor Induk Mahasiswa (NIM)",
            font=("Segoe UI", 11, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        nim_label.pack(anchor="w", pady=(0, 8))

        self.nim_entry = WidgetUtils.create_styled_entry(
            form_inner,
            font=("Segoe UI", 12),
            bg=DarkBlueTheme.get_color("input_bg"),
            fg=DarkBlueTheme.get_color("text_primary"),
            insertbackground=DarkBlueTheme.get_color("accent_info"),
        )
        self.nim_entry.pack(fill="x", pady=(0, 15), ipady=8)
        self.add_placeholder(self.nim_entry, "Masukkan NIM Anda (contoh: 123456789)")

        nama_label = WidgetUtils.create_styled_label(
            form_inner,
            "👤 Nama Lengkap",
            font=("Segoe UI", 11, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        nama_label.pack(anchor="w", pady=(0, 8))

        self.nama_entry = WidgetUtils.create_styled_entry(
            form_inner,
            font=("Segoe UI", 12),
            bg=DarkBlueTheme.get_color("input_bg"),
            fg=DarkBlueTheme.get_color("text_primary"),
            insertbackground=DarkBlueTheme.get_color("accent_info"),
        )
        self.nama_entry.pack(fill="x", pady=(0, 15), ipady=8)
        self.add_placeholder(self.nama_entry, "Masukkan nama lengkap Anda")

        pic_label = WidgetUtils.create_styled_label(
            form_inner,
            "🔐 Password (PIC)",
            font=("Segoe UI", 11, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        pic_label.pack(anchor="w", pady=(0, 8))

        self.pic_entry = WidgetUtils.create_styled_entry(
            form_inner,
            show="*",
            font=("Segoe UI", 12),
            bg=DarkBlueTheme.get_color("input_bg"),
            fg=DarkBlueTheme.get_color("text_primary"),
            insertbackground=DarkBlueTheme.get_color("accent_info"),
        )
        self.pic_entry.pack(fill="x", pady=(0, 15), ipady=8)

        fakultas_label = WidgetUtils.create_styled_label(
            form_inner,
            "🏛️ Fakultas",
            font=("Segoe UI", 11, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        fakultas_label.pack(anchor="w", pady=(0, 8))
        self.fakultas_var = tk.StringVar()

        fakultas_options = [
            "Fakultas Teknik",
            "Fakultas Ekonomi dan Bisnis",
            "Fakultas Hukum",
            "Fakultas Kedokteran",
            "Fakultas Ilmu Sosial dan Politik",
            "Fakultas Ilmu Budaya",
            "Fakultas MIPA",
            "Fakultas Pertanian",
            "Fakultas Peternakan",
            "Fakultas Kehutanan",
            "Fakultas Kelautan dan Perikanan",
            "Fakultas Kesehatan Masyarakat",
            "Fakultas Farmasi",
            "Fakultas Psikologi",
        ]
        self.fakultas_combo = ttk.Combobox(
            form_inner,
            textvariable=self.fakultas_var,
            values=fakultas_options,
            state="readonly",
            font=("Segoe UI", 12),
            style="Custom.TCombobox",
        )
        self.fakultas_combo.pack(fill="x", pady=(0, 20), ipady=8)
        self.fakultas_combo.bind("<<ComboboxSelected>>", self.on_fakultas_selected)

        self.fakultas_combo.set("Pilih Fakultas...")

        self.window.option_add(
            "*TCombobox*Listbox.Background", DarkBlueTheme.get_color("input_bg")
        )
        self.window.option_add(
            "*TCombobox*Listbox.Foreground", DarkBlueTheme.get_color("text_primary")
        )
        self.window.option_add(
            "*TCombobox*Listbox.SelectBackground",
            DarkBlueTheme.get_color("accent_info"),
        )
        self.window.option_add(
            "*TCombobox*Listbox.SelectForeground",
            DarkBlueTheme.get_color("text_primary"),
        )
        self.window.option_add("*TCombobox*Listbox.Font", ("Segoe UI", 11))

        buttons_frame = WidgetUtils.create_styled_frame(
            form_inner, bg=DarkBlueTheme.get_color("bg_card")
        )
        buttons_frame.pack(fill="x", pady=(10, 15))

        register_btn = WidgetUtils.create_styled_button(
            buttons_frame,
            "🚀 DAFTAR SEKARANG",
            command=self.register,
            style_name="button_success",
            font=("Segoe UI", 12, "bold"),
        )
        register_btn.configure(pady=12)
        register_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        back_btn = WidgetUtils.create_styled_button(
            buttons_frame,
            "🔙 KEMBALI LOGIN",
            command=self.back_to_login,
            style_name="button_primary",
            font=("Segoe UI", 12, "bold"),
        )
        back_btn.configure(pady=12)
        back_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

        divider = WidgetUtils.create_styled_frame(
            form_inner, bg=DarkBlueTheme.get_color("border_primary"), height=1
        )
        divider.pack(fill="x", pady=15)

        info_frame = WidgetUtils.create_styled_frame(
            form_inner, bg=DarkBlueTheme.get_color("accent_info"), relief="solid", bd=1
        )
        info_frame.pack(fill="x", pady=5)

        info_text = WidgetUtils.create_styled_label(
            info_frame,
            "ℹ️ INFORMASI PENTING",
            font=("Segoe UI", 11, "bold"),
            bg=DarkBlueTheme.get_color("accent_info"),
            fg=DarkBlueTheme.get_color("text_primary"),
            justify="center",
        )
        info_text.pack(pady=(10, 5))

        info_details = WidgetUtils.create_styled_label(
            info_frame,
            "• NIM akan digunakan sebagai username untuk login\n"
            "• PIC akan digunakan sebagai password\n"
            "• Pastikan semua data yang dimasukkan sudah benar\n"
            "• Setelah registrasi, Anda dapat langsung login",
            font=("Segoe UI", 10),
            bg=DarkBlueTheme.get_color("accent_info"),
            fg=DarkBlueTheme.get_color("text_secondary"),
            justify="left",
        )
        info_details.pack(pady=(0, 10), padx=15)

        self.nim_entry.focus()
        self.bind_enter_key(self.nim_entry, lambda: self.nama_entry.focus())
        self.bind_enter_key(self.nama_entry, lambda: self.pic_entry.focus())
        self.bind_enter_key(self.pic_entry, lambda: self.fakultas_combo.focus())

    def validate_input(self) -> bool:
        nim = self.nim_entry.get().strip()
        nama = self.nama_entry.get().strip()
        pic = self.pic_entry.get().strip()
        fakultas = self.fakultas_var.get().strip()

        if nim == "Masukkan NIM Anda (contoh: 123456789)":
            nim = ""
        if nama == "Masukkan nama lengkap Anda":
            nama = ""

        if not nim:
            DialogUtils.show_error("Error", "NIM harus diisi!")
            self.nim_entry.focus()
            return False

        if not nama:
            DialogUtils.show_error("Error", "Nama lengkap harus diisi!")
            self.nama_entry.focus()
            return False

        if not pic:
            DialogUtils.show_error("Error", "PIC harus diisi!")
            self.pic_entry.focus()
            return False

        if not fakultas or fakultas == "Pilih Fakultas...":
            DialogUtils.show_error("Error", "Fakultas harus dipilih!")
            self.fakultas_combo.focus()
            return False

        if not ValidationUtils.validate_nim(nim):
            DialogUtils.show_error(
                "Error", "Format NIM tidak valid! NIM harus berupa angka 8-15 digit."
            )
            self.nim_entry.focus()
            return False

        if len(pic) < 3:
            DialogUtils.show_error("Error", "PIC minimal 3 karakter!")
            self.pic_entry.focus()
            return False

        return True

    def add_placeholder(self, entry, placeholder_text):
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

    def bind_enter_key(self, entry, action):
        entry.bind("<Return>", lambda event: action())

    def on_fakultas_selected(self, event):
        selected_value = self.fakultas_combo.get()
        if selected_value and selected_value != "Pilih Fakultas...":
            self.fakultas_var.set(selected_value)

    def register(self):
        if not self.validate_input():
            return

        nim = self.nim_entry.get().strip()
        nama = self.nama_entry.get().strip()
        pic = self.pic_entry.get().strip()
        fakultas = self.fakultas_var.get().strip()

        if nim == "Masukkan NIM Anda (contoh: 123456789)":
            nim = ""
        if nama == "Masukkan nama lengkap Anda":
            nama = ""

        try:
            existing_mahasiswa = Mahasiswa.get_by_nim(nim)
            if existing_mahasiswa:
                DialogUtils.show_error(
                    "Error", "NIM sudah terdaftar! Gunakan NIM yang berbeda."
                )
                self.nim_entry.focus()
                return

            mahasiswa = Mahasiswa.create(
                nim=nim, nama=nama, pic=pic, fakultas=fakultas, password=pic
            )

            if mahasiswa:
                DialogUtils.show_success(
                    "Registrasi Berhasil! ✅",
                    f"Selamat datang {nama}!\n\n"
                    f"Data registrasi Anda:\n"
                    f"• NIM: {nim}\n"
                    f"• Nama: {nama}\n"
                    f"• Fakultas: {fakultas}\n\n"
                    f"Silakan login dengan:\n"
                    f"• Username: {nim}\n"
                    f"• Password: {pic}",
                )

                if self.on_registration_success:
                    self.on_registration_success()

                self.window.destroy()
            else:
                DialogUtils.show_error(
                    "Error", "Gagal melakukan registrasi. Silakan coba lagi."
                )
        except Exception as e:
            DialogUtils.show_error("Error", f"Terjadi kesalahan: {str(e)}")

    def cancel(self):
        if DialogUtils.ask_confirmation(
            "Konfirmasi", "Batalkan registrasi dan kembali ke login?"
        ):
            self.back_to_login()

    def back_to_login(self):
        self.window.destroy()
        if self.on_registration_success:
            self.on_registration_success()

    def on_window_close(self):
        self.window.quit()
        self.window.destroy()

    def show(self):
        self.window.mainloop()

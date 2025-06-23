import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ..utils import (
    DarkBlueTheme,
    WidgetUtils,
    DialogUtils,
    DataUtils,
    ValidationUtils,
)
from ..models import Admin, Olahraga, MinatBakat, Mahasiswa


class AdminDashboard:
    def __init__(self, admin: Admin, on_logout: callable):
        self.admin = admin
        self.on_logout = on_logout
        self.window = tk.Tk()
        self.window.title(f"Dashboard Admin - {admin.nama}")
        self.window.configure(bg=DarkBlueTheme.get_color("bg_primary"))
        self.window.attributes("-fullscreen", False)
        self.window.state("zoomed")
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.window.minsize(1200, 1000)
        self.window.resizable(True, True)
        self.window.lift()
        self.window.focus_force()
        self.setup_ui()
        self.load_data()
        self.window.bind("<Configure>", self.on_window_configure)
        self.window.bind("<Map>", self.on_window_map)
        self.window.after(100, self.ensure_fullscreen)

    def on_window_configure(self, event):
        if event.widget == self.window:
            if self.window.state() != "zoomed":
                self.window.state("zoomed")

    def on_window_map(self, event):
        if event.widget == self.window:
            self.ensure_fullscreen()

    def ensure_fullscreen(self):
        try:
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            self.window.state("zoomed")
            self.window.geometry(f"{screen_width}x{max(screen_height, 1000)}+0+0")
            self.window.update_idletasks()
            self.window.lift()
            self.window.focus_force()
        except Exception:
            pass

    def setup_ui(self):
        main_container = WidgetUtils.create_styled_frame(
            self.window, bg=DarkBlueTheme.get_color("bg_primary"), relief="flat", bd=0
        )
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        self.setup_modern_header(main_container)

        content_frame = WidgetUtils.create_styled_frame(
            main_container,
            bg=DarkBlueTheme.get_color("bg_primary"),
            relief="flat",
            bd=0,
        )
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        canvas = tk.Canvas(
            content_frame,
            bg=DarkBlueTheme.get_color("bg_primary"),
            highlightthickness=0,
            relief="flat",
            bd=0,
        )
        canvas.pack(fill="both", expand=True, padx=0, pady=0)

        scrollbar = ttk.Scrollbar(
            content_frame, orient="vertical", command=canvas.yview
        )
        scrollbar.pack_forget()

        scrollable_frame = WidgetUtils.create_styled_frame(
            canvas, bg=DarkBlueTheme.get_color("bg_primary"), relief="flat", bd=0
        )
        scrollable_frame_id = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw"
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        def resize_scrollable_frame(event):
            canvas.itemconfig(scrollable_frame_id, width=event.width)

        canvas.bind("<Configure>", resize_scrollable_frame)

        def update_scrollregion(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", update_scrollregion)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        self.window.bind("<MouseWheel>", _on_mousewheel)

        content_wrapper = WidgetUtils.create_styled_frame(
            scrollable_frame,
            bg=DarkBlueTheme.get_color("bg_primary"),
            relief="flat",
            bd=0,
        )
        content_wrapper.pack(fill="both", expand=True, padx=0, pady=0)

        content_container = WidgetUtils.create_styled_frame(
            content_wrapper,
            bg=DarkBlueTheme.get_color("bg_primary"),
            relief="flat",
            bd=0,
        )
        content_container.pack(fill="both", expand=True, padx=40, pady=0)
        self.setup_dashboard_content(content_container)

    def setup_modern_header(self, parent):
        header_frame = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("primary"), relief="flat", bd=0
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_content = WidgetUtils.create_styled_frame(
            header_frame, bg=DarkBlueTheme.get_color("primary"), relief="flat", bd=0
        )
        header_content.pack(fill="x", padx=20, pady=20)
        user_info_frame = WidgetUtils.create_styled_frame(
            header_content, bg=DarkBlueTheme.get_color("primary")
        )
        user_info_frame.pack(side="left", fill="y")
        title_label = WidgetUtils.create_styled_label(
            user_info_frame,
            "🛡️ Dashboard Admin",
            font=("Segoe UI", 24, "bold"),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        title_label.pack(anchor="w")
        user_label = WidgetUtils.create_styled_label(
            user_info_frame,
            f"Selamat datang, {self.admin.nama}",
            font=("Segoe UI", 14),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_secondary"),
        )
        user_label.pack(anchor="w", pady=(5, 0))
        info_label = WidgetUtils.create_styled_label(
            user_info_frame,
            f"ID: {self.admin.admin_id}",
            font=("Segoe UI", 12),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_muted"),
        )
        info_label.pack(anchor="w", pady=(2, 0))
        actions_frame = WidgetUtils.create_styled_frame(
            header_content, bg=DarkBlueTheme.get_color("primary")
        )
        actions_frame.pack(side="right", fill="y")
        refresh_btn = WidgetUtils.create_styled_button(
            actions_frame,
            "🔄 REFRESH",
            command=self.load_data,
            style_name="button_secondary",
            font=("Segoe UI", 11, "bold"),
        )
        refresh_btn.pack(side="right", padx=(10, 0))
        logout_btn = WidgetUtils.create_styled_button(
            actions_frame,
            "🚪 LOGOUT",
            command=self.logout,
            style_name="button_danger",
            font=("Segoe UI", 11, "bold"),
        )
        logout_btn.pack(side="right", padx=(0, 10))

    def setup_dashboard_content(self, parent):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.TNotebook",
            background=DarkBlueTheme.get_color("bg_primary"),
            borderwidth=0,
            tabmargins=0,
        )
        style.configure(
            "Custom.TNotebook.Tab",
            background=DarkBlueTheme.get_color("bg_tertiary"),
            foreground=DarkBlueTheme.get_color("text_primary"),
            padding=[20, 10],
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            borderwidth=0,
            focuscolor="none",
        )
        style.map(
            "Custom.TNotebook.Tab",
            background=[
                ("selected", DarkBlueTheme.get_color("primary")),
                ("active", DarkBlueTheme.get_color("primary_light")),
            ],
            foreground=[
                ("selected", DarkBlueTheme.get_color("text_primary")),
                ("active", DarkBlueTheme.get_color("text_primary")),
            ],
            padding=[
                ("selected", [20, 10]),
                ("active", [20, 10]),
            ],
            relief=[("selected", "flat"), ("active", "flat")],
            borderwidth=[("selected", 0), ("active", 0)],
        )
        self.notebook = ttk.Notebook(parent, style="Custom.TNotebook")
        self.notebook.pack(fill="both", expand=True)
        self.setup_rekap_tab()
        self.setup_olahraga_tab()
        self.setup_mahasiswa_tab()
        self.setup_data_minat_tab()

    def setup_rekap_tab(self):
        tab_frame = WidgetUtils.create_styled_frame(
            self.notebook, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        self.notebook.add(tab_frame, text="Rekap Data")
        title_label = WidgetUtils.create_styled_label(
            tab_frame, "Rekap Data Minat Olahraga", "title_label"
        )
        title_label.pack(pady=20)
        self.setup_statistics_cards(tab_frame)
        chart_frame = WidgetUtils.create_styled_frame(
            tab_frame,
            bg=DarkBlueTheme.get_color("bg_tertiary"),
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        chart_frame.pack(fill="both", expand=True, padx=20, pady=20)
        chart_frame.configure(height=550)
        chart_frame.pack_propagate(False)
        controls_frame = WidgetUtils.create_styled_frame(
            chart_frame,
            bg=DarkBlueTheme.get_color("bg_tertiary"),
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        controls_frame.pack(fill="x", pady=(0, 10))
        chart_label = WidgetUtils.create_styled_label(
            controls_frame,
            "Visualisasi Data:",
            font=("Segoe UI", 14, "bold"),
            fg=DarkBlueTheme.get_color("text_primary"),
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        chart_label.pack(side="left")
        self.chart_type_var = tk.StringVar(value="Bar Chart")
        chart_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.chart_type_var,
            values=["Bar Chart", "Pie Chart"],
            state="readonly",
            font=DarkBlueTheme.get_font("body"),
        )
        chart_combo.pack(side="left", padx=(20, 10))
        chart_combo.bind("<<ComboboxSelected>>", self.update_chart)
        self.chart_frame = WidgetUtils.create_styled_frame(
            chart_frame,
            bg=DarkBlueTheme.get_color("bg_tertiary"),
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        self.chart_frame.pack(fill="both", expand=True)
        self.chart_frame.configure(height=750)
        self.chart_frame.pack_propagate(False)

    def setup_statistics_cards(self, parent):
        stats_frame = WidgetUtils.create_styled_frame(parent)
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.stats_cards_frame = stats_frame

    def setup_olahraga_tab(self):
        tab_frame = WidgetUtils.create_styled_frame(
            self.notebook, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        self.notebook.add(tab_frame, text="Kelola Olahraga")
        title_label = WidgetUtils.create_styled_label(
            tab_frame, "Kelola Data Olahraga", "title_label"
        )
        title_label.pack(pady=20)
        self.setup_add_sport_form(tab_frame)
        self.setup_sports_list(tab_frame)

    def setup_add_sport_form(self, parent):
        form_frame = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        form_frame.pack(fill="x", padx=20, pady=(0, 20))
        form_title = WidgetUtils.create_styled_label(
            form_frame, "Tambah Olahraga Baru", "heading_label"
        )
        form_title.pack(pady=(0, 15))
        fields_frame = WidgetUtils.create_styled_frame(form_frame)
        fields_frame.pack(fill="x")
        name_frame = WidgetUtils.create_styled_frame(fields_frame)
        name_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        name_label = WidgetUtils.create_styled_label(
            name_frame, "Nama Olahraga:", bg=DarkBlueTheme.get_color("bg_secondary")
        )
        name_label.pack(anchor="w")
        self.sport_name_entry = WidgetUtils.create_styled_entry(name_frame)
        self.sport_name_entry.pack(fill="x", pady=(5, 0))
        category_frame = WidgetUtils.create_styled_frame(fields_frame)
        category_frame.pack(side="left", padx=(0, 10))
        category_label = WidgetUtils.create_styled_label(
            category_frame, "Kategori:", bg=DarkBlueTheme.get_color("bg_secondary")
        )
        category_label.pack(anchor="w")
        self.sport_category_var = tk.StringVar(value="Individual")
        category_combo = ttk.Combobox(
            category_frame,
            textvariable=self.sport_category_var,
            values=["Individual", "Tim"],
            state="readonly",
            font=DarkBlueTheme.get_font("body"),
            width=15,
        )
        category_combo.pack(pady=(5, 0))
        desc_frame = WidgetUtils.create_styled_frame(fields_frame)
        desc_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        desc_label = WidgetUtils.create_styled_label(
            desc_frame, "Deskripsi:", bg=DarkBlueTheme.get_color("bg_secondary")
        )
        desc_label.pack(anchor="w")
        self.sport_desc_entry = WidgetUtils.create_styled_entry(desc_frame)
        self.sport_desc_entry.pack(fill="x", pady=(5, 0))
        add_btn = WidgetUtils.create_styled_button(
            fields_frame, "TAMBAH", command=self.add_sport, style_name="button_success"
        )
        add_btn.pack(side="right", pady=(20, 0))

    def setup_sports_list(self, parent):
        list_frame = WidgetUtils.create_styled_frame(
            parent, "card_frame", bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        list_title = WidgetUtils.create_styled_label(
            list_frame,
            "Daftar Olahraga",
            "heading_label",
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        list_title.pack(pady=(0, 15))
        self.sports_list_frame = WidgetUtils.create_styled_frame(
            list_frame, bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        self.sports_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.sports_grid_row = 0
        self.sports_grid_col = 0
        self.max_cols = 2
        for i in range(self.max_cols):
            self.sports_list_frame.grid_columnconfigure(i, weight=1, minsize=200)

    def setup_mahasiswa_tab(self):
        tab_frame = WidgetUtils.create_styled_frame(
            self.notebook, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        self.notebook.add(tab_frame, text="Data Mahasiswa")
        title_label = WidgetUtils.create_styled_label(
            tab_frame, "Data Mahasiswa", "title_label"
        )
        title_label.pack(pady=20)
        self.mahasiswa_list_frame = WidgetUtils.create_styled_frame(
            tab_frame, "card_frame", bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        self.mahasiswa_list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def setup_data_minat_tab(self):
        tab_frame = WidgetUtils.create_styled_frame(
            self.notebook, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        self.notebook.add(tab_frame, text="Data Minat Bakat")
        title_label = WidgetUtils.create_styled_label(
            tab_frame, "Kelola Data Minat Bakat", "title_label"
        )
        title_label.pack(pady=20)
        self.setup_minat_input_form(tab_frame)
        self.setup_minat_data_list(tab_frame)

    def setup_minat_input_form(self, parent):
        form_frame = WidgetUtils.create_styled_frame(
            parent, "card_frame", bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        form_frame.pack(fill="x", padx=20, pady=(0, 20))
        form_title = WidgetUtils.create_styled_label(
            form_frame,
            "Input Data Minat Bakat",
            "heading_label",
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        form_title.pack(pady=(0, 15))
        fields_frame = WidgetUtils.create_styled_frame(
            form_frame, bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        fields_frame.pack(fill="x")
        nim_frame = WidgetUtils.create_styled_frame(
            fields_frame, bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        nim_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        nim_label = WidgetUtils.create_styled_label(
            nim_frame, "NIM Mahasiswa:", bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        nim_label.pack(anchor="w")
        self.minat_nim_var = tk.StringVar()
        self.minat_nim_combo = ttk.Combobox(
            nim_frame,
            textvariable=self.minat_nim_var,
            font=DarkBlueTheme.get_font("body"),
        )
        self.minat_nim_combo.pack(fill="x", pady=(5, 0))
        olahraga_frame = WidgetUtils.create_styled_frame(
            fields_frame, bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        olahraga_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        olahraga_label = WidgetUtils.create_styled_label(
            olahraga_frame, "Olahraga:", bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        olahraga_label.pack(anchor="w")
        self.minat_olahraga_var = tk.StringVar()
        self.minat_olahraga_combo = ttk.Combobox(
            olahraga_frame,
            textvariable=self.minat_olahraga_var,
            state="readonly",
            font=DarkBlueTheme.get_font("body"),
        )
        self.minat_olahraga_combo.pack(fill="x", pady=(5, 0))
        input_btn = WidgetUtils.create_styled_button(
            fields_frame,
            "INPUT",
            command=self.input_minat_bakat,
            style_name="button_success",
        )
        input_btn.pack(side="right", pady=(20, 0))

    def setup_minat_data_list(self, parent):
        list_frame = WidgetUtils.create_styled_frame(
            parent, "card_frame", bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        list_title = WidgetUtils.create_styled_label(
            list_frame,
            "Data Minat Bakat Mahasiswa",
            "heading_label",
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        list_title.pack(pady=(0, 15))
        self.minat_data_frame = WidgetUtils.create_styled_frame(
            list_frame, bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        self.minat_data_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def load_data(self):
        self.load_statistics()
        self.load_sports()
        self.load_mahasiswa_data()
        self.load_minat_data()
        self.load_olahraga_options()
        self.load_mahasiswa_options()
        self.create_chart()

    def load_statistics(self):
        recap_data = self.admin.lihat_rekap_data()
        for widget in self.stats_cards_frame.winfo_children():
            widget.destroy()
        stats = [
            ("Total Mahasiswa", recap_data.get("total_mahasiswa", 0), "primary"),
            ("Total Minat Terdaftar", recap_data.get("total_minat", 0), "success"),
            ("Olahraga Tersedia", len(Olahraga.get_all()), "info"),
        ]
        for title, value, color in stats:
            self.create_stat_card(self.stats_cards_frame, title, value, color)

    def create_stat_card(self, parent, title: str, value: int, color_type: str):
        bg_color = DarkBlueTheme.get_color(
            f"accent_{color_type}" if color_type != "info" else "accent_info"
        )
        card_frame = WidgetUtils.create_styled_frame(
            parent,
            "card_frame",
            bg=bg_color,
        )
        card_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)

        def is_bright(hex_color: str) -> bool:
            hex_color = hex_color.lstrip("#")
            r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
            return (r * 299 + g * 587 + b * 114) / 1000 > 200

        text_color = "#1E293B" if is_bright(bg_color) else "#FFFFFF"
        value_label = WidgetUtils.create_styled_label(
            card_frame,
            str(value),
            font=("Segoe UI", 28, "bold"),
            fg=text_color,
            bg=bg_color,
        )
        value_label.pack(pady=(10, 0))
        title_label = WidgetUtils.create_styled_label(
            card_frame,
            title,
            font=("Segoe UI", 13, "bold"),
            fg=text_color,
            bg=bg_color,
        )
        title_label.pack(pady=(0, 10))

    def load_sports(self):
        sports = Olahraga.get_with_statistics()
        for widget in self.sports_list_frame.winfo_children():
            widget.destroy()
        self.sports_grid_row = 0
        self.sports_grid_col = 0
        for i in range(self.max_cols):
            self.sports_list_frame.grid_columnconfigure(i, weight=1, minsize=200)
        total_sports = len(sports)
        total_rows = (total_sports + self.max_cols - 1) // self.max_cols
        for row in range(total_rows):
            self.sports_list_frame.grid_rowconfigure(row, weight=0)
        for sport_data in sports:
            self.create_sport_card(sport_data)

    def create_sport_card(self, sport_data):
        card_frame = WidgetUtils.create_styled_frame(
            self.sports_list_frame,
            "card_frame",
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        icon = "🏅" if sport_data["kategori"] == "Individual" else "⚽"
        header = WidgetUtils.create_styled_label(
            card_frame,
            f"{icon} {sport_data['nama_olahraga']}",
            font=("Segoe UI", 10, "bold"),
            fg=DarkBlueTheme.get_color("text_primary"),
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        header.pack(anchor="w", pady=(2, 0))
        kategori_label = WidgetUtils.create_styled_label(
            card_frame,
            f"Kategori: {sport_data['kategori']}",
            font=("Segoe UI", 9),
            fg=DarkBlueTheme.get_color("text_secondary"),
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        kategori_label.pack(anchor="w")
        desc_text = sport_data["deskripsi"] or "Tidak ada deskripsi"
        if len(desc_text) > 50:
            desc_text = desc_text[:50] + "..."
        desc_label = WidgetUtils.create_styled_label(
            card_frame,
            f"Deskripsi: {desc_text}",
            font=("Segoe UI", 9),
            fg=DarkBlueTheme.get_color("text_secondary"),
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        desc_label.pack(anchor="w")
        peminat_label = WidgetUtils.create_styled_label(
            card_frame,
            f"👥 {sport_data['jumlah_peminat']} Peminat",
            font=("Segoe UI", 9),
            fg=DarkBlueTheme.get_color("text_secondary"),
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        peminat_label.pack(anchor="w")
        actions_frame = WidgetUtils.create_styled_frame(
            card_frame, bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        actions_frame.pack(fill="x", pady=(6, 0))
        edit_btn = WidgetUtils.create_styled_button(
            actions_frame,
            "✏️ EDIT",
            command=lambda s=sport_data: self.edit_sport(s),
            style_name="button_secondary",
        )
        edit_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        if sport_data["jumlah_peminat"] == 0:
            delete_btn = WidgetUtils.create_styled_button(
                actions_frame,
                "🗑️ HAPUS",
                command=lambda s=sport_data: self.delete_sport(s),
                style_name="button_danger",
            )
            delete_btn.pack(side="right", fill="x", expand=True, padx=(4, 0))
        card_frame.grid(
            row=self.sports_grid_row,
            column=self.sports_grid_col,
            padx=8,
            pady=8,
            sticky="nsew",
        )
        self.sports_grid_col += 1
        if self.sports_grid_col >= self.max_cols:
            self.sports_grid_col = 0
            self.sports_grid_row += 1

    def create_mahasiswa_card(self, mahasiswa):
        card_frame = WidgetUtils.create_styled_frame(
            self.mahasiswa_list_frame,
            "card_frame",
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        header = WidgetUtils.create_styled_label(
            card_frame,
            f"{mahasiswa.nama} ({mahasiswa.nim})",
            font=("Segoe UI", 10, "bold"),
            fg=DarkBlueTheme.get_color("text_primary"),
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        header.pack(anchor="w", pady=(2, 0))
        fakultas_label = WidgetUtils.create_styled_label(
            card_frame,
            f"Fakultas: {mahasiswa.fakultas}",
            font=("Segoe UI", 9),
            fg=DarkBlueTheme.get_color("text_secondary"),
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        fakultas_label.pack(anchor="w")
        pic_label = WidgetUtils.create_styled_label(
            card_frame,
            f"PIC: {mahasiswa.pic}",
            font=("Segoe UI", 9),
            fg=DarkBlueTheme.get_color("text_secondary"),
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        pic_label.pack(anchor="w")
        actions_frame = WidgetUtils.create_styled_frame(
            card_frame, bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        actions_frame.pack(fill="x", pady=(6, 0))
        edit_btn = WidgetUtils.create_styled_button(
            actions_frame,
            "✏️ EDIT",
            command=lambda m=mahasiswa: self.edit_mahasiswa(m),
            style_name="button_secondary",
        )
        edit_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        delete_btn = WidgetUtils.create_styled_button(
            actions_frame,
            "🗑️ HAPUS",
            command=lambda m=mahasiswa: self.delete_mahasiswa(m),
            style_name="button_danger",
        )
        delete_btn.pack(side="right", fill="x", expand=True, padx=(4, 0))
        return card_frame

    def edit_mahasiswa(self, mahasiswa):
        EditMahasiswaDialog(self.window, mahasiswa, self.on_mahasiswa_edited)

    def on_mahasiswa_edited(self):
        self.load_mahasiswa_data()

    def delete_mahasiswa(self, mahasiswa):
        if DialogUtils.ask_confirmation(
            "Konfirmasi", f"Hapus mahasiswa {mahasiswa.nama} ({mahasiswa.nim})?"
        ):
            from ..models.user import Mahasiswa as MahasiswaModel

            MahasiswaModel.delete_by_nim(mahasiswa.nim)
            self.load_mahasiswa_data()

    def load_mahasiswa_data(self):
        for widget in self.mahasiswa_list_frame.winfo_children():
            widget.destroy()
        mahasiswa_list = Mahasiswa.get_all()
        max_cols = 2
        row = 0
        col = 0
        for mhs in mahasiswa_list:
            card_frame = self.create_mahasiswa_card(mhs)
            card_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        for i in range(max_cols):
            self.mahasiswa_list_frame.grid_columnconfigure(i, weight=1, minsize=200)

    def load_minat_data(self):
        minat_data = MinatBakat.get_all()
        for widget in self.minat_data_frame.winfo_children():
            widget.destroy()
        max_cols = 2
        row = 0
        col = 0
        for data in minat_data:
            card_frame = self.create_minat_item(data)
            card_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        for i in range(max_cols):
            self.minat_data_frame.grid_columnconfigure(i, weight=1, minsize=200)

    def create_minat_item(self, data):
        card_frame = WidgetUtils.create_styled_frame(
            self.minat_data_frame,
            "card_frame",
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        header = WidgetUtils.create_styled_label(
            card_frame,
            f"{data['mahasiswa_nama']} ({data['mahasiswa_nim']})",
            font=("Segoe UI", 10, "bold"),
            fg=DarkBlueTheme.get_color("text_primary"),
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        header.pack(anchor="w", pady=(2, 0))
        fakultas_label = WidgetUtils.create_styled_label(
            card_frame,
            f"Fakultas: {data['fakultas']}",
            font=("Segoe UI", 9),
            fg=DarkBlueTheme.get_color("text_secondary"),
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        fakultas_label.pack(anchor="w")
        olahraga_label = WidgetUtils.create_styled_label(
            card_frame,
            f"Olahraga: {data['nama_olahraga']}",
            font=("Segoe UI", 9),
            fg=DarkBlueTheme.get_color("text_secondary"),
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        olahraga_label.pack(anchor="w")
        tanggal_label = WidgetUtils.create_styled_label(
            card_frame,
            f"Tanggal: {DataUtils.format_date_short(DataUtils.parse_datetime(data['tanggal_input']))}",
            font=("Segoe UI", 9),
            fg=DarkBlueTheme.get_color("text_secondary"),
            bg=DarkBlueTheme.get_color("bg_tertiary"),
        )
        tanggal_label.pack(anchor="w")
        actions_frame = WidgetUtils.create_styled_frame(
            card_frame, bg=DarkBlueTheme.get_color("bg_tertiary")
        )
        actions_frame.pack(fill="x", pady=(6, 0))
        delete_btn = WidgetUtils.create_styled_button(
            actions_frame,
            "🗑️ HAPUS",
            command=lambda d=data: self.delete_minat(d),
            style_name="button_danger",
        )
        delete_btn.pack(side="right", fill="x", expand=True, padx=(4, 0))
        return card_frame

    def load_olahraga_options(self):
        sports = Olahraga.get_all()
        sport_names = [f"{sport.nama_olahraga} (ID: {sport.id})" for sport in sports]
        self.minat_olahraga_combo["values"] = sport_names

    def load_mahasiswa_options(self):
        mahasiswa_list = Mahasiswa.get_all()
        mahasiswa_options = [
            f"{mhs.nim} - {mhs.nama} ({mhs.fakultas})" for mhs in mahasiswa_list
        ]
        self.minat_nim_combo["values"] = mahasiswa_options
        self.minat_nim_combo.bind("<KeyRelease>", self.on_nim_keyrelease)

    def on_nim_keyrelease(self, event):
        value = event.widget.get()
        if not value:
            mahasiswa_list = Mahasiswa.get_all()
            mahasiswa_options = [
                f"{mhs.nim} - {mhs.nama} ({mhs.fakultas})" for mhs in mahasiswa_list
            ]
            event.widget["values"] = mahasiswa_options
            return
        mahasiswa_list = Mahasiswa.get_all()
        filtered_options = []
        for mhs in mahasiswa_list:
            option_text = f"{mhs.nim} - {mhs.nama} ({mhs.fakultas})"
            if value.lower() in mhs.nim.lower() or value.lower() in mhs.nama.lower():
                filtered_options.append(option_text)
        event.widget["values"] = filtered_options
        if filtered_options:
            event.widget.event_generate("<Down>")

    def create_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        recap_data = self.admin.lihat_rekap_data()
        sports_data = recap_data.get("sports_data", [])
        if not sports_data:
            no_data_label = WidgetUtils.create_styled_label(
                self.chart_frame,
                "Tidak ada data untuk ditampilkan",
                "heading_label",
                fg=DarkBlueTheme.get_color("text_muted"),
            )
            no_data_label.pack(expand=True)
            return
        plt.style.use("dark_background")
        fig = Figure(
            figsize=(12, 9),
            facecolor=DarkBlueTheme.get_color("bg_tertiary"),
            edgecolor="none",
        )
        ax = fig.add_subplot(111, facecolor=DarkBlueTheme.get_color("bg_tertiary"))
        names = [sport["nama_olahraga"] for sport in sports_data[:10]]
        counts = [sport["jumlah_peminat"] for sport in sports_data[:10]]
        if self.chart_type_var.get() == "Pie Chart" and any(
            count > 0 for count in counts
        ):
            filtered_data = [
                (name, count) for name, count in zip(names, counts) if count > 0
            ]
            if filtered_data:
                names, counts = zip(*filtered_data)
                ax.pie(counts, labels=names, autopct="%1.1f%%", startangle=90)
                ax.set_title(
                    "Distribusi Minat Olahraga", color="white", fontsize=16, pad=30
                )
        else:
            bars = ax.bar(names, counts, color="#3B82F6")
            ax.set_title(
                "Jumlah Peminat per Olahraga", color="white", fontsize=16, pad=30
            )
            ax.set_xlabel("Olahraga", color="white", fontsize=12)
            ax.set_ylabel("Jumlah Peminat", color="white", fontsize=12)
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
            if counts and max(counts) > 0:
                import numpy as np

                max_val = max(counts)
                y_ticks = list(range(0, int(max_val) + 1))
                ax.set_yticks(y_ticks)
                ax.set_yticklabels([str(i) for i in y_ticks])
            for bar in bars:
                height = bar.get_height()
                if max(counts) > 0:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2.0,
                        height + max(counts) * 0.01,
                        f"{int(height)}",
                        ha="center",
                        va="bottom",
                        color="white",
                    )
        ax.tick_params(colors="white", width=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.grid(True, alpha=0.2, color="#888888", linestyle="-", linewidth=0.3)
        ax.set_axisbelow(True)
        fig.subplots_adjust(
            left=0.12,
            right=0.95,
            top=0.85,
            bottom=0.25,
        )
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(
            bg=DarkBlueTheme.get_color("bg_tertiary"),
            highlightthickness=0,
            relief="flat",
            bd=0,
        )
        canvas_widget.pack(fill="both", expand=True, padx=15, pady=15)

    def update_chart(self, event=None):
        self.create_chart()

    def add_sport(self):
        name = self.sport_name_entry.get().strip()
        category = self.sport_category_var.get()
        description = self.sport_desc_entry.get().strip()
        if not ValidationUtils.validate_olahraga_name(name):
            DialogUtils.show_error("Error", "Nama olahraga tidak valid!")
            return
        sport = Olahraga(nama_olahraga=name, kategori=category, deskripsi=description)
        if sport.tambah_olahraga():
            DialogUtils.show_success("Berhasil", "Olahraga berhasil ditambahkan!")
            self.sport_name_entry.delete(0, tk.END)
            self.sport_desc_entry.delete(0, tk.END)
            self.load_sports()
            self.load_olahraga_options()
            self.create_chart()
        else:
            DialogUtils.show_error("Error", "Gagal menambahkan olahraga!")

    def edit_sport(self, sport_data):
        EditSportDialog(self.window, sport_data, self.on_sport_edited)

    def on_sport_edited(self):
        self.load_sports()
        self.load_olahraga_options()
        self.create_chart()

    def delete_sport(self, sport_data):
        if DialogUtils.ask_confirmation(
            "Konfirmasi", f"Hapus olahraga {sport_data['nama_olahraga']}?"
        ):
            sport = Olahraga.get_by_id(sport_data["id"])
            if sport and sport.hapus_olahraga():
                DialogUtils.show_success("Berhasil", "Olahraga berhasil dihapus!")
                self.load_sports()
                self.load_olahraga_options()
                self.create_chart()
            else:
                DialogUtils.show_error(
                    "Error",
                    "Gagal menghapus olahraga! Mungkin masih ada mahasiswa yang memilihnya.",
                )

    def input_minat_bakat(self):
        nim_text = self.minat_nim_var.get().strip()
        olahraga_text = self.minat_olahraga_var.get()
        if not nim_text or not olahraga_text:
            DialogUtils.show_error("Error", "NIM dan olahraga harus dipilih!")
            return
        try:
            nim = nim_text.split(" - ")[0].strip()
        except:
            DialogUtils.show_error("Error", "Format NIM tidak valid!")
            return
        try:
            olahraga_id = int(olahraga_text.split("ID: ")[1].split(")")[0])
        except:
            DialogUtils.show_error("Error", "Format olahraga tidak valid!")
            return
        if self.admin.input_data_minat_bakat(nim, olahraga_id):
            DialogUtils.show_success("Berhasil", "Data minat bakat berhasil diinput!")
            self.minat_nim_var.set("")
            self.minat_olahraga_var.set("")
            self.load_minat_data()
            self.load_statistics()
            self.create_chart()
        else:
            DialogUtils.show_error("Error", "Gagal menginput data minat bakat!")

    def delete_minat(self, data):
        if DialogUtils.ask_confirmation(
            "Konfirmasi", f"Hapus data minat {data['mahasiswa_nama']}?"
        ):
            if MinatBakat.delete_by_id(data["id"]):
                DialogUtils.show_success("Berhasil", "Data berhasil dihapus!")
                self.load_minat_data()
                self.load_statistics()
                self.create_chart()
            else:
                DialogUtils.show_error("Error", "Gagal menghapus data!")

    def logout(self):
        if DialogUtils.ask_confirmation("Logout", "Yakin ingin logout?"):
            try:
                self.window.quit()
                self.window.destroy()
            except:
                pass
            if self.on_logout:
                self.on_logout()

    def show(self):
        try:
            self.ensure_fullscreen()
            self.window.deiconify()
            self.window.lift()
            self.window.focus_force()
            self.window.mainloop()
        except tk.TclError:
            pass


class EditSportDialog:
    def __init__(self, parent, sport_data, on_success):
        self.sport_data = sport_data
        self.on_success = on_success
        self.window = tk.Toplevel(parent)
        self.window.title("Edit Olahraga")
        self.window.configure(bg=DarkBlueTheme.get_color("bg_primary"))
        self.window.transient(parent)
        self.window.grab_set()
        WidgetUtils.center_window(self.window, 500, 450)
        self.setup_ui()

    def setup_ui(self):
        main_frame = WidgetUtils.create_styled_frame(
            self.window, "card_frame", bg=DarkBlueTheme.get_color("bg_secondary")
        )
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        title_label = WidgetUtils.create_styled_label(
            main_frame, "Edit Olahraga", "heading_label"
        )
        title_label.pack(pady=(0, 25))
        name_label = WidgetUtils.create_styled_label(main_frame, "Nama Olahraga:")
        name_label.pack(anchor="w", pady=(0, 8))
        self.name_entry = WidgetUtils.create_styled_entry(main_frame)
        self.name_entry.pack(fill="x", pady=(0, 15))
        self.name_entry.insert(0, self.sport_data["nama_olahraga"])
        category_label = WidgetUtils.create_styled_label(main_frame, "Kategori:")
        category_label.pack(anchor="w", pady=(0, 8))
        self.category_var = tk.StringVar(value=self.sport_data["kategori"])
        category_combo = ttk.Combobox(
            main_frame,
            textvariable=self.category_var,
            values=["Individual", "Tim"],
            state="readonly",
            font=DarkBlueTheme.get_font("body"),
        )
        category_combo.pack(fill="x", pady=(0, 15))
        desc_label = WidgetUtils.create_styled_label(main_frame, "Deskripsi:")
        desc_label.pack(anchor="w", pady=(0, 8))
        self.desc_entry = WidgetUtils.create_styled_entry(main_frame)
        self.desc_entry.pack(fill="x", pady=(0, 25))
        self.desc_entry.insert(0, self.sport_data["deskripsi"] or "")
        buttons_frame = WidgetUtils.create_styled_frame(main_frame)
        buttons_frame.pack(fill="x", pady=(10, 0))
        save_btn = WidgetUtils.create_styled_button(
            buttons_frame,
            "SIMPAN",
            command=self.save_changes,
            style_name="button_success",
        )
        save_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        cancel_btn = WidgetUtils.create_styled_button(
            buttons_frame,
            "BATAL",
            command=self.window.destroy,
            style_name="button_secondary",
        )
        cancel_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

    def save_changes(self):
        name = self.name_entry.get().strip()
        category = self.category_var.get()
        description = self.desc_entry.get().strip()
        if not ValidationUtils.validate_olahraga_name(name):
            DialogUtils.show_error("Error", "Nama olahraga tidak valid!")
            return
        sport = Olahraga.get_by_id(self.sport_data["id"])
        if sport and sport.update_olahraga(name, category, description):
            DialogUtils.show_success("Berhasil", "Olahraga berhasil diupdate!")
            self.window.destroy()
            self.on_success()
        else:
            DialogUtils.show_error("Error", "Gagal mengupdate olahraga!")


class EditMahasiswaDialog:
    def __init__(self, parent, mahasiswa, on_success):
        self.mahasiswa = mahasiswa
        self.on_success = on_success
        self.window = tk.Toplevel(parent)
        self.window.title("Edit Mahasiswa")
        self.window.configure(bg=DarkBlueTheme.get_color("bg_primary"))
        self.window.transient(parent)
        self.window.grab_set()
        WidgetUtils.center_window(self.window, 400, 400)
        self.setup_ui()

    def setup_ui(self):
        main_frame = WidgetUtils.create_styled_frame(
            self.window, "card_frame", bg=DarkBlueTheme.get_color("bg_secondary")
        )
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        title_label = WidgetUtils.create_styled_label(
            main_frame, "Edit Data Mahasiswa", "heading_label"
        )
        title_label.pack(pady=(0, 15))
        nama_label = WidgetUtils.create_styled_label(main_frame, "Nama:")
        nama_label.pack(anchor="w")
        self.nama_entry = WidgetUtils.create_styled_entry(main_frame)
        self.nama_entry.pack(fill="x", pady=(0, 10))
        self.nama_entry.insert(0, self.mahasiswa.nama)
        fakultas_label = WidgetUtils.create_styled_label(main_frame, "Fakultas:")
        fakultas_label.pack(anchor="w")
        self.fakultas_entry = WidgetUtils.create_styled_entry(main_frame)
        self.fakultas_entry.pack(fill="x", pady=(0, 10))
        self.fakultas_entry.insert(0, self.mahasiswa.fakultas)
        pic_label = WidgetUtils.create_styled_label(main_frame, "PIC:")
        pic_label.pack(anchor="w")
        self.pic_entry = WidgetUtils.create_styled_entry(main_frame)
        self.pic_entry.pack(fill="x", pady=(0, 20))
        self.pic_entry.insert(0, self.mahasiswa.pic)
        btn_frame = WidgetUtils.create_styled_frame(main_frame)
        btn_frame.pack(fill="x")
        save_btn = WidgetUtils.create_styled_button(
            btn_frame, "SIMPAN", command=self.save_changes, style_name="button_success"
        )
        save_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        cancel_btn = WidgetUtils.create_styled_button(
            btn_frame,
            "BATAL",
            command=self.window.destroy,
            style_name="button_secondary",
        )
        cancel_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

    def save_changes(self):
        from ..models.user import Mahasiswa as MahasiswaModel

        nama = self.nama_entry.get().strip()
        fakultas = self.fakultas_entry.get().strip()
        pic = self.pic_entry.get().strip()
        if not nama or not fakultas or not pic:
            DialogUtils.show_error("Error", "Semua field harus diisi!")
            return
        if MahasiswaModel.update_by_nim(self.mahasiswa.nim, nama, fakultas, pic):
            DialogUtils.show_success("Berhasil", "Data mahasiswa berhasil diupdate!")
            self.window.destroy()
            if self.on_success:
                self.on_success()
        else:
            DialogUtils.show_error("Error", "Gagal mengupdate data mahasiswa!")

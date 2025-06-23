import tkinter as tk
from tkinter import ttk
from ..utils import DarkBlueTheme, WidgetUtils, DialogUtils, DataUtils
from ..models import Mahasiswa, Olahraga


class MahasiswaDashboard:
    def __init__(self, mahasiswa: Mahasiswa, on_logout: callable):
        self.mahasiswa = mahasiswa
        self.on_logout = on_logout
        self.selected_sports = []
        self.window = tk.Tk()
        self.window.title(f"Dashboard Mahasiswa - {mahasiswa.nama}")
        self.window.configure(bg=DarkBlueTheme.get_color("bg_primary"))
        self.window.attributes("-fullscreen", False)
        self.window.state("zoomed")
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.window.minsize(1200, 800)
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
                self.window.after_idle(lambda: self.window.state("zoomed"))

    def on_window_map(self, event):
        if event.widget == self.window:
            self.ensure_fullscreen()

    def ensure_fullscreen(self):
        try:
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            self.window.state("zoomed")
            self.window.geometry(f"{screen_width}x{screen_height}+0+0")
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
        self.setup_dashboard_content(content_frame)

    def setup_dashboard_content(self, parent):
        canvas = tk.Canvas(
            parent,
            bg=DarkBlueTheme.get_color("bg_primary"),
            highlightthickness=0,
            relief="flat",
            bd=0,
        )
        canvas.pack(fill="both", expand=True, padx=0, pady=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollbar.pack_forget()
        scrollable_frame = WidgetUtils.create_styled_frame(
            canvas, bg=DarkBlueTheme.get_color("bg_primary"), relief="flat", bd=0
        )
        scrollable_frame_id = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw"
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        def resize_scrollable_frame(event):
            canvas_width = event.width
            canvas.itemconfig(scrollable_frame_id, width=canvas_width)

        canvas.bind("<Configure>", resize_scrollable_frame)

        def update_scrollregion(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", update_scrollregion)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        self.window.bind("<MouseWheel>", _on_mousewheel)

        def bind_mousewheel_recursive(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel_recursive(child)

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
        bind_mousewheel_recursive(content_wrapper)
        self.setup_stats_section(content_container)
        self.setup_sports_section(content_container)
        self.setup_my_sports_section(content_container)

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
            "👨‍🎓 Dashboard Mahasiswa",
            font=("Segoe UI", 24, "bold"),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        title_label.pack(anchor="w")
        user_label = WidgetUtils.create_styled_label(
            user_info_frame,
            f"Selamat datang, {self.mahasiswa.nama}",
            font=("Segoe UI", 14),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_secondary"),
        )
        user_label.pack(anchor="w", pady=(5, 0))
        student_info = (
            f"NIM: {self.mahasiswa.nim} | Fakultas: {self.mahasiswa.fakultas}"
        )
        info_label = WidgetUtils.create_styled_label(
            user_info_frame,
            student_info,
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
            command=self.refresh_data,
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

    def setup_stats_section(self, parent):
        stats_title = WidgetUtils.create_styled_label(
            parent,
            "📊 Ringkasan Minat Olahraga",
            font=("Segoe UI", 18, "bold"),
            bg=DarkBlueTheme.get_color("bg_primary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        stats_title.pack(pady=(0, 20), padx=0)
        cards_frame = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("bg_primary"), relief="flat", bd=0
        )
        cards_frame.pack(fill="both", expand=True, pady=(0, 30), padx=0)
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)
        self.stats_cards = {}
        self.create_stat_card(
            cards_frame,
            "total_sports",
            "⚽",
            "Total Olahraga",
            "0",
            "Olahraga tersedia",
            0,
        )
        self.create_stat_card(
            cards_frame, "my_sports", "❤️", "Minat Saya", "0", "Olahraga yang dipilih", 1
        )
        self.create_stat_card(
            cards_frame,
            "individual_sports",
            "🏃",
            "Individual",
            "0",
            "Olahraga individual",
            2,
        )
        self.create_stat_card(
            cards_frame, "team_sports", "🤝", "Tim", "0", "Olahraga tim", 3
        )

    def create_stat_card(self, parent, card_id, icon, title, value, subtitle, col=0):
        card_frame = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("bg_card"), relief="flat", bd=0
        )
        card_frame.grid(row=0, column=col, sticky="nsew", padx=5)
        card_content = WidgetUtils.create_styled_frame(
            card_frame, bg=DarkBlueTheme.get_color("bg_card"), relief="flat", bd=0
        )
        card_content.pack(fill="both", expand=True, padx=20, pady=20)
        header_frame = WidgetUtils.create_styled_frame(
            card_content, bg=DarkBlueTheme.get_color("bg_card"), relief="flat", bd=0
        )
        header_frame.pack(fill="x", pady=(0, 10))
        icon_label = WidgetUtils.create_styled_label(
            header_frame,
            icon,
            font=("Segoe UI Emoji", 24),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("accent_info"),
        )
        icon_label.pack(side="left")
        title_label = WidgetUtils.create_styled_label(
            header_frame,
            title,
            font=("Segoe UI", 14, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        title_label.pack(side="right", anchor="e")
        value_label = WidgetUtils.create_styled_label(
            card_content,
            value,
            font=("Segoe UI", 28, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("accent_success"),
        )
        value_label.pack(pady=(5, 10))
        subtitle_label = WidgetUtils.create_styled_label(
            card_content,
            subtitle,
            font=("Segoe UI", 11),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_muted"),
        )
        subtitle_label.pack()
        self.stats_cards[card_id] = {
            "value_label": value_label,
            "card_frame": card_frame,
        }

    def setup_sports_section(self, parent):
        sports_title = WidgetUtils.create_styled_label(
            parent,
            "🏅 Pilih Olahraga",
            font=("Segoe UI", 18, "bold"),
            bg=DarkBlueTheme.get_color("bg_primary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        sports_title.pack(pady=(0, 20), padx=0)
        separator = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("border"), relief="flat", bd=0, height=1
        )
        separator.pack(fill="x", padx=0, pady=10)
        sports_container = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("bg_card"), relief="flat", bd=0
        )
        sports_container.pack(fill="both", expand=True, padx=0, pady=(0, 30))
        controls_frame = WidgetUtils.create_styled_frame(
            sports_container, bg=DarkBlueTheme.get_color("bg_card"), relief="flat", bd=0
        )
        controls_frame.pack(fill="x", padx=10, pady=15)
        search_label = WidgetUtils.create_styled_label(
            controls_frame,
            "🔍 Cari Olahraga:",
            font=("Segoe UI", 12, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        search_label.pack(side="left", padx=(0, 10))
        self.search_entry = WidgetUtils.create_styled_entry(controls_frame)
        self.search_entry.pack(side="left", padx=(0, 20))
        self.search_entry.bind("<KeyRelease>", self.filter_sports)
        category_label = WidgetUtils.create_styled_label(
            controls_frame,
            "📂 Kategori:",
            font=("Segoe UI", 12, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        category_label.pack(side="left", padx=(0, 10))
        self.category_var = tk.StringVar(value="Semua")
        self.category_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.category_var,
            values=["Semua", "Individual", "Tim"],
            state="readonly",
            font=("Segoe UI", 10),
        )
        self.category_combo.pack(side="left")
        self.category_combo.bind("<<ComboboxSelected>>", self.filter_sports)
        self.sports_list_frame = WidgetUtils.create_styled_frame(
            sports_container, bg=DarkBlueTheme.get_color("bg_card"), relief="flat", bd=0
        )
        self.sports_list_frame.pack(fill="both", expand=True, padx=5, pady=(0, 15))

    def setup_my_sports_section(self, parent):
        my_sports_title = WidgetUtils.create_styled_label(
            parent,
            "❤️ Minat Olahraga Saya",
            font=("Segoe UI", 18, "bold"),
            bg=DarkBlueTheme.get_color("bg_primary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        my_sports_title.pack(pady=(0, 20), padx=0)
        separator = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("border"), relief="flat", bd=0, height=1
        )
        separator.pack(fill="x", padx=0, pady=(0, 10))
        my_sports_container = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("bg_card"), relief="flat", bd=0
        )
        my_sports_container.pack(fill="x", padx=0, pady=(0, 20))
        self.my_sports_frame = WidgetUtils.create_styled_frame(
            my_sports_container,
            bg=DarkBlueTheme.get_color("bg_card"),
            relief="flat",
            bd=0,
        )
        self.my_sports_frame.pack(fill="both", expand=True, padx=5, pady=15)

    def load_data(self):
        try:
            self.all_sports = Olahraga.get_all()
            self.selected_sports = self.mahasiswa.get_minat_olahraga()
            self.update_statistics()
            self.display_sports()
            self.display_my_sports()
        except Exception as e:
            DialogUtils.show_error("Error", f"Gagal memuat data: {str(e)}")

    def refresh_data(self):
        self.load_data()

    def update_statistics(self):
        try:
            total_sports = len(self.all_sports)
            self.stats_cards["total_sports"]["value_label"].config(
                text=str(total_sports)
            )
            my_sports_count = len(self.selected_sports)
            self.stats_cards["my_sports"]["value_label"].config(
                text=str(my_sports_count)
            )
            individual_count = len(
                [s for s in self.all_sports if s.kategori == "Individual"]
            )
            self.stats_cards["individual_sports"]["value_label"].config(
                text=str(individual_count)
            )
            team_count = len([s for s in self.all_sports if s.kategori == "Tim"])
            self.stats_cards["team_sports"]["value_label"].config(text=str(team_count))
        except Exception:
            pass

    def display_sports(self):
        for widget in self.sports_list_frame.winfo_children():
            widget.destroy()
        search_text = (
            self.search_entry.get().lower() if hasattr(self, "search_entry") else ""
        )
        category_filter = (
            self.category_var.get() if hasattr(self, "category_var") else "Semua"
        )
        selected_ids = [sport["id"] for sport in self.selected_sports]
        filtered_sports = [
            sport
            for sport in self.all_sports
            if (not search_text or search_text in sport.nama_olahraga.lower())
            and (category_filter == "Semua" or sport.kategori == category_filter)
        ]
        for i, sport in enumerate(filtered_sports):
            self.create_sport_card(sport, sport.id in selected_ids, i)

    def create_sport_card(self, sport: Olahraga, is_selected: bool, index: int):
        sport_card = WidgetUtils.create_styled_frame(
            self.sports_list_frame,
            bg=DarkBlueTheme.get_color("bg_secondary"),
            relief="flat",
            bd=0,
        )
        sport_card.pack(fill="x", pady=5, padx=0)
        sport_card.update_idletasks()
        parent_width = self.sports_list_frame.winfo_width()
        if parent_width > 0:
            sport_card.config(width=parent_width)
        card_content = WidgetUtils.create_styled_frame(
            sport_card, bg=DarkBlueTheme.get_color("bg_secondary"), relief="flat", bd=0
        )
        card_content.pack(fill="x", padx=15, pady=10)
        info_frame = WidgetUtils.create_styled_frame(
            card_content, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        info_frame.pack(side="left", fill="both", expand=True)
        name_label = WidgetUtils.create_styled_label(
            info_frame,
            sport.nama_olahraga,
            font=("Segoe UI", 14, "bold"),
            bg=DarkBlueTheme.get_color("bg_secondary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        name_label.pack(anchor="w")
        category_frame = WidgetUtils.create_styled_frame(
            info_frame, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        category_frame.pack(anchor="w", pady=(5, 0))
        category_badge = WidgetUtils.create_styled_label(
            category_frame,
            f"📂 {sport.kategori}",
            font=("Segoe UI", 10),
            bg=DarkBlueTheme.get_color("primary_light"),
            fg="white",
        )
        category_badge.pack(side="left", padx=(0, 10))
        if sport.deskripsi:
            desc_text = (
                sport.deskripsi
                if len(sport.deskripsi) <= 120
                else sport.deskripsi[:117] + "..."
            )
            desc_label = WidgetUtils.create_styled_label(
                info_frame,
                desc_text,
                font=("Segoe UI", 10),
                bg=DarkBlueTheme.get_color("bg_secondary"),
                fg=DarkBlueTheme.get_color("text_muted"),
            )
            desc_label.pack(anchor="w", pady=(5, 0))
        action_frame = WidgetUtils.create_styled_frame(
            card_content, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        action_frame.pack(side="right", fill="y")
        if is_selected:
            action_btn = WidgetUtils.create_styled_button(
                action_frame,
                "✓ TERPILIH",
                command=lambda s=sport: self.remove_sport(s),
                style_name="button_success",
                font=("Segoe UI", 10, "bold"),
            )
        else:
            action_btn = WidgetUtils.create_styled_button(
                action_frame,
                "❤️ PILIH",
                command=lambda s=sport: self.select_sport(s),
                style_name="button_primary",
                font=("Segoe UI", 10, "bold"),
            )
        action_btn.pack(anchor="center")

    def display_my_sports(self):
        for widget in self.my_sports_frame.winfo_children():
            widget.destroy()
        if not self.selected_sports:
            empty_frame = WidgetUtils.create_styled_frame(
                self.my_sports_frame,
                bg=DarkBlueTheme.get_color("bg_card"),
                relief="flat",
                bd=0,
            )
            empty_frame.pack(fill="both", expand=True, pady=50)
            empty_icon = WidgetUtils.create_styled_label(
                empty_frame,
                "😔",
                font=("Segoe UI Emoji", 48),
                bg=DarkBlueTheme.get_color("bg_card"),
                fg=DarkBlueTheme.get_color("text_muted"),
            )
            empty_icon.pack()
            empty_label = WidgetUtils.create_styled_label(
                empty_frame,
                "Belum ada olahraga yang dipilih",
                font=("Segoe UI", 16),
                bg=DarkBlueTheme.get_color("bg_card"),
                fg=DarkBlueTheme.get_color("text_muted"),
            )
            empty_label.pack(pady=(10, 0))
            return
        for i, sport_data in enumerate(self.selected_sports):
            self.create_my_sport_card(sport_data, i)

    def create_my_sport_card(self, sport_data, index: int):
        sport_card = WidgetUtils.create_styled_frame(
            self.my_sports_frame,
            bg=DarkBlueTheme.get_color("bg_secondary"),
            relief="flat",
            bd=0,
        )
        sport_card.pack(fill="x", pady=5, padx=5)
        card_content = WidgetUtils.create_styled_frame(
            sport_card, bg=DarkBlueTheme.get_color("bg_secondary"), relief="flat", bd=0
        )
        card_content.pack(fill="x", padx=15, pady=10)
        info_frame = WidgetUtils.create_styled_frame(
            card_content, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        info_frame.pack(side="left", fill="both", expand=True)
        name_label = WidgetUtils.create_styled_label(
            info_frame,
            f"❤️ {sport_data['nama_olahraga']}",
            font=("Segoe UI", 14, "bold"),
            bg=DarkBlueTheme.get_color("bg_secondary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        name_label.pack(anchor="w")
        info_row = WidgetUtils.create_styled_frame(
            info_frame, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        info_row.pack(anchor="w", pady=(5, 0))
        category_badge = WidgetUtils.create_styled_label(
            info_row,
            f"📂 {sport_data['kategori']}",
            font=("Segoe UI", 10),
            bg=DarkBlueTheme.get_color("primary_light"),
            fg="white",
        )
        category_badge.pack(side="left", padx=(0, 15))
        date_selected = DataUtils.format_date_short(
            DataUtils.parse_datetime(sport_data["tanggal_input"])
        )
        date_label = WidgetUtils.create_styled_label(
            info_row,
            f"📅 Dipilih: {date_selected}",
            font=("Segoe UI", 10),
            bg=DarkBlueTheme.get_color("bg_secondary"),
            fg=DarkBlueTheme.get_color("text_muted"),
        )
        date_label.pack(side="left")
        action_frame = WidgetUtils.create_styled_frame(
            card_content, bg=DarkBlueTheme.get_color("bg_secondary")
        )
        action_frame.pack(side="right", fill="y")
        remove_btn = WidgetUtils.create_styled_button(
            action_frame,
            "🗑️ HAPUS",
            command=lambda: self.remove_sport_by_data(sport_data),
            style_name="button_danger",
            font=("Segoe UI", 10, "bold"),
        )
        remove_btn.pack(anchor="center")

    def select_sport(self, sport: Olahraga):
        try:
            selected_ids = [sport_data["id"] for sport_data in self.selected_sports]
            if sport.id in selected_ids:
                return
            if self.mahasiswa.pilih_minat_olahraga(sport.id):
                self.load_data()
            else:
                DialogUtils.show_error("Error", "Gagal memilih olahraga.")
        except Exception as e:
            DialogUtils.show_error("Error", f"Terjadi kesalahan: {str(e)}")

    def remove_sport(self, sport: Olahraga):
        if DialogUtils.ask_confirmation(
            "Konfirmasi", f"Hapus {sport.nama_olahraga} dari pilihan?"
        ):
            for selected_sport in self.selected_sports:
                if selected_sport["id"] == sport.id:
                    if self.mahasiswa.hapus_minat_olahraga(sport.id):
                        self.load_data()
                        return
            DialogUtils.show_error("Error", "Gagal menghapus pilihan olahraga")

    def remove_sport_by_data(self, sport_data):
        sport = Olahraga.get_by_id(sport_data["id"])
        if sport:
            self.remove_sport(sport)

    def filter_sports(self, event=None):
        self.display_sports()

    def logout(self):
        if DialogUtils.ask_confirmation("Logout", "Yakin ingin logout?"):
            try:
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

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ..utils import DarkBlueTheme, WidgetUtils, DialogUtils, ExportUtils
from ..models import Kemahasiswaan


class KemahasiswaanDashboard:
    def __init__(self, kemahasiswaan: Kemahasiswaan, on_logout: callable):
        self.kemahasiswaan = kemahasiswaan
        self.on_logout = on_logout

        self.window = tk.Tk()
        self.window.title(f"Dashboard Kemahasiswaan - {kemahasiswaan.nama}")
        self.window.configure(bg=DarkBlueTheme.get_color("bg_primary"))
        self.window.state("zoomed")
        self.window.minsize(1200, 800)

        self.current_data = {}

        self.setup_ui()
        self.load_initial_data()

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

        content_wrapper = WidgetUtils.create_styled_frame(
            content_frame,
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

        self.setup_stats_cards(content_container)
        self.setup_charts_section(content_container)

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
            "🏢 Dashboard Kemahasiswaan",
            font=("Segoe UI", 24, "bold"),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        title_label.pack(anchor="w")

        user_label = WidgetUtils.create_styled_label(
            user_info_frame,
            f"Selamat datang, {self.kemahasiswaan.nama}",
            font=("Segoe UI", 14),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_secondary"),
        )
        user_label.pack(anchor="w", pady=(5, 0))

        id_label = WidgetUtils.create_styled_label(
            user_info_frame,
            f"ID: {self.kemahasiswaan.kemahasiswaan_id}",
            font=("Segoe UI", 12),
            bg=DarkBlueTheme.get_color("primary"),
            fg=DarkBlueTheme.get_color("text_muted"),
        )
        id_label.pack(anchor="w", pady=(2, 0))

        actions_frame = WidgetUtils.create_styled_frame(
            header_content, bg=DarkBlueTheme.get_color("primary")
        )
        actions_frame.pack(side="right", fill="y")
        refresh_btn = WidgetUtils.create_styled_button(
            actions_frame,
            "🔄 REFRESH",
            command=self.refresh_all_data,
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

    def setup_stats_cards(self, parent):
        stats_title = WidgetUtils.create_styled_label(
            parent,
            "📊 Statistik Ringkasan",
            font=("Segoe UI", 18, "bold"),
            bg=DarkBlueTheme.get_color("bg_primary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        stats_title.pack(pady=(0, 20), padx=0)
        cards_frame = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("bg_primary"), relief="flat", bd=0
        )
        cards_frame.pack(fill="x", pady=(0, 30))

        self.stats_cards = {}
        self.create_stat_card(
            cards_frame,
            "total_mahasiswa",
            "👥",
            "Total Mahasiswa",
            "0",
            "Terdaftar dalam sistem",
        )
        self.create_stat_card(
            cards_frame,
            "total_olahraga",
            "⚽",
            "Total Olahraga",
            "0",
            "Jenis olahraga tersedia",
        )
        self.create_stat_card(
            cards_frame,
            "total_minat",
            "❤️",
            "Total Minat",
            "0",
            "Pilihan minat mahasiswa",
        )
        self.create_stat_card(
            cards_frame,
            "fakultas_aktif",
            "🏫",
            "Fakultas Aktif",
            "0",
            "Fakultas berpartisipasi",
        )

    def create_stat_card(self, parent, card_id, icon, title, value, subtitle):
        card_frame = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("bg_card"), relief="flat", bd=0
        )
        card_frame.pack(side="left", fill="both", expand=True, padx=5)

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

    def setup_charts_section(self, parent):
        charts_title = WidgetUtils.create_styled_label(
            parent,
            "📈 Visualisasi Data",
            font=("Segoe UI", 18, "bold"),
            bg=DarkBlueTheme.get_color("bg_primary"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        charts_title.pack(pady=(0, 20), padx=0)

        separator = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("border"), relief="flat", bd=0, height=1
        )
        separator.pack(fill="x", padx=50, pady=10)

        charts_container = WidgetUtils.create_styled_frame(
            parent, bg=DarkBlueTheme.get_color("bg_primary"), relief="flat", bd=0
        )
        charts_container.pack(fill="x", padx=0, pady=(0, 30))
        left_chart_frame = WidgetUtils.create_styled_frame(
            charts_container, bg=DarkBlueTheme.get_color("bg_card"), relief="flat", bd=0
        )
        left_chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

        chart_title = WidgetUtils.create_styled_label(
            left_chart_frame,
            "📊 Popularitas Olahraga",
            font=("Segoe UI", 14, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        chart_title.pack(pady=15)

        self.sports_chart_frame = WidgetUtils.create_styled_frame(
            left_chart_frame, bg=DarkBlueTheme.get_color("bg_card"), relief="flat", bd=0
        )
        self.sports_chart_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        right_chart_frame = WidgetUtils.create_styled_frame(
            charts_container, bg=DarkBlueTheme.get_color("bg_card"), relief="flat", bd=0
        )
        right_chart_frame.pack(side="right", fill="both", expand=True, padx=(15, 0))
        chart_title2 = WidgetUtils.create_styled_label(
            right_chart_frame,
            "🏫 Distribusi Fakultas",
            font=("Segoe UI", 14, "bold"),
            bg=DarkBlueTheme.get_color("bg_card"),
            fg=DarkBlueTheme.get_color("text_primary"),
        )
        chart_title2.pack(pady=15)

        self.faculty_chart_frame = WidgetUtils.create_styled_frame(
            right_chart_frame,
            bg=DarkBlueTheme.get_color("bg_card"),
            relief="flat",
            bd=0,
        )
        self.faculty_chart_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def load_initial_data(self):
        try:
            self.refresh_all_data()
        except Exception as e:
            DialogUtils.show_error("Kesalahan", f"Gagal memuat data: {str(e)}")

    def refresh_all_data(self):
        self.load_statistics()
        self.load_sports_data()
        self.load_faculty_data()
        self.update_charts()

    def load_statistics(self):
        try:
            stats = self.kemahasiswaan.get_dashboard_statistics()

            self.stats_cards["total_mahasiswa"]["value_label"].config(
                text=str(stats.get("total_mahasiswa", 0))
            )
            self.stats_cards["total_olahraga"]["value_label"].config(
                text=str(stats.get("total_olahraga", 0))
            )
            self.stats_cards["total_minat"]["value_label"].config(
                text=str(stats.get("total_minat", 0))
            )
            self.stats_cards["fakultas_aktif"]["value_label"].config(
                text=str(stats.get("fakultas_aktif", 0))
            )

            self.current_data["statistics"] = stats
        except Exception:
            for card in self.stats_cards.values():
                card["value_label"].config(text="0")

    def load_sports_data(self):
        try:
            data = self.kemahasiswaan.lihat_rekap_olahraga()
            sports_data = data.get("sports_data", [])
            self.current_data["sports"] = sports_data
        except Exception:
            self.current_data["sports"] = []

    def load_faculty_data(self):
        try:
            data = self.kemahasiswaan.lihat_rekap_fakultas()
            faculty_data = data.get("faculty_data", [])
            self.current_data["faculty"] = faculty_data
        except Exception:
            self.current_data["faculty"] = []

    def update_charts(self):
        try:
            self.update_sports_chart()
            self.update_faculty_chart()
        except Exception:
            pass

    def update_sports_chart(self):
        try:
            for widget in self.sports_chart_frame.winfo_children():
                widget.destroy()

            sports_data = self.current_data.get("sports", [])
            if not sports_data:
                no_chart_label = WidgetUtils.create_styled_label(
                    self.sports_chart_frame,
                    "Data tidak tersedia",
                    bg=DarkBlueTheme.get_color("bg_card"),
                    fg=DarkBlueTheme.get_color("text_muted"),
                )
                no_chart_label.pack(expand=True)
                return

            sports_names = [
                row[0][:10] + "..." if len(row[0]) > 10 else row[0]
                for row in sports_data[:8]
            ]
            popularity = [int(row[2]) for row in sports_data[:8]]

            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor(DarkBlueTheme.get_color("bg_card"))
            ax.set_facecolor(DarkBlueTheme.get_color("bg_card"))

            bars = ax.bar(
                sports_names,
                popularity,
                color=DarkBlueTheme.get_color("primary"),
                alpha=0.8,
            )

            ax.set_xlabel("Olahraga", color=DarkBlueTheme.get_color("text_primary"))
            ax.set_ylabel(
                "Jumlah Peminat", color=DarkBlueTheme.get_color("text_primary")
            )
            ax.tick_params(colors=DarkBlueTheme.get_color("text_primary"), rotation=45)
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, self.sports_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception:
            error_label = WidgetUtils.create_styled_label(
                self.sports_chart_frame,
                "Error membuat grafik",
                bg=DarkBlueTheme.get_color("bg_card"),
                fg=DarkBlueTheme.get_color("accent_danger"),
            )
            error_label.pack(expand=True)

    def update_faculty_chart(self):
        try:
            for widget in self.faculty_chart_frame.winfo_children():
                widget.destroy()

            faculty_data = self.current_data.get("faculty", [])
            if not faculty_data:
                no_chart_label = WidgetUtils.create_styled_label(
                    self.faculty_chart_frame,
                    "Data tidak tersedia",
                    bg=DarkBlueTheme.get_color("bg_card"),
                    fg=DarkBlueTheme.get_color("text_muted"),
                )
                no_chart_label.pack(expand=True)
                return

            faculty_names = [row[0] for row in faculty_data]
            student_counts = [int(row[1]) for row in faculty_data]

            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor(DarkBlueTheme.get_color("bg_card"))

            colors = ["#1f4e79", "#2d5aa0", "#3b66b8", "#4a72d0", "#587ee8"]
            wedges, texts, autotexts = ax.pie(
                student_counts,
                labels=faculty_names,
                autopct="%1.1f%%",
                colors=colors,
                textprops={"color": DarkBlueTheme.get_color("text_primary")},
            )

            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, self.faculty_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception:
            error_label = WidgetUtils.create_styled_label(
                self.faculty_chart_frame,
                "Error membuat grafik",
                bg=DarkBlueTheme.get_color("bg_card"),
                fg=DarkBlueTheme.get_color("accent_danger"),
            )
            error_label.pack(expand=True)

    def export_sports_data(self):
        try:
            data = self.current_data.get("sports", [])
            if not data:
                DialogUtils.show_info("Info", "Tidak ada data untuk diekspor")
                return

            headers = ["Olahraga", "Kategori", "Jumlah Peminat", "Persentase"]
            ExportUtils.export_to_csv(data, headers, "rekap_olahraga.csv")
            DialogUtils.show_success("Sukses", "Data olahraga berhasil diekspor")
        except Exception as e:
            DialogUtils.show_error("Error", f"Gagal mengekspor data: {str(e)}")

    def export_faculty_data(self):
        try:
            data = self.current_data.get("faculty", [])
            if not data:
                DialogUtils.show_info("Info", "Tidak ada data untuk diekspor")
                return

            headers = [
                "Fakultas",
                "Jumlah Mahasiswa",
                "Jumlah Minat",
                "Rata-rata Minat/Mahasiswa",
            ]
            ExportUtils.export_to_csv(data, headers, "rekap_fakultas.csv")
            DialogUtils.show_success("Sukses", "Data fakultas berhasil diekspor")
        except Exception as e:
            DialogUtils.show_error("Error", f"Gagal mengekspor data: {str(e)}")

    def export_category_data(self):
        try:
            data = self.current_data.get("category", [])
            if not data:
                DialogUtils.show_info("Info", "Tidak ada data untuk diekspor")
                return

            headers = ["Kategori", "Jumlah Olahraga", "Jumlah Peminat", "Persentase"]
            ExportUtils.export_to_csv(data, headers, "rekap_kategori.csv")
            DialogUtils.show_success("Sukses", "Data kategori berhasil diekspor")
        except Exception as e:
            DialogUtils.show_error("Error", f"Gagal mengekspor data: {str(e)}")

    def generate_comprehensive_report(self):
        try:
            report_type = self.report_type_var.get()

            for widget in self.report_preview_frame.winfo_children():
                widget.destroy()

            if report_type == "comprehensive":
                self.generate_full_report()
            elif report_type == "sports":
                self.generate_sports_report()
            elif report_type == "faculty":
                self.generate_faculty_report()
            elif report_type == "category":
                self.generate_category_report()
        except Exception as e:
            DialogUtils.show_error("Error", f"Gagal membuat laporan: {str(e)}")

    def generate_full_report(self):
        report_text = "=== LAPORAN KOMPREHENSIF MINAT OLAHRAGA MAHASISWA ===\n\n"

        stats = self.current_data.get("statistics", {})
        report_text += "RINGKASAN STATISTIK:\n"
        report_text += f"- Total Mahasiswa: {stats.get('total_mahasiswa', 0)}\n"
        report_text += f"- Total Olahraga: {stats.get('total_olahraga', 0)}\n"
        report_text += f"- Total Minat: {stats.get('total_minat', 0)}\n"
        report_text += f"- Fakultas Aktif: {stats.get('fakultas_aktif', 0)}\n\n"

        sports_data = self.current_data.get("sports", [])[:5]
        if sports_data:
            report_text += "TOP 5 OLAHRAGA TERPOPULER:\n"
            for i, sport in enumerate(sports_data, 1):
                report_text += f"{i}. {sport[0]} - {sport[2]} peminat\n"

        text_widget = tk.Text(
            self.report_preview_frame,
            bg=DarkBlueTheme.get_color("bg_tertiary"),
            fg=DarkBlueTheme.get_color("text_primary"),
            font=("Consolas", 10),
            wrap=tk.WORD,
        )
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", report_text)
        text_widget.config(state="disabled")

    def generate_sports_report(self):
        sports_data = self.current_data.get("sports", [])

        report_text = "=== LAPORAN REKAP OLAHRAGA ===\n\n"

        if sports_data:
            for sport in sports_data:
                report_text += f"• {sport[0]} ({sport[1]})\n"
                report_text += f"  Peminat: {sport[2]} ({sport[3]})\n\n"
        else:
            report_text += "Tidak ada data olahraga tersedia.\n"

        text_widget = tk.Text(
            self.report_preview_frame,
            bg=DarkBlueTheme.get_color("bg_tertiary"),
            fg=DarkBlueTheme.get_color("text_primary"),
            font=("Consolas", 10),
            wrap=tk.WORD,
        )
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", report_text)
        text_widget.config(state="disabled")

    def generate_faculty_report(self):
        faculty_data = self.current_data.get("faculty", [])

        report_text = "=== LAPORAN REKAP FAKULTAS ===\n\n"

        if faculty_data:
            for faculty in faculty_data:
                report_text += f"• {faculty[0]}\n"
                report_text += f"  Mahasiswa: {faculty[1]}\n"
                report_text += f"  Total Minat: {faculty[2]}\n"
                report_text += f"  Rata-rata: {faculty[3]}\n\n"
        else:
            report_text += "Tidak ada data fakultas tersedia.\n"

        text_widget = tk.Text(
            self.report_preview_frame,
            bg=DarkBlueTheme.get_color("bg_tertiary"),
            fg=DarkBlueTheme.get_color("text_primary"),
            font=("Consolas", 10),
            wrap=tk.WORD,
        )
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", report_text)
        text_widget.config(state="disabled")

    def generate_category_report(self):
        category_data = self.current_data.get("category", [])

        report_text = "=== LAPORAN REKAP KATEGORI ===\n\n"

        if category_data:
            for category in category_data:
                report_text += f"• {category[0]}\n"
                report_text += f"  Jumlah Olahraga: {category[1]}\n"
                report_text += f"  Jumlah Peminat: {category[2]}\n"
                report_text += f"  Persentase: {category[3]}\n\n"
        else:
            report_text += "Tidak ada data kategori tersedia.\n"

        text_widget = tk.Text(
            self.report_preview_frame,
            bg=DarkBlueTheme.get_color("bg_tertiary"),
            fg=DarkBlueTheme.get_color("text_primary"),
            font=("Consolas", 10),
            wrap=tk.WORD,
        )
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", report_text)
        text_widget.config(state="disabled")

    def logout(self):
        try:
            plt.close("all")

            self.window.destroy()
            self.on_logout()
        except Exception:
            self.window.destroy()
            self.on_logout()

    def show(self):
        self.window.mainloop()

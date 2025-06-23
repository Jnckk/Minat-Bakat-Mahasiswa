import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from typing import Optional, Callable, Tuple, List
from datetime import datetime
import csv
from .theme import DarkBlueTheme


class DialogUtils:
    __slots__ = ()

    @staticmethod
    def show_success(title: str, message: str) -> None:
        messagebox.showinfo(title, message)

    @staticmethod
    def show_error(title: str, message: str) -> None:
        messagebox.showerror(title, message)

    @staticmethod
    def show_warning(title: str, message: str) -> None:
        messagebox.showwarning(title, message)

    @staticmethod
    def ask_confirmation(title: str, message: str) -> bool:
        return messagebox.askyesno(title, message)

    @staticmethod
    def ask_input(title: str, prompt: str) -> Optional[str]:
        return simpledialog.askstring(title, prompt)


class WidgetUtils:
    __slots__ = ()

    @staticmethod
    def create_styled_frame(parent, style_name: str = "frame", **kwargs) -> tk.Frame:
        style = DarkBlueTheme.get_style(style_name)
        style.update(kwargs)
        return tk.Frame(parent, **style)

    @staticmethod
    def create_styled_label(
        parent, text: str = "", style_name: str = "label", **kwargs
    ) -> tk.Label:
        style = DarkBlueTheme.get_style(style_name)
        style.update(kwargs)
        return tk.Label(parent, text=text, **style)

    @staticmethod
    def create_styled_entry(parent, style_name: str = "entry", **kwargs) -> tk.Entry:
        style = DarkBlueTheme.get_style(style_name)
        style.update(kwargs)
        entry = tk.Entry(parent, **style)

        focus_color = DarkBlueTheme.get_color("border_focus")
        normal_color = DarkBlueTheme.get_color("border_primary")

        entry.bind(
            "<FocusIn>", lambda e: entry.configure(highlightbackground=focus_color)
        )
        entry.bind(
            "<FocusOut>", lambda e: entry.configure(highlightbackground=normal_color)
        )

        return entry

    @staticmethod
    def create_styled_button(
        parent,
        text: str = "",
        command: Optional[Callable] = None,
        style_name: str = "button_primary",
        **kwargs,
    ) -> tk.Button:
        style = DarkBlueTheme.get_style(style_name)
        style.update(kwargs)

        button = tk.Button(parent, text=text, command=command, **style)

        style_type = (
            style_name.replace("button_", "") if "button_" in style_name else "primary"
        )
        DarkBlueTheme.apply_hover_effect(button, style_type)

        return button

    @staticmethod
    def create_styled_listbox(
        parent, style_name: str = "listbox", **kwargs
    ) -> tk.Listbox:
        style = DarkBlueTheme.get_style(style_name)
        style.update(kwargs)
        return tk.Listbox(parent, **style)

    @staticmethod
    def create_styled_text(parent, style_name: str = "text", **kwargs) -> tk.Text:
        style = DarkBlueTheme.get_style(style_name)
        style.update(kwargs)
        return tk.Text(parent, **style)

    @staticmethod
    def create_scrollable_frame(parent) -> Tuple[tk.Frame, tk.Canvas, tk.Scrollbar]:
        canvas = tk.Canvas(
            parent, bg=DarkBlueTheme.get_color("bg_secondary"), highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            parent,
            orient="vertical",
            command=canvas.yview,
            **DarkBlueTheme.get_style("scrollbar"),
        )
        scrollable_frame = WidgetUtils.create_styled_frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        return scrollable_frame, canvas, scrollbar

    @staticmethod
    def center_window(window, width: int, height: int) -> None:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        pos_x = (screen_width - width) // 2
        pos_y = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")


class DataUtils:
    __slots__ = ()

    @staticmethod
    def format_date(date_obj: datetime) -> str:
        return date_obj.strftime("%d/%m/%Y %H:%M")

    @staticmethod
    def format_date_short(date_obj: datetime) -> str:
        return date_obj.strftime("%d/%m/%Y")

    @staticmethod
    def capitalize_name(name: str) -> str:
        return " ".join(word.capitalize() for word in name.split())

    @staticmethod
    def clean_string(text: str) -> str:
        return text.strip() if text else ""

    @staticmethod
    def calculate_percentage(part: int, total: int) -> float:
        return (part / total * 100) if total > 0 else 0.0

    @staticmethod
    def parse_datetime(date_string: str) -> datetime:
        try:
            formats = (
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
            )

            for fmt in formats:
                try:
                    return datetime.strptime(date_string, fmt)
                except ValueError:
                    continue

            return datetime.fromisoformat(
                date_string.replace("T", " ").replace("Z", "")
            )
        except Exception:
            return datetime.now()


class ExportUtils:
    __slots__ = ()

    DEFAULT_FILETYPES = (("CSV files", "*.csv"), ("All files", "*.*"))

    @staticmethod
    def export_to_csv(
        data: List, filename: str, headers: Optional[List[str]] = None
    ) -> bool:
        try:
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if headers:
                    writer.writerow(headers)
                writer.writerows(data)
            return True
        except Exception:
            return False

    @staticmethod
    def save_file_dialog(
        default_name: str = "export.csv", filetypes: Optional[Tuple] = None
    ) -> Optional[str]:
        if not filetypes:
            filetypes = ExportUtils.DEFAULT_FILETYPES

        return filedialog.asksaveasfilename(
            defaultextension=".csv", initialvalue=default_name, filetypes=filetypes
        )

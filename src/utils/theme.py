from typing import Dict, Any, Tuple


class DarkBlueTheme:
    __slots__ = ()
    COLORS = {
        "primary": "#1E3A8A",
        "primary_light": "#3B82F6",
        "primary_dark": "#1E40AF",
        "bg_primary": "#0F172A",
        "bg_secondary": "#1E293B",
        "bg_tertiary": "#334155",
        "bg_card": "#475569",
        "text_primary": "#F8FAFC",
        "text_secondary": "#CBD5E1",
        "text_muted": "#94A3B8",
        "text_dark": "#1E293B",
        "accent_success": "#10B981",
        "accent_warning": "#F59E0B",
        "accent_error": "#EF4444",
        "accent_info": "#06B6D4",
        "btn_primary": "#3B82F6",
        "btn_primary_hover": "#2563EB",
        "btn_secondary": "#6B7280",
        "btn_secondary_hover": "#4B5563",
        "btn_success": "#10B981",
        "btn_success_hover": "#059669",
        "btn_danger": "#EF4444",
        "btn_danger_hover": "#DC2626",
        "border_primary": "#475569",
        "border_secondary": "#64748B",
        "border_focus": "#3B82F6",
        "input_bg": "#334155",
        "input_border": "#475569",
        "input_focus": "#3B82F6",
    }
    FONTS = {
        "title": ("Segoe UI", 20, "bold"),
        "heading": ("Segoe UI", 16, "bold"),
        "subheading": ("Segoe UI", 14, "bold"),
        "body": ("Segoe UI", 12),
        "body_bold": ("Segoe UI", 12, "bold"),
        "small": ("Segoe UI", 10),
        "small_bold": ("Segoe UI", 10, "bold"),
        "button": ("Segoe UI", 11, "bold"),
    }
    STYLES = {
        "window": {"bg": COLORS["bg_primary"]},
        "frame": {"bg": COLORS["bg_secondary"], "relief": "flat", "bd": 1},
        "card_frame": {
            "bg": COLORS["bg_card"],
            "relief": "raised",
            "bd": 2,
            "padx": 20,
            "pady": 15,
        },
        "label": {
            "bg": COLORS["bg_secondary"],
            "fg": COLORS["text_primary"],
            "font": FONTS["body"],
        },
        "title_label": {
            "bg": COLORS["bg_secondary"],
            "fg": COLORS["text_primary"],
            "font": FONTS["title"],
        },
        "heading_label": {
            "bg": COLORS["bg_secondary"],
            "fg": COLORS["text_primary"],
            "font": FONTS["heading"],
        },
        "entry": {
            "bg": COLORS["input_bg"],
            "fg": COLORS["text_primary"],
            "font": FONTS["body"],
            "relief": "flat",
            "bd": 2,
            "insertbackground": COLORS["text_primary"],
            "selectbackground": COLORS["primary"],
            "selectforeground": COLORS["text_primary"],
        },
        "button_primary": {
            "bg": COLORS["btn_primary"],
            "fg": COLORS["text_primary"],
            "font": FONTS["button"],
            "relief": "flat",
            "bd": 0,
            "pady": 8,
            "padx": 20,
            "cursor": "hand2",
        },
        "button_secondary": {
            "bg": COLORS["btn_secondary"],
            "fg": COLORS["text_primary"],
            "font": FONTS["button"],
            "relief": "flat",
            "bd": 0,
            "pady": 8,
            "padx": 20,
            "cursor": "hand2",
        },
        "button_success": {
            "bg": COLORS["btn_success"],
            "fg": COLORS["text_primary"],
            "font": FONTS["button"],
            "relief": "flat",
            "bd": 0,
            "pady": 8,
            "padx": 20,
            "cursor": "hand2",
        },
        "button_danger": {
            "bg": COLORS["btn_danger"],
            "fg": COLORS["text_primary"],
            "font": FONTS["button"],
            "relief": "flat",
            "bd": 0,
            "pady": 8,
            "padx": 20,
            "cursor": "hand2",
        },
        "listbox": {
            "bg": COLORS["input_bg"],
            "fg": COLORS["text_primary"],
            "font": FONTS["body"],
            "relief": "flat",
            "bd": 2,
            "selectbackground": COLORS["primary"],
            "selectforeground": COLORS["text_primary"],
            "activestyle": "none",
        },
        "text": {
            "bg": COLORS["input_bg"],
            "fg": COLORS["text_primary"],
            "font": FONTS["body"],
            "relief": "flat",
            "bd": 2,
            "insertbackground": COLORS["text_primary"],
            "selectbackground": COLORS["primary"],
            "selectforeground": COLORS["text_primary"],
        },
        "scrollbar": {
            "bg": COLORS["bg_tertiary"],
            "troughcolor": COLORS["bg_secondary"],
            "activebackground": COLORS["primary"],
            "relief": "flat",
            "bd": 0,
            "width": 12,
        },
    }
    HOVER_COLORS = {
        "primary": ("#2563EB", "#3B82F6"),
        "secondary": ("#4B5563", "#6B7280"),
        "success": ("#059669", "#10B981"),
        "danger": ("#DC2626", "#EF4444"),
    }

    @classmethod
    def get_color(cls, color_name: str) -> str:
        return cls.COLORS.get(color_name, "#FFFFFF")

    @classmethod
    def get_font(cls, font_name: str) -> Tuple[str, int, str]:
        return cls.FONTS.get(font_name, ("Segoe UI", 12))

    @classmethod
    def get_style(cls, style_name: str) -> Dict[str, Any]:
        return cls.STYLES.get(style_name, {}).copy()

    @classmethod
    def apply_hover_effect(cls, widget, style_type: str = "primary") -> None:
        colors = cls.HOVER_COLORS.get(style_type)
        if not colors:
            return

        hover_color, normal_color = colors

        widget.bind("<Enter>", lambda e: widget.configure(bg=hover_color))
        widget.bind("<Leave>", lambda e: widget.configure(bg=normal_color))

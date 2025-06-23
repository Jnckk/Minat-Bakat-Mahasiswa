import re
from typing import Tuple


class ValidationUtils:
    __slots__ = ()
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    NAME_PATTERN = re.compile(r"^[a-zA-Z\s]+$")
    DANGEROUS_CHARS = frozenset("<>\"'&%;()+-")
    VALID_CATEGORIES = frozenset(("individual", "tim"))

    @staticmethod
    def validate_nim(nim: str) -> bool:
        return bool(nim and 8 <= len(nim) <= 15 and nim.isdigit())

    @staticmethod
    def validate_pic(pic: str) -> bool:
        return bool(pic and 6 <= len(pic) <= 20 and pic.isalnum())

    @staticmethod
    def validate_name(name: str) -> bool:
        if not name:
            return False
        name = name.strip()
        return len(name) >= 2 and ValidationUtils.NAME_PATTERN.match(name) is not None

    @staticmethod
    def validate_fakultas(fakultas: str) -> bool:
        return bool(fakultas and len(fakultas.strip()) >= 2)

    @staticmethod
    def validate_olahraga_name(name: str) -> bool:
        return bool(name and len(name.strip()) >= 2)

    @staticmethod
    def validate_kategori(kategori: str) -> bool:
        return bool(
            kategori and kategori.strip().lower() in ValidationUtils.VALID_CATEGORIES
        )

    @staticmethod
    def validate_email(email: str) -> bool:
        return bool(email and ValidationUtils.EMAIL_PATTERN.match(email))

    @staticmethod
    def validate_password(password: str) -> bool:
        return bool(password and len(password) >= 6)

    @staticmethod
    def sanitize_input(text: str) -> str:
        if not text:
            return ""
        text = text.strip()
        return "".join(
            char for char in text if char not in ValidationUtils.DANGEROUS_CHARS
        )

    @staticmethod
    def validate_required_field(value: str, field_name: str) -> Tuple[bool, str]:
        if not value or not value.strip():
            return False, f"{field_name} tidak boleh kosong"
        return True, ""

    @staticmethod
    def validate_length(
        value: str, min_length: int, max_length: int, field_name: str
    ) -> Tuple[bool, str]:
        length = len(value)
        if length < min_length:
            return False, f"{field_name} minimal {min_length} karakter"
        if length > max_length:
            return False, f"{field_name} maksimal {max_length} karakter"
        return True, ""

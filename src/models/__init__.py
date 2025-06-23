"""
Production models package
"""

from .user import User, Mahasiswa, Admin, Kemahasiswaan
from .minat_bakat import MinatBakat
from .olahraga import Olahraga
from .rekap import Rekap

__all__ = (
    "User",
    "Mahasiswa",
    "Admin",
    "Kemahasiswaan",
    "MinatBakat",
    "Olahraga",
    "Rekap",
)

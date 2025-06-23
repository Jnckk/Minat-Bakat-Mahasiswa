from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from ..config.database import db_config


class User(ABC):
    """Base User class for production"""

    __slots__ = ("username", "password", "role", "is_logged_in")

    def __init__(self, username: str, password: str, role: str):
        self.username = username
        self.password = password
        self.role = role
        self.is_logged_in = False

    @abstractmethod
    def login(self) -> bool:
        """Abstract login method"""
        pass

    def logout(self) -> None:
        """Logout user"""
        self.is_logged_in = False


class Mahasiswa(User):
    """Optimized Mahasiswa class for production"""

    __slots__ = ("nim", "nama", "pic", "fakultas", "user_id")

    def __init__(
        self,
        username: str = "",
        password: str = "",
        nim: str = "",
        nama: str = "",
        pic: str = "",
        fakultas: str = "",
    ):
        super().__init__(username, password, "mahasiswa")
        self.nim = nim
        self.nama = nama
        self.pic = pic
        self.fakultas = fakultas
        self.user_id: Optional[int] = None

    def login(self) -> bool:
        """Login mahasiswa using NIM and PIC"""
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT m.*, u.id as user_id, u.username 
                    FROM mahasiswa m 
                    JOIN users u ON m.user_id = u.id 
                    WHERE m.nim = ? AND m.pic = ?
                """,
                    (self.nim, self.pic),
                )

                result = cursor.fetchone()
                if result:
                    self.user_id = result["user_id"]
                    self.username = result["username"]
                    self.nama = result["nama"]
                    self.fakultas = result["fakultas"]
                    self.is_logged_in = True
                    return True
                return False
        except Exception:
            return False

    def pilih_minat_olahraga(self, olahraga_id: int) -> bool:
        """Select sport interest"""
        if not self.is_logged_in:
            return False

        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT id FROM minat_bakat 
                    WHERE mahasiswa_nim = ? AND olahraga_id = ?
                """,
                    (self.nim, olahraga_id),
                )

                if cursor.fetchone():
                    return False

                conn.execute(
                    """
                    INSERT INTO minat_bakat (mahasiswa_nim, olahraga_id) 
                    VALUES (?, ?)
                """,
                    (self.nim, olahraga_id),
                )

                conn.commit()
                return True
        except Exception:
            return False

    def hapus_minat_olahraga(self, olahraga_id: int) -> bool:
        """Hapus minat olahraga yang dipilih"""
        if not self.is_logged_in:
            return False
        try:
            with db_config.get_connection() as conn:
                conn.execute(
                    "DELETE FROM minat_bakat WHERE mahasiswa_nim = ? AND olahraga_id = ?",
                    (self.nim, olahraga_id),
                )
                conn.commit()
                return True
        except Exception:
            return False

    def get_minat_olahraga(self) -> list:
        """Get selected sports"""
        if not self.is_logged_in:
            return []

        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT o.*, mb.tanggal_input 
                    FROM minat_bakat mb 
                    JOIN olahraga o ON mb.olahraga_id = o.id 
                    WHERE mb.mahasiswa_nim = ?
                """,
                    (self.nim,),
                )

                return cursor.fetchall()
        except Exception:
            return []

    @staticmethod
    def register(
        nim: str, nama: str, pic: str, fakultas: str, password: str = None
    ) -> bool:
        """Register new mahasiswa"""
        if not password:
            password = pic

        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO users (username, password, role) 
                    VALUES (?, ?, 'mahasiswa')
                """,
                    (nim, password),
                )

                user_id = cursor.lastrowid

                conn.execute(
                    """
                    INSERT INTO mahasiswa (user_id, nim, nama, pic, fakultas) 
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (user_id, nim, nama, pic, fakultas),
                )

                conn.commit()
                return True
        except Exception:
            return False

    @staticmethod
    def create(
        nim: str, nama: str, pic: str, fakultas: str, password: str
    ) -> Optional["Mahasiswa"]:
        """Create new mahasiswa with user account"""
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute("SELECT id FROM mahasiswa WHERE nim = ?", (nim,))
                if cursor.fetchone():
                    return None

                cursor = conn.execute(
                    """
                    INSERT INTO users (username, password, role) 
                    VALUES (?, ?, 'mahasiswa')
                """,
                    (nim, password),
                )

                user_id = cursor.lastrowid

                conn.execute(
                    """
                    INSERT INTO mahasiswa (user_id, nim, nama, pic, fakultas) 
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (user_id, nim, nama, pic, fakultas),
                )

                mahasiswa = Mahasiswa(nim, password, nim, nama, pic, fakultas)
                mahasiswa.user_id = user_id
                return mahasiswa

        except Exception:
            return None

    @staticmethod
    def get_by_nim(nim: str) -> Optional["Mahasiswa"]:
        """Get mahasiswa by NIM"""
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT m.*, u.username, u.password 
                    FROM mahasiswa m 
                    JOIN users u ON m.user_id = u.id 
                    WHERE m.nim = ?
                """,
                    (nim,),
                )

                row = cursor.fetchone()
                if row:
                    mahasiswa = Mahasiswa(
                        username=row["username"],
                        password=row["password"],
                        nim=row["nim"],
                        nama=row["nama"],
                        pic=row["pic"],
                        fakultas=row["fakultas"],
                    )
                    mahasiswa.user_id = row["user_id"]
                    return mahasiswa

                return None

        except Exception:
            return None

    @staticmethod
    def get_all() -> list["Mahasiswa"]:
        """Fetch all mahasiswa from the database."""
        mahasiswa_list = []
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT m.*, u.username, u.password, u.id as user_id
                    FROM mahasiswa m
                    JOIN users u ON m.user_id = u.id
                    ORDER BY m.nama ASC
                    """
                )
                rows = cursor.fetchall()
                for row in rows:
                    mhs = Mahasiswa(
                        username=row["username"],
                        password=row["password"],
                        nim=row["nim"],
                        nama=row["nama"],
                        pic=row["pic"],
                        fakultas=row["fakultas"],
                    )
                    mhs.user_id = row["user_id"]
                    mahasiswa_list.append(mhs)
            return mahasiswa_list
        except Exception as e:
            return []

    @staticmethod
    def update_by_nim(nim: str, nama: str, fakultas: str, pic: str) -> bool:
        """Update mahasiswa data by NIM"""
        try:
            with db_config.get_connection() as conn:
                conn.execute(
                    """
                    UPDATE mahasiswa SET nama = ?, fakultas = ?, pic = ? WHERE nim = ?
                    """,
                    (nama, fakultas, pic, nim),
                )
                conn.commit()
                return True
        except Exception:
            return False

    @staticmethod
    def delete_by_nim(nim: str) -> bool:
        """Delete mahasiswa by NIM (and user account)"""
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT user_id FROM mahasiswa WHERE nim = ?", (nim,)
                )
                row = cursor.fetchone()
                if not row:
                    return False
                user_id = row["user_id"]
                conn.execute("DELETE FROM mahasiswa WHERE nim = ?", (nim,))
                conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                return True
        except Exception:
            return False


class Admin(User):
    """Optimized Admin class for production"""

    __slots__ = ("admin_id", "nama", "user_id")

    def __init__(
        self, username: str = "", password: str = "", admin_id: str = "", nama: str = ""
    ):
        super().__init__(username, password, "admin")
        self.admin_id = admin_id
        self.nama = nama
        self.user_id: Optional[int] = None

    def login(self) -> bool:
        """Login admin"""
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT a.*, u.id as user_id 
                    FROM admin a 
                    JOIN users u ON a.user_id = u.id 
                    WHERE u.username = ? AND u.password = ?
                """,
                    (self.username, self.password),
                )

                result = cursor.fetchone()
                if result:
                    self.user_id = result["user_id"]
                    self.admin_id = result["admin_id"]
                    self.nama = result["nama"]
                    self.is_logged_in = True
                    return True
                return False
        except Exception:
            return False

    def input_data_minat_bakat(self, nim: str, olahraga_id: int) -> bool:
        """Input sport interest data"""
        if not self.is_logged_in:
            return False

        try:
            with db_config.get_connection() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO minat_bakat (mahasiswa_nim, olahraga_id) 
                    VALUES (?, ?)
                """,
                    (nim, olahraga_id),
                )

                conn.commit()
                return True
        except Exception:
            return False

    def lihat_rekap_data(self) -> Dict[str, Any]:
        """View comprehensive data recap"""
        if not self.is_logged_in:
            return {}

        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT o.nama_olahraga, o.kategori, COUNT(mb.id) as jumlah_peminat
                    FROM olahraga o 
                    LEFT JOIN minat_bakat mb ON o.id = mb.olahraga_id 
                    GROUP BY o.id, o.nama_olahraga, o.kategori
                    ORDER BY jumlah_peminat DESC
                """
                )

                sports_data = cursor.fetchall()

                cursor = conn.execute("SELECT COUNT(*) as total FROM mahasiswa")
                total_mahasiswa = cursor.fetchone()["total"]

                cursor = conn.execute("SELECT COUNT(*) as total FROM minat_bakat")
                total_minat = cursor.fetchone()["total"]

                return {
                    "sports_data": sports_data,
                    "total_mahasiswa": total_mahasiswa,
                    "total_minat": total_minat,
                }
        except Exception:
            return {}

    def get_dashboard_statistics(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        if not self.is_logged_in:
            return {}

        try:
            with db_config.get_connection() as conn:
                stats = {}

                cursor = conn.execute("SELECT COUNT(*) as count FROM mahasiswa")
                stats["total_mahasiswa"] = cursor.fetchone()["count"]

                cursor = conn.execute("SELECT COUNT(*) as count FROM olahraga")
                stats["total_olahraga"] = cursor.fetchone()["count"]

                cursor = conn.execute("SELECT COUNT(*) as count FROM minat_bakat")
                stats["total_minat"] = cursor.fetchone()["count"]

                cursor = conn.execute(
                    "SELECT COUNT(DISTINCT fakultas) as count FROM mahasiswa"
                )
                stats["fakultas_aktif"] = cursor.fetchone()["count"]

                return stats
        except Exception:
            return {
                "total_mahasiswa": 0,
                "total_olahraga": 0,
                "total_minat": 0,
                "fakultas_aktif": 0,
            }

    def lihat_rekap_fakultas(self) -> Dict[str, Any]:
        """View faculty-based recap"""
        if not self.is_logged_in:
            return {}

        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT 
                        m.fakultas,
                        COUNT(DISTINCT m.id) as jumlah_mahasiswa,
                        COUNT(mb.id) as jumlah_minat,
                        ROUND(CAST(COUNT(mb.id) AS FLOAT) / COUNT(DISTINCT m.id), 2) as rata_rata
                    FROM mahasiswa m 
                    LEFT JOIN minat_bakat mb ON m.id = mb.mahasiswa_id 
                    GROUP BY m.fakultas
                    ORDER BY jumlah_mahasiswa DESC
                """
                )

                return {
                    "faculty_data": [
                        [
                            row["fakultas"],
                            row["jumlah_mahasiswa"],
                            row["jumlah_minat"],
                            f"{row['rata_rata']:.2f}",
                        ]
                        for row in cursor.fetchall()
                    ]
                }
        except Exception:
            return {}

    def lihat_rekap_kategori(self) -> Dict[str, Any]:
        """View category-based recap"""
        if not self.is_logged_in:
            return {}

        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT 
                        o.kategori,
                        COUNT(DISTINCT o.id) as jumlah_olahraga,
                        COUNT(mb.id) as jumlah_peminat,
                        ROUND(CAST(COUNT(mb.id) AS FLOAT) / 
                              (SELECT COUNT(*) FROM minat_bakat) * 100, 1) as persentase
                    FROM olahraga o 
                    LEFT JOIN minat_bakat mb ON o.id = mb.olahraga_id 
                    GROUP BY o.kategori
                    ORDER BY jumlah_peminat DESC
                """
                )

                return {
                    "category_data": [
                        [
                            row["kategori"],
                            row["jumlah_olahraga"],
                            row["jumlah_peminat"],
                            f"{row['persentase']}%",
                        ]
                        for row in cursor.fetchall()
                    ]
                }
        except Exception:
            return {}


class Kemahasiswaan(User):
    """Optimized Kemahasiswaan class for production"""

    __slots__ = ("kemahasiswaan_id", "nama", "user_id")

    def __init__(
        self,
        username: str = "",
        password: str = "",
        kemahasiswaan_id: str = "",
        nama: str = "",
    ):
        super().__init__(username, password, "kemahasiswaan")
        self.kemahasiswaan_id = kemahasiswaan_id
        self.nama = nama
        self.user_id: Optional[int] = None

    def login(self) -> bool:
        """Login kemahasiswaan"""
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT k.*, u.id as user_id 
                    FROM kemahasiswaan k 
                    JOIN users u ON k.user_id = u.id 
                    WHERE u.username = ? AND u.password = ?
                """,
                    (self.username, self.password),
                )

                result = cursor.fetchone()
                if result:
                    self.user_id = result["user_id"]
                    self.kemahasiswaan_id = result["kemahasiswaan_id"]
                    self.nama = result["nama"]
                    self.is_logged_in = True
                    return True
                return False
        except Exception:
            return False

    def lihat_rekap_olahraga(self) -> Dict[str, Any]:
        """View sports recap"""
        if not self.is_logged_in:
            return {}

        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT 
                        o.nama_olahraga, 
                        o.kategori, 
                        COUNT(mb.id) as jumlah_peminat,
                        ROUND(CAST(COUNT(mb.id) AS FLOAT) / 
                              (SELECT COUNT(*) FROM minat_bakat) * 100, 1) as persentase
                    FROM olahraga o 
                    LEFT JOIN minat_bakat mb ON o.id = mb.olahraga_id 
                    GROUP BY o.id, o.nama_olahraga, o.kategori
                    ORDER BY jumlah_peminat DESC
                """
                )

                return {
                    "sports_data": [
                        [
                            row["nama_olahraga"],
                            row["kategori"],
                            row["jumlah_peminat"],
                            f"{row['persentase']}%",
                        ]
                        for row in cursor.fetchall()
                    ]
                }
        except Exception:
            return {}

    def get_dashboard_statistics(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        if not self.is_logged_in:
            return {}

        try:
            with db_config.get_connection() as conn:
                stats = {}

                cursor = conn.execute("SELECT COUNT(*) as count FROM mahasiswa")
                stats["total_mahasiswa"] = cursor.fetchone()["count"]

                cursor = conn.execute("SELECT COUNT(*) as count FROM olahraga")
                stats["total_olahraga"] = cursor.fetchone()["count"]

                cursor = conn.execute("SELECT COUNT(*) as count FROM minat_bakat")
                stats["total_minat"] = cursor.fetchone()["count"]

                cursor = conn.execute(
                    "SELECT COUNT(DISTINCT fakultas) as count FROM mahasiswa"
                )
                stats["fakultas_aktif"] = cursor.fetchone()["count"]

                return stats
        except Exception:
            return {
                "total_mahasiswa": 0,
                "total_olahraga": 0,
                "total_minat": 0,
                "fakultas_aktif": 0,
            }

    def lihat_rekap_fakultas(self) -> Dict[str, Any]:
        """View faculty-based recap"""
        if not self.is_logged_in:
            return {}

        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT 
                        m.fakultas,
                        COUNT(DISTINCT m.id) as jumlah_mahasiswa,
                        COUNT(mb.id) as jumlah_minat,
                        ROUND(CAST(COUNT(mb.id) AS FLOAT) / COUNT(DISTINCT m.id), 2) as rata_rata
                    FROM mahasiswa m 
                    LEFT JOIN minat_bakat mb ON m.nim = mb.mahasiswa_nim
                    GROUP BY m.fakultas
                    ORDER BY jumlah_mahasiswa DESC
                """
                )

                return {
                    "faculty_data": [
                        [
                            row["fakultas"],
                            row["jumlah_mahasiswa"],
                            row["jumlah_minat"],
                            f"{row['rata_rata']:.2f}",
                        ]
                        for row in cursor.fetchall()
                    ]
                }
        except Exception:
            return {}

    def lihat_rekap_kategori(self) -> Dict[str, Any]:
        """View category-based recap"""
        if not self.is_logged_in:
            return {}

        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT 
                        o.kategori,
                        COUNT(DISTINCT o.id) as jumlah_olahraga,
                        COUNT(mb.id) as jumlah_peminat,
                        ROUND(CAST(COUNT(mb.id) AS FLOAT) / 
                              (SELECT COUNT(*) FROM minat_bakat) * 100, 1) as persentase
                    FROM olahraga o 
                    LEFT JOIN minat_bakat mb ON o.id = mb.olahraga_id 
                    GROUP BY o.kategori
                    ORDER BY jumlah_peminat DESC
                """
                )

                return {
                    "category_data": [
                        [
                            row["kategori"],
                            row["jumlah_olahraga"],
                            row["jumlah_peminat"],
                            f"{row['persentase']}%",
                        ]
                        for row in cursor.fetchall()
                    ]
                }
        except Exception:
            return {}

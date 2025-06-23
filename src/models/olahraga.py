from typing import Optional, List, Dict, Any
from ..config.database import db_config


class Olahraga:
    __slots__ = ("id", "nama_olahraga", "kategori", "deskripsi")

    def __init__(
        self,
        id: Optional[int] = None,
        nama_olahraga: str = "",
        kategori: str = "",
        deskripsi: str = "",
    ):
        self.id = id
        self.nama_olahraga = nama_olahraga
        self.kategori = kategori
        self.deskripsi = deskripsi

    def tambah_olahraga(self) -> bool:
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO olahraga (nama_olahraga, kategori, deskripsi) 
                    VALUES (?, ?, ?)
                """,
                    (self.nama_olahraga, self.kategori, self.deskripsi),
                )

                self.id = cursor.lastrowid
                conn.commit()
                return True
        except Exception:
            return False

    def hapus_olahraga(self) -> bool:
        if self.id is None:
            return False
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT COUNT(*) as count FROM minat_bakat WHERE olahraga_id = ?
                """,
                    (self.id,),
                )
                if cursor.fetchone()["count"] > 0:
                    return False
                conn.execute("DELETE FROM olahraga WHERE id = ?", (self.id,))
                conn.commit()
                return True
        except Exception:
            return False

    def update_olahraga(
        self, nama_olahraga: str, kategori: str, deskripsi: str
    ) -> bool:
        if self.id is None:
            return False
        try:
            with db_config.get_connection() as conn:
                conn.execute(
                    """
                    UPDATE olahraga 
                    SET nama_olahraga = ?, kategori = ?, deskripsi = ? 
                    WHERE id = ?
                """,
                    (nama_olahraga, kategori, deskripsi, self.id),
                )
                self.nama_olahraga = nama_olahraga
                self.kategori = kategori
                self.deskripsi = deskripsi
                conn.commit()
                return True
        except Exception:
            return False

    @staticmethod
    def get_all() -> List["Olahraga"]:
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT * FROM olahraga ORDER BY nama_olahraga
                """
                )
                return [
                    Olahraga(
                        id=row["id"],
                        nama_olahraga=row["nama_olahraga"],
                        kategori=row["kategori"],
                        deskripsi=row["deskripsi"],
                    )
                    for row in cursor.fetchall()
                ]
        except Exception:
            return []

    @staticmethod
    def get_by_id(olahraga_id: int) -> Optional["Olahraga"]:
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT * FROM olahraga WHERE id = ?
                """,
                    (olahraga_id,),
                )
                row = cursor.fetchone()
                if row:
                    return Olahraga(
                        id=row["id"],
                        nama_olahraga=row["nama_olahraga"],
                        kategori=row["kategori"],
                        deskripsi=row["deskripsi"],
                    )
                return None
        except Exception:
            return None

    @staticmethod
    def get_with_statistics() -> List[Dict[str, Any]]:
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT o.*, COUNT(mb.id) as jumlah_peminat
                    FROM olahraga o 
                    LEFT JOIN minat_bakat mb ON o.id = mb.olahraga_id 
                    GROUP BY o.id, o.nama_olahraga, o.kategori, o.deskripsi
                    ORDER BY jumlah_peminat DESC, o.nama_olahraga
                """
                )
                return cursor.fetchall()
        except Exception:
            return []

    @staticmethod
    def get_categories() -> List[str]:
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT DISTINCT kategori FROM olahraga ORDER BY kategori
                """
                )
                return [row["kategori"] for row in cursor.fetchall()]
        except Exception:
            return []

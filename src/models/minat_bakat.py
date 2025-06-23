from typing import Optional, List, Dict, Any
from datetime import datetime
from ..config.database import db_config


class MinatBakat:
    __slots__ = ("id", "mahasiswa_nim", "olahraga_id", "tanggal_input")

    def __init__(
        self,
        id: Optional[int] = None,
        mahasiswa_nim: str = "",
        olahraga_id: int = 0,
        tanggal_input: Optional[datetime] = None,
    ):
        self.id = id
        self.mahasiswa_nim = mahasiswa_nim
        self.olahraga_id = olahraga_id
        self.tanggal_input = tanggal_input or datetime.now()

    def simpan_data(self) -> bool:
        try:
            with db_config.get_connection() as conn:
                if self.id is None:
                    cursor = conn.execute(
                        """
                        INSERT INTO minat_bakat (mahasiswa_nim, olahraga_id, tanggal_input) 
                        VALUES (?, ?, ?)
                    """,
                        (self.mahasiswa_nim, self.olahraga_id, self.tanggal_input),
                    )
                    self.id = cursor.lastrowid
                else:
                    conn.execute(
                        """
                        UPDATE minat_bakat 
                        SET olahraga_id = ?, tanggal_input = ? 
                        WHERE id = ?
                    """,
                        (self.olahraga_id, self.tanggal_input, self.id),
                    )
                conn.commit()
                return True
        except Exception:
            return False

    def update_data(self, olahraga_id: int) -> bool:
        if self.id is None:
            return False
        self.olahraga_id = olahraga_id
        self.tanggal_input = datetime.now()
        return self.simpan_data()

    @staticmethod
    def get_by_mahasiswa(nim: str) -> List["MinatBakat"]:
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT * FROM minat_bakat WHERE mahasiswa_nim = ?
                """,
                    (nim,),
                )
                return [
                    MinatBakat(
                        id=row["id"],
                        mahasiswa_nim=row["mahasiswa_nim"],
                        olahraga_id=row["olahraga_id"],
                        tanggal_input=datetime.fromisoformat(row["tanggal_input"]),
                    )
                    for row in cursor.fetchall()
                ]
        except Exception:
            return []

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT mb.*, m.nama as mahasiswa_nama, m.fakultas, 
                           o.nama_olahraga, o.kategori
                    FROM minat_bakat mb
                    JOIN mahasiswa m ON mb.mahasiswa_nim = m.nim
                    JOIN olahraga o ON mb.olahraga_id = o.id
                    ORDER BY mb.tanggal_input DESC
                """
                )
                return cursor.fetchall()
        except Exception:
            return []

    @staticmethod
    def delete_by_id(minat_id: int) -> bool:
        try:
            with db_config.get_connection() as conn:
                conn.execute("DELETE FROM minat_bakat WHERE id = ?", (minat_id,))
                conn.commit()
                return True
        except Exception:
            return False

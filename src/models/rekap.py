from typing import Optional, List, Dict, Any
from datetime import datetime
import json
from ..config.database import db_config


class Rekap:
    __slots__ = ("id", "jenis_rekap", "tanggal_rekap", "jumlah_data", "detail_data")

    def __init__(
        self,
        id: Optional[int] = None,
        jenis_rekap: str = "",
        tanggal_rekap: Optional[datetime] = None,
        jumlah_data: int = 0,
        detail_data: str = "",
    ):
        self.id = id
        self.jenis_rekap = jenis_rekap
        self.tanggal_rekap = tanggal_rekap or datetime.now()
        self.jumlah_data = jumlah_data
        self.detail_data = detail_data

    def generate_rekap(self, jenis: str = "olahraga") -> Dict[str, Any]:
        try:
            with db_config.get_connection() as conn:
                generators = {
                    "olahraga": self._generate_rekap_olahraga,
                    "fakultas": self._generate_rekap_fakultas,
                    "kategori": self._generate_rekap_kategori,
                }
                generator = generators.get(jenis)
                return generator(conn) if generator else {}
        except Exception:
            return {}

    def _generate_rekap_olahraga(self, conn) -> Dict[str, Any]:
        cursor = conn.execute(
            """
            SELECT o.nama_olahraga, o.kategori, COUNT(mb.id) as jumlah_peminat,
                   ROUND(COUNT(mb.id) * 100.0 / (SELECT COUNT(*) FROM minat_bakat), 2) as persentase
            FROM olahraga o 
            LEFT JOIN minat_bakat mb ON o.id = mb.olahraga_id 
            GROUP BY o.id, o.nama_olahraga, o.kategori
            ORDER BY jumlah_peminat DESC
        """
        )
        data = cursor.fetchall()
        total_minat = sum(row["jumlah_peminat"] for row in data)
        return {
            "jenis": "olahraga",
            "data": data,
            "total": total_minat,
            "tanggal": datetime.now().isoformat(),
        }

    def _generate_rekap_fakultas(self, conn) -> Dict[str, Any]:
        cursor = conn.execute(
            """
            SELECT m.fakultas, COUNT(mb.id) as jumlah_minat,
                   COUNT(DISTINCT m.nim) as jumlah_mahasiswa
            FROM mahasiswa m 
            LEFT JOIN minat_bakat mb ON m.nim = mb.mahasiswa_nim 
            GROUP BY m.fakultas
            ORDER BY jumlah_minat DESC
        """
        )
        return {
            "jenis": "fakultas",
            "data": cursor.fetchall(),
            "tanggal": datetime.now().isoformat(),
        }

    def _generate_rekap_kategori(self, conn) -> Dict[str, Any]:
        cursor = conn.execute(
            """
            SELECT o.kategori, COUNT(mb.id) as jumlah_peminat,
                   COUNT(DISTINCT o.id) as jumlah_olahraga
            FROM olahraga o 
            LEFT JOIN minat_bakat mb ON o.id = mb.olahraga_id 
            GROUP BY o.kategori
            ORDER BY jumlah_peminat DESC
        """
        )
        return {
            "jenis": "kategori",
            "data": cursor.fetchall(),
            "tanggal": datetime.now().isoformat(),
        }

    def tampilkan_data(self) -> Dict[str, Any]:
        if self.detail_data:
            try:
                return json.loads(self.detail_data)
            except json.JSONDecodeError:
                return {}
        return {}

    def simpan_rekap(self, rekap_data: Dict[str, Any]) -> bool:
        try:
            self.jenis_rekap = rekap_data.get("jenis", "")
            self.jumlah_data = len(rekap_data.get("data", []))
            self.detail_data = json.dumps(rekap_data)
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO rekap (jenis_rekap, tanggal_rekap, jumlah_data, detail_data) 
                    VALUES (?, ?, ?, ?)
                """,
                    (
                        self.jenis_rekap,
                        self.tanggal_rekap,
                        self.jumlah_data,
                        self.detail_data,
                    ),
                )
                self.id = cursor.lastrowid
                conn.commit()
                return True
        except Exception:
            return False

    @staticmethod
    def get_all() -> List["Rekap"]:
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT * FROM rekap ORDER BY tanggal_rekap DESC
                """
                )
                return [
                    Rekap(
                        id=row["id"],
                        jenis_rekap=row["jenis_rekap"],
                        tanggal_rekap=datetime.fromisoformat(row["tanggal_rekap"]),
                        jumlah_data=row["jumlah_data"],
                        detail_data=row["detail_data"],
                    )
                    for row in cursor.fetchall()
                ]
        except Exception:
            return []

    @staticmethod
    def get_latest_by_type(jenis_rekap: str) -> Optional["Rekap"]:
        try:
            with db_config.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT * FROM rekap 
                    WHERE jenis_rekap = ? 
                    ORDER BY tanggal_rekap DESC 
                    LIMIT 1
                """,
                    (jenis_rekap,),
                )
                row = cursor.fetchone()
                if row:
                    return Rekap(
                        id=row["id"],
                        jenis_rekap=row["jenis_rekap"],
                        tanggal_rekap=datetime.fromisoformat(row["tanggal_rekap"]),
                        jumlah_data=row["jumlah_data"],
                        detail_data=row["detail_data"],
                    )
                return None
        except Exception:
            return None

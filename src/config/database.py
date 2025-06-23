import sqlite3
import os


class DatabaseConfig:
    """Optimized database configuration for production"""

    __slots__ = ("db_path",)

    def __init__(self, db_path: str = "data/sports_management.db"):
        self.db_path = db_path
        self._ensure_db_directory()

    def _ensure_db_directory(self) -> None:
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        return conn

    def init_database(self) -> None:
        with self.get_connection() as conn:
            self._create_tables(conn)
            self._insert_default_data(conn)

    def _create_tables(self, conn: sqlite3.Connection) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('mahasiswa', 'admin', 'kemahasiswaan')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mahasiswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                nim TEXT UNIQUE NOT NULL,
                nama TEXT NOT NULL,
                pic TEXT NOT NULL,
                fakultas TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                admin_id TEXT UNIQUE NOT NULL,
                nama TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS kemahasiswaan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                kemahasiswaan_id TEXT UNIQUE NOT NULL,
                nama TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS olahraga (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_olahraga TEXT UNIQUE NOT NULL,
                kategori TEXT NOT NULL,
                deskripsi TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS minat_bakat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mahasiswa_nim TEXT NOT NULL,
                olahraga_id INTEGER NOT NULL,
                tanggal_input TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (mahasiswa_nim) REFERENCES mahasiswa(nim) ON DELETE CASCADE,
                FOREIGN KEY (olahraga_id) REFERENCES olahraga(id) ON DELETE CASCADE,
                UNIQUE(mahasiswa_nim, olahraga_id)
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rekap (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jenis_rekap TEXT NOT NULL,
                tanggal_rekap TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                jumlah_data INTEGER NOT NULL,
                detail_data TEXT
            )
        """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_mahasiswa_nim ON mahasiswa(nim)")
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_minat_bakat_mahasiswa ON minat_bakat(mahasiswa_nim)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_minat_bakat_olahraga ON minat_bakat(olahraga_id)"
        )

    def _insert_default_data(self, conn: sqlite3.Connection) -> None:
        cursor = conn.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 0:
            return
        cursor = conn.execute(
            """
            INSERT INTO users (username, password, role) 
            VALUES ('admin', 'admin123', 'admin')
        """
        )
        admin_user_id = cursor.lastrowid
        conn.execute(
            """
            INSERT INTO admin (user_id, admin_id, nama) 
            VALUES (?, 'ADM001', 'Administrator')
        """,
            (admin_user_id,),
        )
        cursor = conn.execute(
            """
            INSERT INTO users (username, password, role) 
            VALUES ('kemahasiswaan', 'kemahasiswaan123', 'kemahasiswaan')
        """
        )
        kemahasiswaan_user_id = cursor.lastrowid
        conn.execute(
            """
            INSERT INTO kemahasiswaan (user_id, kemahasiswaan_id, nama) 
            VALUES (?, 'KMH001', 'Bagian Kemahasiswaan')
        """,
            (kemahasiswaan_user_id,),
        )
        olahraga_data = (
            ("Sepak Bola", "Tim", "Olahraga tim dengan bola"),
            ("Basket", "Tim", "Olahraga bola basket"),
            ("Voli", "Tim", "Olahraga voli"),
            ("Badminton", "Individual", "Olahraga raket"),
            ("Tenis Meja", "Individual", "Ping pong"),
            ("Renang", "Individual", "Olahraga air"),
            ("Lari", "Individual", "Atletik lari"),
            ("Futsal", "Tim", "Sepak bola indoor"),
            ("Catur", "Individual", "Olahraga pikiran"),
            ("Karate", "Individual", "Bela diri"),
        )
        conn.executemany(
            """
            INSERT INTO olahraga (nama_olahraga, kategori, deskripsi) 
            VALUES (?, ?, ?)
        """,
            olahraga_data,
        )
        conn.commit()


db_config = DatabaseConfig()

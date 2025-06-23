# Sistem Manajemen Minat Olahraga Mahasiswa

**Version 2.0.0** | _by Yusuf Wibisono_

Aplikasi desktop berbasis Python dengan GUI tkinter untuk mengelola minat olahraga mahasiswa di lingkungan perguruan tinggi. Sistem ini menggunakan arsitektur Model-View-Controller (MVC) dengan tema dark blue yang modern dan user-friendly.

## 🎯 Fitur Utama

### 🎓 Untuk Mahasiswa

- **Registrasi mandiri** dengan form pendaftaran (NIM, Nama, PIC, Fakultas)
- **Login dengan NIM dan PIC** (PIC berfungsi sebagai password)
- **Dashboard dengan tampilan tabel** untuk memilih minat olahraga
- **Kelola minat olahraga** dengan fitur tambah/hapus pilihan
- **Filter dan pencarian** olahraga berdasarkan kategori
- **Profil mahasiswa** dengan informasi lengkap

### 👨‍💼 Untuk Admin

- **Login dengan kredensial admin**
- **Dashboard manajemen lengkap** dengan sistem tab
- **Kelola data mahasiswa** (view, edit, delete)
- **Kelola data olahraga** (CRUD operations)
- **Monitoring sistem** dan statistik

### 🏢 Untuk Kemahasiswaan

- **Login dengan kredensial kemahasiswaan**
- **Dashboard monitoring** dengan visualisasi data real-time
- **Laporan statistik** minat olahraga mahasiswa dengan grafik interaktif
- **Rekap data** per fakultas dan kategori olahraga
- **Dashboard cards** dengan statistik overview
- **Grafik visual** menggunakan matplotlib terintegrasi

## 🛠 Teknologi yang Digunakan

- **Python 3.8+**: Bahasa pemrograman utama
- **Tkinter**: Framework GUI native Python
- **SQLite**: Database lokal embedded
- **Matplotlib**: Visualisasi data dan grafik statistik
- **Pillow (PIL)**: Image processing untuk UI enhancement

## 📁 Struktur Proyek

```
├── src/
│   ├── config/              # Konfigurasi aplikasi dan database
│   │   ├── app_config.py    # Konfigurasi utama aplikasi (v2.0.0)
│   │   └── database.py      # Setup dan koneksi database SQLite
│   ├── controllers/         # Business logic (MVC Controller)
│   │   ├── __init__.py
│   │   └── app_controller.py # Kontroller utama aplikasi
│   ├── models/              # Data models (MVC Model)
│   │   ├── __init__.py
│   │   ├── user.py          # Mahasiswa, Admin, Kemahasiswaan
│   │   ├── olahraga.py      # Model Olahraga
│   │   ├── minat_bakat.py   # Relasi Mahasiswa-Olahraga
│   │   └── rekap.py         # Model untuk laporan dan statistik
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   ├── theme.py         # Dark blue theme dengan styling konsisten
│   │   ├── validation_utils.py # Input validation dan sanitasi
│   │   └── helpers.py       # Dialog, Widget, Data, Export utilities
│   └── views/               # GUI components (MVC View)
│       ├── __init__.py
│       ├── login_window.py            # Window login multi-role
│       ├── registration_window.py     # Registrasi mahasiswa baru
│       ├── mahasiswa_dashboard.py     # Dashboard mahasiswa
│       ├── admin_dashboard.py         # Dashboard admin dengan tabs
│       └── kemahasiswaan_dashboard.py # Dashboard dengan charts & export
├── data/                    # Database file (auto-generated)
│   └── sports_management.db # SQLite database dengan schema lengkap
├── main.py                  # Entry point aplikasi
├── requirements.txt         # Python dependencies (Pillow, matplotlib)
├── run.bat                  # Windows batch file untuk eksekusi cepat
└── README.md               # Dokumentasi lengkap ini
```

## 🚀 Instalasi dan Menjalankan Aplikasi

### Prerequisites

- **Python 3.8+** atau lebih baru (Direkomendasikan Python 3.9+)
- **OS**: Windows, macOS, atau Linux
- **RAM**: Minimal 512MB (Direkomendasikan 1GB untuk performa optimal)
- **Storage**: 100MB untuk aplikasi dan database
- **Display**: Resolusi minimal 800x600 (Optimal 1200x800+)

### 📥 Instalasi

1. **Clone atau download project ini**

   ```bash
   # Jika menggunakan git
   git clone https://github.com/Jnckk/Minat-Bakar-Mahasiswa.git
   cd "Minat Bakat Mahasiswa"
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   _Dependencies yang diinstal:_

   - **Pillow >= 9.0.0**: Image processing untuk UI enhancement
   - **matplotlib >= 3.5.0**: Visualisasi data dan grafik statistik

### ▶️ Menjalankan Aplikasi

#### Metode 1: Menggunakan Batch File (Windows)

```bash
.\run.bat
```

#### Metode 2: Manual

```bash
python main.py
```

#### Metode 3: VS Code Task

- Tekan `Ctrl+Shift+P`
- Ketik "Tasks: Run Task"
- Pilih "Run Sports Management System"

_Atau gunakan Command Palette:_

- `Ctrl+Shift+P` → "Run Task" → "shell: Run Sports Management System"

## 🔐 Akun Default

### Admin

- **Username**: `admin`
- **Password**: `admin123`

### Kemahasiswaan

- **Username**: `kemahasiswaan`
- **Password**: `kemahasiswaan123`

### Mahasiswa

- **Registrasi mandiri** melalui form "Registrasi Mahasiswa Baru"
- **Login** menggunakan NIM + PIC yang didaftarkan

## 💾 Database

Aplikasi menggunakan SQLite dengan schema berikut:

### Tabel Utama

- **users**: Data autentikasi untuk semua role
- **mahasiswa**: Data mahasiswa (NIM, nama, PIC, fakultas)
- **admin**: Data administrator sistem
- **kemahasiswaan**: Data staff kemahasiswaan
- **olahraga**: Data olahraga yang tersedia
- **minat_bakat**: Relasi mahasiswa dengan olahraga yang dipilih

### Data Default

- **14 jenis olahraga** (Sepak Bola, Basket, Voli, Badminton, dll.)
- **Kategori olahraga**: Individual dan Tim
- **Akun admin dan kemahasiswaan** siap pakai

## 🎨 User Interface

### Tema Dark Blue

- **Primary Color**: Dark blue gradient (#1e3a8a, #3b82f6)
- **Accent Colors**: Multi-color palette untuk charts dan visualisasi
- **Consistent Styling**: Semua komponen menggunakan theme yang konsisten
- **Responsive Design**: Layout yang adaptif untuk berbagai ukuran layar
- **Modern Typography**: Font Segoe UI dengan hierarki yang jelas
- **Table Layout**: Data ditampilkan dalam format tabel yang mudah dibaca

### Fitur UI

- **Form Validation**: Real-time validation dengan pesan error yang jelas
- **Confirmation Dialogs**: Konfirmasi untuk aksi-aksi penting (hapus, logout, dll.)
- **Search & Filter**: Pencarian dan filter data yang responsif
- **Alternating Row Colors**: Tabel dengan warna baris bergantian untuk readability
- **Window State Management**: Automatic maximized window dengan minimum size
- **Modern Cards Layout**: Dashboard dengan card-based statistics display

## 🧪 Testing

⚠️ **Catatan**: Folder `tests/` belum tersedia dalam struktur proyek saat ini.

Untuk implementasi testing di masa depan:

```bash
# Struktur testing yang direkomendasikan
mkdir tests
touch tests/__init__.py
touch tests/test_models.py
touch tests/test_controllers.py
touch tests/test_utils.py

# Menjalankan tests (jika sudah diimplementasi)
python -m pytest tests/

# Test dengan coverage (jika sudah diimplementasi)
python -m pytest tests/ --cov=src
```

### Rencana Test Coverage

- ✅ Database connection dan operations (implementasi manual)
- ✅ Model CRUD operations (terintegrasi dalam aplikasi)
- ✅ User authentication (berfungsi dalam production)
- ✅ Data validation (active validation dalam forms)
- ⏳ Unit tests otomatis (untuk development selanjutnya)

## 📊 Fitur Unggulan

### 1. **Authentication System**

- Multi-role login (Mahasiswa, Admin, Kemahasiswaan)
- Session management yang aman
- Logout yang proper (kembali ke login, tidak menutup aplikasi)

### 2. **User Management**

- Self-registration untuk mahasiswa
- Profile management
- Role-based access control

### 3. **Sports Management**

- CRUD operations untuk data olahraga
- Kategorisasi olahraga (Individual/Tim)
- Search dan filter functionality

### 4. **Data Visualization**

- Statistik minat olahraga dengan grafik matplotlib terintegrasi
- Dashboard cards dengan real-time statistics
- Color-coded charts dengan palette yang konsisten

### 5. **Error Handling**

- Comprehensive error handling di seluruh aplikasi
- User-friendly error messages
- Debug logging untuk troubleshooting

## 🔧 Konfigurasi

### Database Configuration

```python
# src/config/database.py
DATABASE_PATH = "data/sports_management.db"
```

### Application Configuration

```python
# src/config/app_config.py
class AppConfig:
    APP_NAME = "Sistem Manajemen Minat Olahraga Mahasiswa"
    VERSION = "2.0.0"
    WINDOW_MIN_WIDTH = 800
    WINDOW_MIN_HEIGHT = 600
    DEFAULT_WINDOW_WIDTH = 1000
    DEFAULT_WINDOW_HEIGHT = 700
    MIN_NIM_LENGTH = 8
    MAX_NIM_LENGTH = 15
    MIN_PIC_LENGTH = 6
```

### Theme Configuration

```python
# src/utils/theme.py
# Customizable dark blue theme colors dengan palette lengkap
CHART_COLORS = ("#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6")
```

## 🤝 Kontribusi & Development

Aplikasi ini dibuat dengan prinsip:

- **Clean Code**: Kode yang mudah dibaca dan dipelihara
- **Separation of Concerns**: Arsitektur MVC yang jelas
- **Error Handling**: Penanganan error yang komprehensif
- **User Experience**: Interface yang intuitif dan responsif
- **Modern Python**: Menggunakan type hints dan best practices
- **Scalable Architecture**: Struktur yang mudah dikembangkan

### Development Info

- **Author**: Yusuf Wibisono
- **Architecture**: Model-View-Controller (MVC)
- **UI Framework**: tkinter dengan custom dark blue theme
- **Database**: SQLite dengan ORM custom
- **Python Version**: 3.8+ (Optimized for 3.9+)

## 📞 Support & Troubleshooting

Jika mengalami masalah:

1. **Dependency Issues**: Pastikan semua dependencies terinstall dengan benar
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
2. **Python Version**: Periksa versi Python (minimal 3.8, direkomendasikan 3.9+)
   ```bash
   python --version
   ```
3. **Database Issues**: Hapus file database untuk reset (data akan hilang):
   ```bash
   rm data/sports_management.db  # Linux/Mac
   del data\sports_management.db  # Windows
   ```
4. **Window Display**: Pastikan resolusi layar minimal 800x600
5. **Performance**: Untuk performa optimal, gunakan RAM minimal 1GB

### Known Issues & Solutions

- **Tkinter Import Error**: Install tkinter sesuai OS

  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-tk

  # CentOS/RHEL
  sudo yum install tkinter
  ```

- **Matplotlib Backend**: Jika grafik tidak muncul, install backend GUI
  ```bash
  pip install matplotlib[gui]
  ```

### Logs & Debugging

- Error logs tersimpan dalam console output
- Database schema auto-created saat first run
- Window state management otomatis (maximized pada startup)

---

**Status**: ✅ **READY FOR PRODUCTION v2.0.0**

Aplikasi telah diuji secara menyeluruh dan siap digunakan di lingkungan perguruan tinggi untuk mengelola minat olahraga mahasiswa. Fitur-fitur utama telah terintegrasi dengan baik dengan UI modern dan user experience yang optimal.

_Last Updated: June 2025 | Built with ❤️ using Python & tkinter_

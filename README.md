# ♻️ Safe&Recycle Backend – AIML Service (FastAPI)

Backend dan layanan **AI/ML inference** untuk aplikasi **Safe&Recycle**, dibangun menggunakan **FastAPI**.
Project ini menyediakan **REST API** untuk autentikasi, manajemen user, serta layanan backend lainnya, dan sudah mendukung **database migration menggunakan Alembic**.

---

## 🚀 Tech Stack

* **Python 3.10+**
* **FastAPI**
* **SQLModel (SQLAlchemy Core)**
* **Alembic** (Database Migration)
* **PostgreSQL / MySQL** (berdasarkan konfigurasi)
* **JWT Authentication**
* **Uvicorn**

---

## 📁 Struktur Project

```
backend/
├── app/
│   ├── routers/        # Routing / endpoint API
│   ├── models/         # Model database (SQLModel)
│   ├── schemas/        # Request & response schema
│   ├── services/       # Business logic
│   ├── databases/      # Session & engine database
│   ├── core/           # Utility & helper functions
│   └── main.py
├── alembic/
│   ├── versions/       # File migration
│   └── env.py
├── alembic.ini
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Persiapan Environment

### 1️⃣ Clone Repository

```bash
git clone <repository-url>
cd backend
```

---

### 2️⃣ Buat Virtual Environment

```bash
python -m venv venv
```

Aktifkan virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / MacOS**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Konfigurasi Database

### 1️⃣ Environment Variable (`.env`)

> ⚠️ File `.env` **tidak di-commit ke repository** (masuk `.gitignore`).

---

### 2️⃣ Database Migration (Alembic)

Project ini menggunakan **Alembic** untuk mengelola perubahan struktur database.

```bash
alembic upgrade head
```

---

## ▶️ Menjalankan Server

Jalankan aplikasi FastAPI dengan **Uvicorn**:

```bash
uvicorn app.main:app --reload
```

Server akan berjalan di:

```
http://127.0.0.1:8000
```

---

## 📖 API Documentation

FastAPI menyediakan dokumentasi otomatis:

* **Swagger UI**
  👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

* **ReDoc**
  👉 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔑 Autentikasi

Aplikasi menggunakan **JWT Authentication**:

* **Access Token** → untuk mengakses endpoint terproteksi
* **Refresh Token** → untuk memperbarui access token
* Token yang logout akan **direvoke (blacklist)**

Header yang wajib disertakan:

```
Authorization: Bearer <access_token>
```

---

## 🧪 Testing

Testing dapat dilakukan menggunakan:

* **Postman**
* **Insomnia**
* **Swagger UI**

Pastikan:

* Database aktif
* `.env` sudah benar
* Token JWT valid

---

## 🛠️ Development Notes

* Semua timestamp menggunakan **UTC**
* Struktur project mengikuti pola **separation of concerns**
* Database schema dikelola sepenuhnya melalui **migration**
* Siap untuk **deployment (production-ready)**

---

## 📌 Troubleshooting

Jika terjadi error database:

* Pastikan database sudah berjalan
* Cek `DATABASE_URL` di `.env`
* Pastikan migration sudah dijalankan (`alembic upgrade head`)

---
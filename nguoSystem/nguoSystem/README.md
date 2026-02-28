# Mfumo wa Kushonja Nguo (nguoSystem)

Sistema ya kusimamia oda za kushona nguo - inaunganisha wateja na washonaji.

## Vipengele Vikuu

- Usajili wa watumiaji (wateja na washonaji)
- Mitindo ya nguo
- Kuagiza nguo
- Usimamizi wa oda
- Dashboard ya washonaji

## Mahitaji

- Python 3.11+
- Django 6.0.1
- Pillow (kwa picha)
- MySQL 8+

## Jinsi ya Ku-setup

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd nguoSystem
```

### 2. Unda Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# au
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Nakili `.env.example` kuwa `.env` na ubadilishe values:

```bash
cp .env.example .env
```

Hariri `.env` file na weka:
- SECRET_KEY yako
- DEBUG=True (kwa development)
- ALLOWED_HOSTS
- DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

### 5. MySQL Setup (Development)

Unda database na user kwenye MySQL:

```bash
mysql -u root -p
CREATE DATABASE nguo_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'nguo_user'@'%' IDENTIFIED BY 'nguo_password';
GRANT ALL PRIVILEGES ON nguo_system.* TO 'nguo_user'@'%';
FLUSH PRIVILEGES;
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Unda Superuser (Admin Mkuu)

```bash
python manage.py createsuperuser
```

### 8. Data Migration (SQLite → MySQL)

Kama ulikuwa unatumia SQLite kabla, hamisha data kwa kutumia script:

```bash
python migrate_sqlite_to_mysql.py
```

Ikiwa umehifadhi SQLite file mahali tofauti, tumia:

```bash
SQLITE_DB_PATH=/path/to/db.sqlite3 python migrate_sqlite_to_mysql.py
```

### 9. Run Server

```bash
python manage.py runserver
```

Au kwa amri moja baada ya setup:

```bash
python manage.py migrate && python manage.py runserver
```

Fungua browser: http://127.0.0.1:8000

## Muundo wa Sistema

### Aina za Watumiaji

1. **Superuser** - Admin mkuu wa system (anaweza kufanya kila kitu)
2. **Mshonaji (Tailor)** - Mtu anayeshona nguo (is_staff=True)
   - Anahitaji approval kutoka kwa superuser
   - Anaweza kusimamia oda
   - Anaweza kuongeza mitindo
3. **Mteja** - Mtumiaji wa kawaida (is_staff=False)
   - Anaweza kuona mitindo
   - Anaweza kuagiza nguo

### Apps

- **accounts** - Usimamizi wa watumiaji
- **styles** - Mitindo ya nguo
- **orders** - Oda za nguo

## Teknolojia Zilizotumika

- Django 6.0.1
- MySQL (Database)
- Pillow (Image processing)
- Python Decouple (Environment variables)

## Mawasiliano

Kwa maswali au msaada, wasiliana nasi.

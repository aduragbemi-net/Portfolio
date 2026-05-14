# 🚀 Deployment Files — Drop-In Instructions

These files replace or are added to your existing `feedback_system/` project folder.

---

## 📂 Where Each File Goes

```
feedback_system/                     ← your project root
│
├── Procfile                         ← NEW — copy here
├── runtime.txt                      ← NEW — copy here
├── railway.json                     ← NEW — copy here
├── nixpacks.toml                    ← NEW — copy here
├── requirements.txt                 ← REPLACE with this one
│
├── feedback_project/
│   ├── settings.py                  ← REPLACE with this one
│   └── __init__.py                  ← REPLACE with this one
│
└── feedback/
    └── views.py                     ← REPLACE with this one
```

---

## ⚙️ Environment Variables to Set on Railway

Go to your Railway project → **Variables** tab and add:

| Variable       | Value                                      |
|----------------|--------------------------------------------|
| `SECRET_KEY`   | Generate at https://djecrety.ir            |
| `DEBUG`        | `False`                                    |
| `ALLOWED_HOSTS`| `your-app-name.up.railway.app`             |

Railway automatically adds `DATABASE_URL` when you attach a PostgreSQL plugin.

---

## 🗄️ After Deploy — Run These Once

In the Railway dashboard → your service → **Shell** tab:

```bash
python manage.py migrate
python manage.py createsuperuser
```

The superuser you create will be able to log into `/admin/` and also the
app's admin dashboard (set role = 'admin' via Django admin after creation,
or use the shell: `User.objects.filter(username='your_name').update(role='admin')`).

---

## 💻 Local Development (still works with SQLite)

No env vars needed locally. Just run:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

SQLite is used automatically when `DATABASE_URL` is not set.

If you still want MySQL locally, set this env var before running:
```bash
set USE_PYMYSQL=True   # Windows CMD
# or
export USE_PYMYSQL=True  # Mac/Linux
```

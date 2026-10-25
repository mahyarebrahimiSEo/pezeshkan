# راهنمای جامع استقرار اکوسیستم سلامت دیجیتال پزشکآن روی سرور (Production Deployment Guide)

این مستند برای تیم دواپس (DevOps) و مدیران سرور تهیه شده است تا پروژه را به راحتی روی سرورهای ابری لینوکس (Ubuntu / Debian / RHEL) یا با داکر (Docker) مستقر نمایند.

---

## ۱. پیش‌نیازهای سرور
- **سیستم‌عامل**: Ubuntu 22.04 LTS یا جدیدتر
- **پایتون**: Python 3.11 یا 3.12
- **وب‌سرور معکوس**: Nginx
- **پایگاه داده (اختیاری)**: PostgreSQL 15+ (پروژه دارای SQLite بهینه‌سازی شده در حالت WAL نیز می‌باشد)
- **ابزارهای سیستمی**: `git`, `curl`, `build-essential`, `libpq-dev`

---

## ۲. روش اول: استقرار مستقیم با Systemd و Nginx (روش پیشنهادی استاندارد)

### گام اول: کلون کردن ریپازیتوری
```bash
cd /var/www
git clone https://github.com/mahyarebrahimiSEo/pezeshkan.git pezeshkan
cd pezeshkan
```

### گام دوم: ساخت Virtualenv و نصب وابستگی‌ها
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### گام سوم: تنظیم فایل محیطی (.env)
```bash
cp .env.example .env
nano .env
```
*مقادیر کلیدی مانند `ENVIRONMENT=production`, `ALLOWED_HOSTS`, `ADMIN_PASSWORD` و در صورت نیاز متغیرهای PostgreSQL یا S3 را تنظیم کنید.*

### گام چهارم: اعمال مایگریشن‌های دیتابیس
```bash
python manage.py migrate
```

### گام پنجم: تنظیم سرویس Systemd
یک فایل سرویس در مسیر `/etc/systemd/system/pezeshkan.service` بسازید:
```ini
[Unit]
Description=Pezeshkan Medical Ecosystem Production Cluster
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/pezeshkan
EnvironmentFile=/var/www/pezeshkan/.env
ExecStart=/var/www/pezeshkan/venv/bin/gunicorn config.asgi:application \
          -k uvicorn.workers.UvicornWorker \
          -w 4 \
          -b 127.0.0.1:3000 \
          --timeout 60 \
          --max-requests 5000 \
          --max-requests-jitter 500

Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

فعال‌سازی سرویس:
```bash
sudo chown -R www-data:www-data /var/www/pezeshkan/data /var/www/pezeshkan/mag/uploads
sudo systemctl daemon-reload
sudo systemctl enable --now pezeshkan
sudo systemctl status pezeshkan
```

### گام ششم: تنظیم Nginx معکوس و SSL رایگان با Certbot
فایل تنظیمات در مسیر `/etc/nginx/sites-available/pezeshkan`:
```nginx
server {
    listen 80;
    server_name pezeshk-on.ir www.pezeshk-on.ir;

    client_max_body_size 50M;

    # فایل‌های استاتیک و رسانه‌ها
    location /mag/uploads/ {
        alias /var/www/pezeshkan/mag/uploads/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # انتقال درخواست‌ها به کلاستر جنگو
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 60s;
    }
}
```
فعال‌سازی Nginx و دریافت گواهی SSL:
```bash
sudo ln -s /etc/nginx/sites-available/pezeshkan /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d pezeshk-on.ir -d www.pezeshk-on.ir
```

---

## ۳. روش دوم: استقرار با Docker و Docker Compose

در صورتی که ترجیح می‌دهید با داکر مستقر کنید:
```bash
cp .env.example .env
# ویرایش تنظیمات در صورت نیاز:
nano .env

# اجرای کانتینرها در پس‌زمینه:
docker compose up -d --build

# بررسی لاگ‌ها و سلامت سرویس:
docker compose logs -f
```

---

## ۴. بررسی سلامت و تست اندپوینت‌ها (Smoke Test)
پس از اجرای سرور، بررسی سلامت با دستورات زیر امکان‌پذیر است:
```bash
curl -I http://127.0.0.1:3000/
curl http://127.0.0.1:3000/api/pillars
curl http://127.0.0.1:3000/api/v1/clinic/public/directory/
```

---

## ۵. پشتیبان‌گیری دوره‌ای (Backup)
جهت پشتیبان‌گیری خودکار از دیتابیس و فایل‌های آپلود شده:
```bash
# دیتابیس پیش‌فرض SQLite:
sqlite3 /var/www/pezeshkan/data/pezeshkan.sqlite3 ".backup '/backup/pezeshkan_$(date +%F).sqlite3'"

# رسانه‌ها:
tar -czf /backup/uploads_$(date +%F).tar.gz /var/www/pezeshkan/mag/uploads/
```

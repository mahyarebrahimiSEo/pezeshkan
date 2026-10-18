@echo off
chcp 65001 > nul
title اکوسیستم سلامت دیجیتال پزشکآن - راه‌انداز جامع پروژه
cls

echo ===============================================================================
echo          اکوسیستم سلامت دیجیتال پزشکآن - راه‌انداز یکپارچه کل پروژه
echo ===============================================================================
echo.
echo  در حال اجرای سرور محلی لوکال‌هاست روی پورت 3000...
echo.
echo  نشانی‌های دسترسی به سامانه‌های پزشکآن:
echo  - پلتفرم و وب‌سایت اصلی:            http://localhost:3000/
echo  - پرونده الکترونیک و محصول (EMR):   http://localhost:3000/product
echo  - ارزیابی هوشمند مطب و کلینیک:      http://localhost:3000/start
echo  - مجله سلامت بالینی (ساب‌فولدر):     http://localhost:3000/mag
echo  - استودیو مدیریت محتوا (Tiptap):     http://localhost:3000/admin
echo  - درگاه ورود امن به پنل:             http://localhost:3000/login
echo.
echo  اطلاعات ورود مدیر کل سیستم (مهیار ابراهیمی):
echo  - نام کاربری: mahyarebrahimi
echo  - رمز عبور:   mahyebi86
echo.
echo ===============================================================================
echo در حال باز کردن صفحات اصلی در مرورگر شما...
echo.

timeout /t 1 /nobreak > nul
start "" "http://localhost:3000/"
timeout /t 1 /nobreak > nul
start "" "http://localhost:3000/mag"
timeout /t 1 /nobreak > nul
start "" "http://localhost:3000/admin"

python "%~dp0manage.py" runserver 0.0.0.0:3000

pause

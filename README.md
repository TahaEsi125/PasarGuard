# 🚀 RoXeT VpN

ربات تلگرامی مدیریت و فروش سرویس VPN با پنل مدیریت داخل Telegram و اتصال به PasarGuard.

## ✨ امکانات

- 🤖 پنل مدیریت کامل داخل Telegram
- 🛒 ساخت سرویس از PasarGuard User Template
- 📦 پلن‌های Basic / Premium / VIP
- 📊 آمار سفارش‌ها
- 🔌 تست اتصال به PasarGuard
- 🔐 دریافت Bot Token و اطلاعات تنظیمات هنگام نصب
- 💾 SQLite برای ثبت سفارش‌ها
- 🐧 نصب سریع با `install.sh`
- 🔄 اجرای دائمی با systemd

## 📋 پیش‌نیازها

- Ubuntu 22.04 / 24.04
- دسترسی `root` یا `sudo`
- Python 3
- یک Bot Token از `@BotFather`
- اطلاعات دسترسی API پنل PasarGuard

## 🚀 نصب سریع

### 1️⃣ اتصال به VPS

```bash
ssh root@YOUR_SERVER_IP
```

### 2️⃣ دریافت پروژه

```bash
git clone https://github.com/TahaEsi125/PasarGuard.git
cd PasarGuard
```

> به‌جای `YOUR_USERNAME` نام کاربری GitHub خودت را قرار بده.

### 3️⃣ اجرای نصب

```bash
chmod +x install.sh run.sh
./install.sh
```

نصب‌کننده وابستگی‌های لازم را نصب می‌کند و تنظیمات اولیه را از تو می‌گیرد.

## 🤖 تنظیم ربات

اطلاعات موردنیاز شامل موارد زیر است:

```env
BOT_TOKEN=YOUR_BOT_TOKEN
ADMIN_ID=YOUR_TELEGRAM_ID
PASARGUARD_URL=https://panel.example.com
PASARGUARD_USERNAME=YOUR_USERNAME
PASARGUARD_PASSWORD=YOUR_PASSWORD
```

### 🔑 دریافت Bot Token

1. وارد `@BotFather` در Telegram شو.
2. دستور `/newbot` را بفرست.
3. نام و Username ربات را انتخاب کن.
4. Token را دریافت کن.
5. Token را فقط در `.env` قرار بده.

⚠️ **Bot Token و رمز PasarGuard را داخل GitHub عمومی قرار نده.**

## 👑 تنظیم Admin ID

آیدی عددی حساب Telegram ادمین را در `ADMIN_ID` قرار بده تا فقط ادمین بتواند پنل مدیریت را باز کند.

## 🖥️ اتصال به PasarGuard

آدرس پنل و اطلاعات API را در تنظیمات وارد کن. نمونه:

```env
PASARGUARD_URL=https://panel.example.com
```

همچنین ID قالب‌های فروش را در تنظیمات پروژه قرار بده.

## ▶️ اجرای ربات

برای اجرای دستی:

```bash
./run.sh
```

یا:

```bash
python3 -m bot.main
```

در صورت موفقیت، ربات شروع به کار می‌کند و می‌توانی در Telegram دستور `/start` را بفرستی.

## 🔄 اجرای دائمی با systemd

```bash
sudo cp roxet-vpn.service /etc/systemd/system/roxet-vpn.service
sudo systemctl daemon-reload
sudo systemctl enable --now roxet-vpn
```

بررسی وضعیت:

```bash
sudo systemctl status roxet-vpn
```

نمایش لاگ‌ها:

```bash
sudo journalctl -u roxet-vpn -f
```

ری‌استارت:

```bash
sudo systemctl restart roxet-vpn
```

توقف:

```bash
sudo systemctl stop roxet-vpn
```

## 📁 ساختار پروژه

```text
RoXeT-VpN/
│
├── 🤖 bot/
│   ├── main.py
│   ├── panel.py
│   ├── config.py
│   └── db.py
│
├── 💾 data/
├── ⚙️ .env.example
├── 🚀 install.sh
├── ▶️ run.sh
├── 🔄 roxet-vpn.service
├── 📦 requirements.txt
└── 📖 README.md
```

## 🛡️ امنیت

این اطلاعات را در Repository عمومی قرار نده:

```text
BOT_TOKEN
PASARGUARD_PASSWORD
API_KEY
SECRET_KEY
```

فایل `.env` در `.gitignore` قرار دارد و نباید Commit شود.

## 🆘 رفع خطا

بررسی وضعیت سرویس:

```bash
sudo systemctl status roxet-vpn
```

نمایش آخرین لاگ‌ها:

```bash
sudo journalctl -u roxet-vpn -n 100 --no-pager
```

بررسی Python:

```bash
python3 --version
```

نصب دوباره وابستگی‌ها:

```bash
pip3 install -r requirements.txt
```

## 💙 RoXeT VpN

ساخته‌شده برای مدیریت ساده و حرفه‌ای سرویس‌های VPN از طریق Telegram.

> ⚠️ این پروژه را مطابق قوانین کشور محل استفاده و قوانین سرویس‌های مورد استفاده اجرا کنید.

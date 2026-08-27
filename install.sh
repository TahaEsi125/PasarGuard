#!/usr/bin/env bash
set -euo pipefail
APP_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$APP_DIR"
command -v python3 >/dev/null || { echo 'Python3 is required'; exit 1; }
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
python3 - <<'PY'
from pathlib import Path
p=Path('.env')
print('\n🚀 RoXeT VpN installer\n')
lines=p.read_text().splitlines()
vals={}
for line in lines:
    if '=' in line and not line.lstrip().startswith('#'):
        k,v=line.split('=',1); vals[k]=v

def ask(k,label,secret=False):
    import getpass
    old=vals.get(k,'')
    if old: return old
    return getpass.getpass(label+': ') if secret else input(label+': ')
for k,label,secret in [('BOT_TOKEN','🤖 Telegram Bot Token',True),('ADMIN_IDS','👑 Admin Telegram ID(s), comma separated',False),('PANEL_URL','🌐 PasarGuard Panel URL',False),('PANEL_TOKEN','🔑 PasarGuard API/JWT Token (recommended)',True),('PANEL_USERNAME','👤 Panel username (optional)',False),('PANEL_PASSWORD','🔐 Panel password (optional)',True),('TEMPLATE_BASIC','🟢 Basic template ID (0 disables)',False),('TEMPLATE_PREMIUM','🔵 Premium template ID (0 disables)',False),('TEMPLATE_VIP','🟣 VIP template ID (0 disables)',False)]:
    vals[k]=ask(k,label,secret)
for i,line in enumerate(lines):
    if '=' in line and not line.lstrip().startswith('#'):
        k=line.split('=',1)[0]
        if k in vals: lines[i]=k+'='+vals[k]
p.write_text('\n'.join(lines)+'\n')
PY
chmod +x install.sh
cat > /mnt/data/RoXeT-VpN/run.sh <<'SH'
#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
. .venv/bin/activate
exec python main.py

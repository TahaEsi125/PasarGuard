import asyncio, html, logging, secrets, string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from config import *
from db import init_db, save_customer, save_order, orders_count
from panel import PasarGuard, PanelError

logging.basicConfig(level=logging.INFO)
log=logging.getLogger('roxet')
panel=PasarGuard()

PLANS={'basic':('🟢 Basic',TEMPLATE_BASIC),'premium':('🔵 Premium',TEMPLATE_PREMIUM),'vip':('🟣 VIP',TEMPLATE_VIP)}

def is_admin(uid): return uid in ADMIN_IDS

def main_menu(uid):
    rows=[[InlineKeyboardButton('🛒 خرید سرویس',callback_data='buy'),InlineKeyboardButton('📦 سرویس‌های من',callback_data='mine')],
          [InlineKeyboardButton('📊 وضعیت پنل',callback_data='status'),InlineKeyboardButton('🆘 پشتیبانی',callback_data='support')]]
    if is_admin(uid): rows.append([InlineKeyboardButton('🛠 پنل مدیریت',callback_data='admin')])
    return InlineKeyboardMarkup(rows)

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    u=update.effective_user; save_customer(u.id,u.username or '')
    text=f'🚀 <b>{BRAND[2:]}</b>\n\nسلام {html.escape(u.first_name or "دوست من")} 👋\nبه ربات مدیریت و فروش سرویس خوش اومدی.\n\n🛰 مدیریت سرویس‌ها از همین‌جا انجام میشه.'
    await update.message.reply_text(text,parse_mode=ParseMode.HTML,reply_markup=main_menu(u.id))

async def buy(update,context):
    q=update.callback_query; await q.answer()
    rows=[]
    for k,(name,tid) in PLANS.items():
        if tid: rows.append([InlineKeyboardButton(name,callback_data='plan:'+k)])
    if not rows: rows=[[InlineKeyboardButton('⚠️ پلن‌ها هنوز تنظیم نشده‌اند',callback_data='noop')]]
    rows.append([InlineKeyboardButton('🔙 بازگشت',callback_data='home')])
    await q.edit_message_text('🛒 <b>انتخاب سرویس</b>\n\nپلن موردنظر را انتخاب کن:',parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup(rows))

async def plan(update,context):
    q=update.callback_query; await q.answer(); key=q.data.split(':',1)[1]; name,tid=PLANS[key]
    context.user_data['plan']=key
    await q.edit_message_text(f'📦 <b>{name}</b>\n\nیک نام کاربری انگلیسی وارد کن (مثلاً: Mike123):',parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 لغو',callback_data='buy')]]))
    context.user_data['await_username']=True

async def text_handler(update,context):
    if not context.user_data.get('await_username'): return
    username=update.message.text.strip()
    if not (3<=len(username)<=64) or any(c not in string.ascii_letters+string.digits+'_-.' for c in username):
        await update.message.reply_text('❌ نام کاربری معتبر نیست. فقط حروف انگلیسی، عدد، - _ . و حداقل ۳ کاراکتر.')
        return
    key=context.user_data.pop('plan'); context.user_data.pop('await_username',None); tid=PLANS[key][1]
    await update.message.reply_text('⏳ در حال ساخت سرویس...')
    try:
        result=await panel.create_from_template(tid,username,f'Created by Telegram user {update.effective_user.id}')
        sub=result.get('subscription_url') or result.get('subscription_link') or result.get('subscription') or ''
        save_order(update.effective_user.id,username,key)
        msg=f'✅ <b>سرویس ساخته شد</b>\n\n👤 Username: <code>{html.escape(username)}</code>\n📦 Plan: {PLANS[key][0]}\n'
        if sub: msg+=f'\n🔗 Subscription:\n<code>{html.escape(str(sub))}</code>'
        else: msg+='\n🔗 لینک اشتراک را از پنل PasarGuard بردار.'
        await update.message.reply_text(msg,parse_mode=ParseMode.HTML,reply_markup=main_menu(update.effective_user.id))
    except Exception as e:
        log.exception('create user failed'); await update.message.reply_text('❌ ساخت سرویس انجام نشد.\n\n'+html.escape(str(e)),parse_mode=ParseMode.HTML)

async def callback(update,context):
    q=update.callback_query; data=q.data
    if data=='noop': await q.answer(); return
    if data=='home': await q.answer(); await q.edit_message_text(f'🚀 <b>{BRAND[2:]}</b>\n\nمنوی اصلی:',parse_mode=ParseMode.HTML,reply_markup=main_menu(q.from_user.id)); return
    if data=='buy': return await buy(update,context)
    if data.startswith('plan:'): return await plan(update,context)
    if data=='mine':
        await q.answer(); await q.edit_message_text('📦 <b>سرویس‌های من</b>\n\nبرای مشاهده دقیق، از نام کاربری سرویس در پنل استفاده کن.\n\n🛠 نسخه بعدی این بخش را به لیست کامل کاربران متصل می‌کند.',parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 بازگشت',callback_data='home')]])); return
    if data=='support':
        await q.answer(); await q.edit_message_text('🆘 <b>پشتیبانی</b>\n\nآیدی پشتیبانی را در کد/ENV پروژه تنظیم کن.',parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 بازگشت',callback_data='home')]])); return
    if data=='status':
        await q.answer();
        try:
            nodes=await panel.nodes(); await q.edit_message_text('🟢 اتصال به PasarGuard برقرار است.\n\n'+html.escape(str(nodes)[:2500]),parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 بازگشت',callback_data='home')]]))
        except Exception as e: await q.edit_message_text('🔴 اتصال به پنل برقرار نشد.\n\n'+html.escape(str(e)),parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 بازگشت',callback_data='home')]]))
        return
    if data=='admin' and is_admin(q.from_user.id):
        await q.answer(); kb=[[InlineKeyboardButton('📈 آمار ربات',callback_data='admin_stats')],[InlineKeyboardButton('🔌 تست PasarGuard',callback_data='status')],[InlineKeyboardButton('🔙 بازگشت',callback_data='home')]]
        await q.edit_message_text('🛠 <b>پنل مدیریت RoXeT VpN</b>\n\nمدیریت اصلی از داخل تلگرام انجام می‌شود.',parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup(kb)); return
    if data=='admin_stats' and is_admin(q.from_user.id):
        await q.answer(); await q.edit_message_text(f'📊 <b>آمار</b>\n\n🛒 سفارش‌ها: <code>{orders_count()}</code>',parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 بازگشت',callback_data='admin')]])); return

async def shutdown(app): await panel.close()

def run():
    if not BOT_TOKEN: raise SystemExit('BOT_TOKEN is empty. Run install.sh and fill .env')
    init_db(); app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start',start)); app.add_handler(CallbackQueryHandler(callback)); app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,text_handler))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__=='__main__': run()

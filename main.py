import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder
import config
from domain_checker import DomainChecker
from database import Database

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
checker = DomainChecker()
db = Database()

async def background_monitoring_task():
    while True:
        try:
            monitors = await db.get_all_monitors()
            if not monitors:
                await asyncio.sleep(60)
                continue
            
            for monitor in monitors:
                m_id, user_id, domain = monitor
                try:
                    result = await checker.check(domain)
                    if result['status'] == 'available':
                        text = (
                            f"🚨 <b>ALARM! DOMAIN DÜŞTÜ!</b>\n"
                            f"🌐 <code>{domain}</code> şu an <b>BOŞTA!</b>"
                        )
                        builder = InlineKeyboardBuilder()
                        builder.button(text="🚀 Hemen Al", url=f"https://tr.godaddy.com/domainsearch/find?checkAvail=1&domainToCheck={domain}")
                        await bot.send_message(user_id, text, reply_markup=builder.as_markup())
                        await db.remove_monitor(m_id)
                    await asyncio.sleep(2)
                except:
                    pass
            await asyncio.sleep(60)
        except:
            await asyncio.sleep(60)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await db.add_user(message.from_user.id, message.from_user.username)
    await message.answer(
        "<b>🦅 R10 Pro Domain Analizcisi</b>\n\n"
        "Domain Yaşı, Kalan Gün ve SEO Analizi.\n"
        "<i>Sorgulamak için domain adını yazın.</i>"
    )

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    stats = await db.get_stats()
    await message.answer(f"📊 Kullanıcı: {stats['users']} | Sorgu: {stats['queries']}")

@dp.message(F.text)
async def handle_message(message: types.Message):
    raw_text = message.text
    user_id = message.from_user.id
    domains = [d.strip() for d in raw_text.split(',')][:5]

    await bot.send_chat_action(message.chat.id, action="typing")
    
    try:
        if len(domains) == 1:
            await handle_single_domain(message, domains[0], user_id)
        else:
            await handle_bulk_domain(message, domains, user_id)
    except Exception as e:
        await message.answer(f"⚠️ Hata: {e}")

async def handle_single_domain(message, domain, user_id):
    status_msg = await message.answer(f"🔍 <code>{domain}</code> analiz ediliyor...")
    
    try:
        result = await checker.check(domain)
        await db.log_query(user_id, result['domain'], result['status'])
        builder = InlineKeyboardBuilder()

        if result['status'] == 'available':
            text = (
                f"✅ <b>DOMAIN BOŞTA!</b>\n"
                f"🌐 <code>{result['domain']}</code>\n\n"
                f"💡 <i>Projelik veya jenerik olabilir.</i>"
            )
            builder.button(text="🚀 Kayıt Et (Godaddy)", url=f"https://tr.godaddy.com/domainsearch/find?checkAvail=1&domainToCheck={result['domain']}")
        
        elif result['status'] == 'registered':
            d = result['data']
            age = result.get('age', 'Bilinmiyor')
            remaining = result.get('remaining_days', 0)
            
            time_icon = "🟢"
            if isinstance(remaining, int):
                if remaining < 60: time_icon = "🔴"
                elif remaining < 180: time_icon = "🟡"

            registrar_name = str(d.get('registrar', 'Bilinmiyor'))
            if registrar_name == "None": registrar_name = "Bilinmiyor"

            text = (
                f"🔒 <b>DOMAIN DOLU</b>\n"
                f"🌐 <code>{result['domain']}</code>\n"
                f"➖➖➖➖➖➖➖➖➖➖\n"
                f"👴 <b>Yaş:</b> {age}\n"
                f"{time_icon} <b>Kalan Süre:</b> {remaining} Gün\n"
                f"🏢 <b>Firma:</b> {registrar_name}\n"
                f"➖➖➖➖➖➖➖➖➖➖"
            )
            builder.button(text="🔔 Düşünce Haber Ver", callback_data=f"monitor_{result['domain']}")
            builder.button(text="🔍 Google Ban Kontrol", url=f"https://www.google.com/search?q=site:{result['domain']}")
            builder.button(text="📜 Whois", callback_data=f"whois_{result['domain']}")
            builder.button(text="💡 Alternatif Bul", callback_data=f"suggest_{result['domain']}")
        
        else:
            text = f"⚠️ Hata: {result.get('message')}"

        builder.adjust(1)
        await status_msg.edit_text(text, reply_markup=builder.as_markup())
        
    except Exception as e:
        await status_msg.edit_text(f"⚠️ Beklenmeyen Hata: {str(e)}")

async def handle_bulk_domain(message, domains, user_id):
    report = "<b>📋 Toplu Analiz</b>\n\n"
    msg = await message.answer("Taranıyor...")
    for d in domains:
        try:
            r = await checker.check(d)
            if r['status']=='available':
                report += f"✅ <code>{d}</code>: <b>BOŞTA</b>\n"
            else:
                rem = r.get('remaining_days', '?')
                report += f"❌ <code>{d}</code>: {rem} gün kaldı\n"
        except: pass
    await msg.edit_text(report)

@dp.callback_query(F.data.startswith("suggest_"))
async def callback_suggest(callback: types.CallbackQuery):
    domain = callback.data.split("_")[1]
    await callback.answer("Jenerik alternatifler aranıyor...")
    sug = await checker.get_smart_suggestions(domain)
    if sug:
        t = f"💡 <b>Boştaki Alternatifler:</b>\n" + "\n".join([f"🔹 {s}" for s in sug])
        await bot.send_message(callback.from_user.id, t, parse_mode=ParseMode.HTML)
    else:
        await bot.send_message(callback.from_user.id, "Mantıklı bir alternatif bulamadım.")

@dp.callback_query(F.data.startswith("monitor_"))
async def callback_monitor(callback: types.CallbackQuery):
    domain = callback.data.split("_")[1]
    await db.add_monitor(callback.from_user.id, domain)
    await callback.answer(f"{domain} sniper moduna alındı! Düşerse yazarım.", show_alert=True)

@dp.callback_query(F.data.startswith("whois_"))
async def callback_whois(callback: types.CallbackQuery):
    domain = callback.data.split("_")[1]
    await callback.answer("Whois verisi çekiliyor...")
    try:
        r = await checker.check(domain)
        if r['status'] == 'registered':
            d = r['data']
            
            ns_raw = d.get('name_servers', [])
            if isinstance(ns_raw, list):
                ns_clean = "\n".join([str(n).lower() for n in ns_raw[:2]])
            else:
                ns_clean = str(ns_raw)

            text = (
                f"📋 <b>WHOIS: {domain}</b>\n"
                f"➖➖➖➖➖➖➖➖➖➖\n"
                f"📅 <b>Kayıt:</b> {d.get('creation_date', '-')}\n"
                f"⏳ <b>Bitiş:</b> {d.get('expiration_date', '-')}\n\n"
                f"📡 <b>Name Servers:</b>\n<code>{ns_clean}</code>"
            )
            await bot.send_message(callback.from_user.id, text, parse_mode=ParseMode.HTML)
    except:
        await callback.answer("Veri hatası", show_alert=True)

async def main():
    await db.create_tables()
    print("Bot aktif.")
    asyncio.create_task(background_monitoring_task())
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
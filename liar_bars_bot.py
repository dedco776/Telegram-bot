import logging import random from aiogram 
import Bot, Dispatcher, types from 
aiogram.types import 
InlineKeyboardMarkup, 
InlineKeyboardButton from aiogram.utils 
import executor API_TOKEN = 
'8053582758:AAH9q5jRek5xphHXb-BoB_p9aSrGsR7Pb4k' 
logging.basicConfig(level=logging.INFO) 
bot = Bot(token=API_TOKEN) dp = 
Dispatcher(bot) games = {} players = {} 
ai_mode_users = set() def 
get_rules_text():
    return ( "🎲 *Liar Bars* o‘yini 
        qoidalari:\n\n" "1. O‘yinchi 1 
        dan 6 gacha son oladi.\n" "2. U 
        rost yoki yolg‘on gapiradi.\n" 
        "3. Raqib 'ishondim' yoki 
        'ko‘rsat' deydi.\n" "4. Agar 
        yolg‘onni ushlab olsa — 
        yutadi!\n" "5. O‘yin 
        navbatma-navbat davom etadi.\n\n" 
        "_/ai — bot bilan o‘ynash, faqat 
        shaxsiy chatda._"
    ) 
@dp.message_handler(commands=['start']) 
async def start_game(message: 
types.Message):
    if message.chat.type != "private": 
        chat_id = message.chat.id if 
        chat_id not in games:
            games[chat_id] = {'players': 
            [], 'started': False} await 
            message.reply("🕹 O‘yin 
            boshlanishi uchun kamida 2 
            kishi kerak. /start yozishda 
            davom eting.")
        if message.from_user.id not in 
        games[chat_id]['players']:
            games[chat_id]['players'].append(message.from_user.id) 
            await 
            bot.send_message(message.from_user.id, 
            get_rules_text(), 
            parse_mode="Markdown")
        if len(games[chat_id]['players']) 
        >= 2 and not 
        games[chat_id]['started']: 
            games[chat_id]['started'] = 
            True players[chat_id] = 
            {'turn': 0, 'number': None, 
            'truth': None} player_id = 
            games[chat_id]['players'][0] 
            await 
            bot.send_message(chat_id, 
            f"<a 
            href='tg://user?id={player_id}'>1-o‘yinchi</a>, 
            sonni tanlang.", 
            parse_mode="HTML") await 
            ask_number(chat_id, 
            player_id)
    else: await message.answer("🤖 Bot 
        bilan o‘ynash uchun /ai ni 
        bosing.")
@dp.message_handler(commands=['qoida']) 
async def rules(message: types.Message):
    await 
    message.answer(get_rules_text(), 
    parse_mode="Markdown")
@dp.message_handler(commands=['ai']) 
async def ai_game(message: 
types.Message):
    user_id = message.from_user.id 
    ai_mode_users.add(user_id) number = 
    random.randint(1, 6) keyboard = 
    InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Rost", 
        callback_data=f"ai_truth_{number}"), 
        InlineKeyboardButton("❌ 
        Yolg‘on", callback_data="ai_lie")
    ) await message.answer(f"🎯 Sizga son 
    berildi. Rost gapirasizmi yoki 
    aldaysizmi?", reply_markup=keyboard)
@dp.callback_query_handler(lambda c: 
c.data.startswith('ai_truth_')) async def 
ai_truth(call: types.CallbackQuery):
    number = 
    int(call.data.split('_')[-1]) choice 
    = random.choice(['ishondim', 
    'ko‘rsat']) await 
    call.message.edit_text(f"🧠 Siz 
    {number} deb rost gapirdingiz.\n🤖 
    Bot: *{choice}*", 
    parse_mode="Markdown")
@dp.callback_query_handler(lambda c: 
c.data == 'ai_lie') async def 
ai_lie(call: types.CallbackQuery):
    fake_number = random.randint(1, 6) 
    true_number = random.randint(1, 6) 
    while fake_number == true_number:
        fake_number = random.randint(1, 
        6)
    choice = random.choice(['ishondim', 
    'ko‘rsat']) if choice == 'ko‘rsat':
        if fake_number == true_number: 
            result = "😮 To‘g‘ri 
            aytibsiz. Bot yutqazdi!"
        else: result = "🤖 Sizni ushladi! 
            Bot yutdi!"
    else: result = "✅ Bot ishonib qoldi. 
        Navbat sizda!"
    await call.message.edit_text(f"🧠 Siz 
    aslida {true_number} deb o‘ylab, 
    {fake_number} dedingiz.\n🤖 Bot: 
    *{choice}*\n\n{result}", 
    parse_mode="Markdown")
async def ask_number(chat_id, user_id): 
    number = random.randint(1, 6) 
    players[chat_id]['number'] = number 
    keyboard = 
    InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Rost", 
        callback_data=f"truth_{chat_id}"), 
        InlineKeyboardButton("❌ 
        Yolg‘on", 
        callback_data=f"lie_{chat_id}")
    ) await bot.send_message(user_id, 
    f"🔢 Sizga {number} raqam tushdi. 
    Rost aytasizmi?", 
    reply_markup=keyboard)
@dp.callback_query_handler(lambda c: 
c.data.startswith('truth_')) async def 
group_truth(call: types.CallbackQuery):
    chat_id = 
    int(call.data.split('_')[1]) 
    next_player_index = 1 - 
    players[chat_id]['turn'] next_player 
    = 
    games[chat_id]['players'][next_player_index] 
    choice = random.choice(['ishondim', 
    'ko‘rsat']) await 
    bot.send_message(chat_id, f"🤖 
    {choice}") await ask_number(chat_id, 
    next_player) players[chat_id]['turn'] 
    = next_player_index await 
    call.answer()
@dp.callback_query_handler(lambda c: 
c.data.startswith('lie_')) async def 
group_lie(call: types.CallbackQuery):
    chat_id = 
    int(call.data.split('_')[1]) 
    fake_number = random.randint(1, 6) 
    true_number = 
    players[chat_id]['number'] choice = 
    random.choice(['ishondim', 
    'ko‘rsat']) if choice == 'ko‘rsat':
        if fake_number == true_number: 
            result = "😮 To‘g‘ri 
            aytibsiz. Bot yutqazdi!"
        else: result = "🤖 Sizni ushladi! 
            Bot yutdi!"
    else:
        


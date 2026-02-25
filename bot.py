import telebot
import random
from telebot import types
from config import TOKEN, USERS_FILE

bot = telebot.TeleBot(TOKEN)

# ===== юзери =====
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return set(int(x.strip()) for x in f)
    except:
        return set()

def save_user(uid):
    users = load_users()
    if uid not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(uid) + "\n")

# ===== клавіатура =====
def kb_main():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🎲 Кості", "🏀 Баскет")
    kb.add("🎯 Дартс", "🔮 Шар")
    kb.add("🎮 Вгадай", "🎰 Рандом")
    return kb

# ===== старт =====
@bot.message_handler(commands=["start"])
def start(m):
    save_user(m.chat.id)
    bot.send_message(
        m.chat.id,
        "Йо ✌️\n"
        "Я простий бот.\n"
        "Тицяй кнопки, шо є 👇",
        reply_markup=kb_main()
    )

# ===== кості =====
@bot.message_handler(func=lambda m: m.text == "🎲 Кості")
def dice(m):
    bot.send_dice(m.chat.id, emoji="🎲")

@bot.message_handler(func=lambda m: m.text == "🏀 Баскет")
def basket(m):
    bot.send_dice(m.chat.id, emoji="🏀")

@bot.message_handler(func=lambda m: m.text == "🎯 Дартс")
def dart(m):
    bot.send_dice(m.chat.id, emoji="🎯")

# ===== шар долі =====
@bot.message_handler(func=lambda m: m.text == "🔮 Шар")
def ball(m):
    ans = ["Та да", "Та ні", "Може бути", "Скоріше всього", "Не зараз"]
    bot.send_message(m.chat.id, random.choice(ans))

# ===== вгадай число =====
@bot.message_handler(func=lambda m: m.text == "🎮 Вгадай")
def guess_start(m):
    num = random.randint(1, 5)
    bot.send_message(m.chat.id, "Я загадав число від 1 до 5. Давай, пробуй")

    bot.register_next_step_handler(m, lambda msg: guess_check(msg, num))

def guess_check(m, num):
    if not m.text.isdigit():
        bot.send_message(m.chat.id, "Я ж казав — число 😑")
        return

    if int(m.text) == num:
        bot.send_message(m.chat.id, "О, вгадав 💪")
    else:
        bot.send_message(m.chat.id, f"Нє, було {num}")

# ===== рандом =====
@bot.message_handler(func=lambda m: m.text == "🎰 Рандом")
def rnd(m):
    bot.send_message(m.chat.id, f"Випало: {random.randint(1, 100)}")

# ===== розсилка =====
@bot.message_handler(commands=["send"])
def send_all(m):
    text = m.text.replace("/send", "").strip()
    if not text:
        bot.send_message(m.chat.id, "Пиши так: /send текст")
        return

    users = load_users()
    sent = 0

    for uid in users:
        try:
            bot.send_message(uid, f"📢 {text}")
            sent += 1
        except:
            pass

    bot.send_message(m.chat.id, f"Готово. Пішло {sent} людям")

# ===== запуск =====
bot.polling()
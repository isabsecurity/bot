from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from tg_bot.buttons.text import *
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_btn_uz():
    keyboard1 = KeyboardButton(text = "🧾 Mijozlar ro'yxati")
    keyboard2 = KeyboardButton(text = "📊 Otzivlar statistikasi")
    keyboard3 = KeyboardButton(text="🗂 Fikrlar, baholar")
    keyboard4 = KeyboardButton(text="📥 Export CSV")

    design = [[keyboard1, keyboard2],
              [keyboard3, keyboard4],]
    return ReplyKeyboardMarkup(keyboard=design ,
                               resize_keyboard=True)
def admin_btn_ru():
    keyboard1 = KeyboardButton(text="🧾 Список клиентов")
    keyboard2 = KeyboardButton(text="📊 Статистика отзывов")
    keyboard3 = KeyboardButton(text="🗂 Мнения и оценки")
    keyboard4 = KeyboardButton(text="📥 Экспорт CSV")

    design = [[keyboard1, keyboard2],
              [keyboard3, keyboard4],]
    return ReplyKeyboardMarkup(keyboard=design ,
                               resize_keyboard=True)
def phone_number_btn_uz():
    keyboard1=KeyboardButton(text = "Raqamni yuborish 📞",request_contact=True)
    keyboard2=KeyboardButton(text=ortga)
    design=[[keyboard1],[keyboard2]]
    return ReplyKeyboardMarkup(keyboard=design ,
                               resize_keyboard=True)
def phone_number_btn_ru():
    keyboard1 = KeyboardButton(text="Отправить номер 📞", request_contact=True)
    keyboard2 = KeyboardButton(text=nazad)
    design = [[keyboard1], [keyboard2]]
    return ReplyKeyboardMarkup(keyboard=design,
                               resize_keyboard=True)

def rating_buttons_uz():
    keyboard1=KeyboardButton(text='⭐️')
    keyboard2=KeyboardButton(text='⭐️⭐️')
    keyboard3=KeyboardButton(text='⭐️⭐️⭐️')
    keyboard4=KeyboardButton(text='⭐️⭐️⭐️⭐️')
    keyboard5=KeyboardButton(text='⭐️⭐️⭐️⭐️⭐️')
    keyboard6=KeyboardButton(text=ortga)
    design = [[keyboard1, keyboard2],[keyboard3, keyboard4],[keyboard5,keyboard6]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
def rating_buttons_ru():
    keyboard1 = KeyboardButton(text='⭐️')
    keyboard2 = KeyboardButton(text='⭐️⭐️')
    keyboard3 = KeyboardButton(text='⭐️⭐️⭐️')
    keyboard4 = KeyboardButton(text='⭐️⭐️⭐️⭐️')
    keyboard5 = KeyboardButton(text='⭐️⭐️⭐️⭐️⭐️')
    keyboard6=KeyboardButton(text=nazad)
    design = [[keyboard1, keyboard2],[keyboard3, keyboard4],[keyboard5,keyboard6]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
def language_btn():
    keyboard1 = KeyboardButton(text=uz_text)
    keyboard2 = KeyboardButton(text=ru_text)
    design = [[keyboard1, keyboard2]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
#
# def servis_btn_uz(user_id):
#     user = UniversityApplication.objects.filter(tg_id=user_id).first()
#     keyboard1=KeyboardButton(text=uz.get('servis_btn1'))
#     keyboard2=KeyboardButton(text=uz.get('servis_btn2'))
#     keyboard4_text = uz.get('see_info') if user else uz.get('ask_fill_info')
#     keyboard4 = KeyboardButton(text=keyboard4_text)
#     keyboard3=KeyboardButton(text=uz.get('lang_change'))
#     design = [
#         [keyboard1],
#         [keyboard2],
#         [keyboard4,keyboard3]
#     ]
#     return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
#
# def servis_btn_ru(user_id):
#     user = UniversityApplication.objects.filter(tg_id=user_id).first()
#     keyboard1=KeyboardButton(text=ru.get('servis_btn1'))
#     keyboard2=KeyboardButton(text=ru.get('servis_btn2'))
#     keyboard4_text = ru.get('see_info') if user else ru.get('ask_fill_info')
#     keyboard4 = KeyboardButton(text=keyboard4_text)
#     keyboard3 = KeyboardButton(text=ru.get('lang_change'))
#     design = [
#         [keyboard1],
#         [keyboard2],
#         [keyboard4,keyboard3]
#     ]
#     return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)

def back_uz():
    keyboard1 = KeyboardButton(text = ortga)
    design = [[keyboard1]]
    return ReplyKeyboardMarkup(keyboard=design , resize_keyboard=True)
def back_ru():
    keyboard1 = KeyboardButton(text = nazad)
    design = [[keyboard1]]
    return ReplyKeyboardMarkup(keyboard=design , resize_keyboard=True)

def menu_back_uz():
    keyboard3=KeyboardButton(text=menuga_uz)
    design=[[keyboard3]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
def menu_back_ru():
    keyboard3=KeyboardButton(text=menuga_ru)
    design=[[keyboard3]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)

def referral_btn_uz(user_id):
    bot_link = f"https://t.me/isabsecuritybot?start={user_id}"
    text = "🚀 Bizga qo'shiling va uyingiz hamda businnesingiz havfsizligini oshiring."

    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(
        text="Do'stlarni taklif qilish",
        url=f"https://t.me/share/url?url={bot_link}&text={text}"
    ))

    return ikb.as_markup()
def referral_btn_ru(user_id):
    bot_link = f"https://t.me/isabsecuritybot?start={user_id}"
    text = "🚀 Присоединяйтесь к нам и повышайте безопасность вашего дома и бизнеса."

    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(
        text='Пригласить друзей',
        url=f"https://t.me/share/url?url={bot_link}&text={text}"
    ))

    return ikb.as_markup()

def menu_uz():
    keyboard1=KeyboardButton(text='')
    keyboard2=KeyboardButton(text='📑 Kafolat Talonini')
    keyboard3=KeyboardButton(text="👨‍💼 Do'stlatni taklif qilish")
    keyboard4=KeyboardButton(text='⏱️ Kafolat muddatini bilish')
    design = [[keyboard1, keyboard2], [keyboard3, keyboard4]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
def menu_ru():
    keyboard1 = KeyboardButton(text='')
    keyboard2 = KeyboardButton(text='📑 Гарантийный талон')
    keyboard3 = KeyboardButton(text='👨‍💼 Пригласить друзей')
    keyboard4 = KeyboardButton(text='⏱️ Узнать срок гарантии')
    design = [[keyboard1, keyboard2], [keyboard3, keyboard4]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
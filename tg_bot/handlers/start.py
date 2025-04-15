from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.models import Referral, User, Otziv
from dispatcher import dp
from tg_bot.buttons.reply import *
from tg_bot.state.main import *
from tg_bot.utils import *
from tg_bot.language_db import uz, ru

@dp.message(lambda message: message.text == admin_txt)
async def Mening_ma(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(chat_id=message.from_user.id).first()
    if user.interface_language == 'uz':
        if user.role != "ADMIN":
            user.role = "ADMIN"
            user.save()
            await message.answer(text="👮🏻‍♂️ Sizning xuquqingiz Adminga muvoffaqiyatli uzlashtirildi !",
                                 reply_markup=admin_btn_uz())
        else:
            await message.answer(text="👮🏻‍♂️ Admin bo'limi !", reply_markup=admin_btn_uz())
    else:
        if user.role != "ADMIN":
            user.role = "ADMIN"
            user.save()
            await message.answer(
                "👮🏻‍♂️ Ваши права успешно переданы Администратору!", reply_markup=admin_btn_ru())
        else:
            await message.answer(
                text="👮🏻‍♂️ Админ раздел!", reply_markup=admin_btn_ru())


@dp.message(Command("start"), StateFilter(None))
async def start(message: Message, state: FSMContext) -> None:
    tg_id = message.from_user.id
    user = User.objects.filter(chat_id=tg_id).first()
    if user and user.role == "ADMIN":
        if user.interface_language == 'ru':
            await message.answer(text="👮🏻‍♂️ Админ раздел!", reply_markup=admin_btn_ru())
            return
        else:
            await message.answer(text="👮🏻‍♂️ Admin bo'limi !", reply_markup=admin_btn_uz())
            return
    if user:
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return
    if ' ' in message.text:
        try:
            args = int(message.text.split(' ')[1])
            print(f"Args found: {args}")
        except ValueError:
            args = None
        if args:
            referred = Referral.objects.filter(referrer_id=args, referred_user_id=tg_id).first()
            referrer = User.objects.filter(chat_id=args).first()
            if not referred and referrer:
                if not user:
                    user = User.objects.create(chat_id=tg_id)
                Referral.objects.create(referrer_id=args, referred_user_id=tg_id)
                referrer.referal_count += 1
                referrer.save()
                await bot.send_message(
                    chat_id=args,
                    text=f"🥳 Tabriklayman! Sizning referalingiz orqali <a href='tg://user?id={tg_id}'>{message.from_user.full_name}</a> ro'yxatdan o'tdi.",
                    parse_mode="HTML"
                )



    await message.answer(
        text="Tilni tanlang 🇺🇿\nВыберите язык 🇷🇺",
        reply_markup=language_btn()
    )

    await state.set_state(LanguageState.language)


@dp.message(StateFilter(LanguageState.language))
async def select_language(message: Message, state: FSMContext) -> None:
    tg_id = message.from_user.id

    if message.text == uz_text:
        User.objects.update_or_create(chat_id=tg_id, defaults={"interface_language":"uz"})


    elif message.text == ru_text:
        User.objects.update_or_create(chat_id=tg_id, defaults={"interface_language":"ru"})
    else:
        await message.answer(text=uz.get('button'))
        return
    user=User.objects.filter(chat_id=tg_id).first()
    if user.interface_language == 'ru':
        await message.answer(text=ru.get('number_ask'), reply_markup=phone_number_btn_ru())
    else:
        await message.answer(text=uz.get('number_ask'), reply_markup=phone_number_btn_uz())
    await state.set_state(Messeage.phone)


@dp.message(StateFilter(Messeage.phone))
async def phone_handler(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(chat_id=message.from_user.id).first()
    phone_number=None
    if message.contact:
        phone_number = format_phone_number(message.contact.phone_number)
    elif message.text and re.match(r"^\+\d{9,13}$", message.text):
        phone_number = format_phone_number(message.text)
    if not phone_number:
        await state.set_state(Messeage.phone)
        if user.interface_language == 'ru':
            await message.answer(text=ru.get('number_ask'), reply_markup=phone_number_btn_ru())
            return
        else:
            await message.answer(text=uz.get('number_ask'), reply_markup=phone_number_btn_uz())
            return
    user.phone=phone_number
    user.save()
    await state.set_state(Messeage.phone)
    await menu_handler(message, state)

@dp.message(StateFilter(MenuState.menu))
async def menu_handler(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(chat_id=message.from_user.id).first()
    if not user:
        await menu_handler(message, state)
        return

    if user.interface_language == "uz":
        await message.answer(text=uz.get('servis'),reply_markup=menu_uz())
    else:
        await message.answer(text=ru.get('servis'),reply_markup=menu_ru())

    await state.clear()


@dp.message(lambda message: message.text in ["👨‍💼 Do'stlatni taklif qilish",'👨‍💼 Пригласить друзей'])
async def servis(message: Message, state: FSMContext) -> None:
    tg_id=message.from_user.id
    user = User.objects.filter(chat_id=tg_id).first()
    if user.interface_language == "uz":
        await message.answer(text=uz.get('referal'),reply_markup=referral_btn_uz(message.from_user.id))
    else:
        await message.answer(text=ru.get('referal'),reply_markup=referral_btn_ru(message.from_user.id))
    await state.set_state(Messeage.rating)


@dp.message(lambda message: message.text in [ru.get('lang_change'), uz.get('lang_change')])
async def Mening_ma(message: Message, state: FSMContext) -> None:
    await state.set_state(LanguageState.language)
    await message.answer(text="Tilni tanlang 🇺🇿\nВыберите язык 🇷🇺",reply_markup=language_btn())


@dp.message(lambda message: message.text in ('📑 Гарантийный талон','📑 Kafolat Talonini'))
async def begin_fill(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_temp = User.objects.filter(chat_id=user_id).first()
    await state.set_state(Messeage.rating)
    if user_temp.interface_language == 'uz':
        await message.answer(text=uz.get('rating_ask'), reply_markup=rating_buttons_uz())
    else:
        await message.answer(text=ru.get('rating_ask'), reply_markup=rating_buttons_ru())


@dp.message(StateFilter(Messeage.rating))
async def handle_name(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(chat_id=message.from_user.id).first()
    data = await state.get_data()
    if 'msg' in data:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data['msg'])
    if message.text in [ortga, nazad]:
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return
    if message.text not in ['⭐️', '⭐️⭐️', '⭐️⭐️⭐️', '⭐️⭐️⭐️⭐️', '⭐️⭐️⭐️⭐️⭐️', '1', '2', '3', '4', '5']:
        await state.set_state(Messeage.rating)
        if user.interface_language == 'uz':
            await message.answer(text=uz.get('button'))
            return
        else:
            await message.answer(text=ru.get('button'))
            return
    if not message.text.isdigit():
        rating = message.text.count('⭐️')
    else:
        rating = message.text
    data['rating'] = rating
    await state.set_data(data)
    await state.set_state(Messeage.opinion)
    if user.interface_language == 'ru':
        await message.answer(text=ru.get('opinion_ask'), reply_markup=back_ru())
    else:
        await message.answer(text=uz.get('opinion_ask'), reply_markup=back_uz())


@dp.message(StateFilter(Messeage.opinion))
async def opinion(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(chat_id=message.from_user.id).first()
    data = await state.get_data()
    if 'msg' in data:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data['msg'])
    if message.text in [ortga, nazad]:
        await state.set_state(Messeage.rating)
        if user.interface_language == 'uz':
            await message.answer(text=uz.get('rating_ask'))

            return
        else:
            await message.answer(text=ru.get('rating_ask'))

            return
    data['opinion'] = message.text
    await state.set_data(data)
    await state.set_state(Messeage.objective)
    if user.interface_language == 'ru':
        await message.answer(text=ru.get('objection'), reply_markup=back_ru())
    else:
        await message.answer(text=uz.get('objection'), reply_markup=back_uz())


@dp.message(StateFilter(Messeage.objective))
async def handle_phone_number(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(chat_id=message.from_user.id).first()
    data = await state.get_data()
    if 'msg' in data:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data['msg'])
    if message.text in [ortga, nazad]:
        await state.set_state(Messeage.opinion)
        if user.interface_language == 'ru':
            await message.answer(text=ru.get('opinion_ask'), reply_markup=back_ru())

            return
        else:
            await message.answer(text=uz.get('opinion_ask'), reply_markup=back_uz())

            return
    data['objection'] = message.text
    await state.set_data(data)
    if user.interface_language == 'uz':
        await message.answer(text=uz.get('photo'), reply_markup=back_uz())
    else:
        await message.answer(text=ru.get('photo'), reply_markup=back_ru())
    await state.set_state(Messeage.photo)


@dp.message(StateFilter(Messeage.photo))
async def extra_number(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(chat_id=message.from_user.id).first()
    data = await state.get_data()
    if 'msg' in data:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data['msg'])
    if message.text in [ortga, nazad]:
        await state.set_state(Messeage.objective)
        if user.interface_language == 'uz':
            await message.answer(text=uz.get('objection'), reply_markup=back_uz())

            return
        else:
            await message.answer(text=ru.get('objection'), reply_markup=back_ru())

            return
    if not message.photo:
        await message.answer("Iltimos, rasm yuboring!")
        return

    photo_file_id = message.photo[-1].file_id

    data['image'] = photo_file_id
    await state.set_data(data)


    if user.interface_language == 'uz':
        await message.answer(text=uz.get('thanks'), reply_markup=menu_uz())

    else:
        await message.answer(text=ru.get('thanks'), reply_markup=menu_ru())
    await state.set_state(Messeage.accept)
    await accept(message, state)


@dp.message(StateFilter(Messeage.accept))
async def accept(message: Message, state: FSMContext) -> None:
    print('kirdi')
    data = await state.get_data()
    if 'msg' in data:
        del data['msg']
    if "sub_msg1" in data:
        del data['sub_msg1']
    if "inviter_id" in data:
        del data['inviter_id']
    await state.set_data(data)
    data = await state.get_data()
    user=User.objects.get(chat_id=message.from_user.id)
    data['user'] = user
    otziv = Otziv.objects.create(**data)
    otziv.save()
    if 'user' in data:
        del data['user']
    data['phone_number']=user.phone
    save_to_google_sheets(**data)
    await state.set_state(MenuState.menu)

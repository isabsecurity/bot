from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from asgiref.sync import sync_to_async
from bot.models import  Referral, User,Otziv
from dispatcher import dp
from tg_bot.buttons.reply import *
from tg_bot.state.main import *
from tg_bot.utils import *


@dp.message(lambda message: message.text == admin_txt)
async def Mening_ma(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(chat_id=message.from_user.id).first()
    if user.role != "ADMIN":
        user.role = "ADMIN"
        user.save()
        await message.answer(
            "👮🏻‍♂️ Sizning xuquqingiz Adminga muvoffaqiyatli uzlashtirildi !",
            reply_markup=admin_btn_uz()
        )
    else:
        await message.answer(
            "👮🏻‍♂️ Admin bo'limi !",
            reply_markup=admin_btn_ru()
        )

@dp.message(Command("start"), StateFilter(None))
async def start(message: Message, state: FSMContext) -> None:
    tg_id = message.from_user.id
    idlar = list(User.objects.values_list('chat_id', flat=True))
    user=User.objects.filter(chat_id=tg_id).first()
    if tg_id not in idlar:
        User.objects.create(tg_id=tg_id)
    if ' ' in message.text:
        args = message.text.split(' ')[1]
        print(f"Args found: {args}")
        user1 = User.objects.filter(tg_id=tg_id).first()
        referred = Referral.objects.filter(referrer_id=args, referred_user_id=tg_id).first()
        if not referred and user1:
            Referral.objects.create(referrer_id=args, referred_user_id=tg_id)
            inviter = User.objects.get(tg_id=tg_id)
            inviter.referal_count += 1
            inviter.save()
    if user and user.role=="ADMIN":
        await message.answer(
            "👮🏻‍♂️ Admin bo'limi !",
            reply_markup=admin_btn_ru()
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
        User.objects.update_or_create(
            tg_id=tg_id, defaults={"interface_language": "uz"}
        )


    elif message.text == ru_text:
        User.objects.update_or_create(
            tg_id=tg_id, defaults={"interface_language": "ru"}
        )
    else:
        await message.answer(text=uz.get('button'))
        return

    await state.set_state(MenuState.menu)
    await menu_handler(message, state)


@dp.message(StateFilter(MenuState.menu))
async def menu_handler(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(tg_id=message.from_user.id).first()
    if not user:
        await menu_handler(message, state)
        return

    if user.interface_language == "uz":
        await message.answer(
            text=uz.get('servis'),
        )
    else:
        await message.answer(
            text=ru.get('servis'),
        )

    await state.clear()


@dp.message(lambda message: message.text in commands)
async def servis(message: Message, state: FSMContext) -> None:
    user_temp = User.objects.filter(tg_id=message.from_user.id).first()
    user = User.objects.filter(tg_id=message.from_user.id).first()



@dp.message(lambda message: message.text in [
    ru.get('lang_change'),
    uz.get('lang_change')
])
async def Mening_ma(message: Message, state: FSMContext) -> None:
    await state.set_state(LanguageState.language)

    await message.answer(
        text="Tilni tanlang 🇺🇿\nВыберите язык 🇷🇺",
        reply_markup=language_btn()
    )


@dp.message(lambda message: message.text in (uz.get('ask_fill_info'), ru.get('ask_fill_info')))
async def begin_fill(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_temp = User.objects.filter(tg_id=user_id).first()
    await state.set_state(Messeage.rating)
    if user_temp.interface_language == 'uz':
        msg = await message.answer(text=uz.get('rating_ask'), reply_markup=rating_buttons_uz())
        await state.update_data(msg=msg.message_id)
    else:
        msg = await message.answer(text=ru.get('rating_ask'), reply_markup=rating_buttons_ru())
        await state.update_data(msg=msg.message_id)


@dp.message(StateFilter(Messeage.rating))
async def handle_name(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(tg_id=message.from_user.id).first()
    data = await state.get_data()
    await message.delete()
    if 'msg' in data:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data['msg'])
    if message.text in [ortga, nazad]:
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return
    if message.text not in ['⭐️','⭐️⭐️','⭐️⭐️⭐️','⭐️⭐️⭐️⭐️','⭐️⭐️⭐️⭐️⭐️',1,2,3,4,5]:
        await state.set_state(Messeage.rating)
        if user.interface_language == 'uz':
            await message.answer(text=uz.get('button'))
            return
        else:
            await message.answer(text=ru.get('button'))
            return
    if not message.text.isdigit():
        rating=len(message.text)
    else:
        rating=message.text
    data['rating'] = rating
    await state.set_data(data)
    await state.set_state(Messeage.opinion)
    if user.interface_language == 'ru':
        msg = await message.answer(text=ru.get('opinion_ask'), reply_markup=back_ru())
        await state.update_data(msg=msg.message_id)
    else:
        msg = await message.answer(text=uz.get('opinion_ask'), reply_markup=back_uz())
        await state.update_data(msg=msg.message_id)


@dp.message(StateFilter(Messeage.opinion))
async def opinion(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(tg_id=message.from_user.id).first()
    data = await state.get_data()
    await message.delete()
    if 'msg' in data:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data['msg'])
    if message.text in [ortga, nazad]:
        await state.set_state(Messeage.rating)
        if user.interface_language == 'uz':
            msg = await message.answer(text=uz.get('rating_ask'))
            await state.update_data(msg=msg.message_id)
            return
        else:
            msg = await message.answer(text=ru.get('rating_ask'))
            await state.update_data(msg=msg.message_id)
            return
    data['opinion'] = message.text
    await state.set_data(data)
    await state.set_state(Messeage.objective)
    if user.interface_language == 'ru':
        msg = await message.answer(text=ru.get('objection'), reply_markup=back_ru())
        await state.update_data(msg=msg.message_id)
    else:
        msg = await message.answer(text=uz.get('objection'), reply_markup=back_uz())
        await state.update_data(msg=msg.message_id)


@dp.message(StateFilter(Messeage.objective))
async def handle_phone_number(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(tg_id=message.from_user.id).first()
    data = await state.get_data()
    if 'msg' in data:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data['msg'])
    await message.delete()
    if message.text in [ortga, nazad]:
        await state.set_state(Messeage.opinion)
        if user.interface_language == 'ru':
            msg = await message.answer(text=ru.get('opinion_ask'), reply_markup=back_ru())
            await state.update_data(msg=msg.message_id)
            return
        else:
            msg = await message.answer(text=uz.get('opinion_ask'), reply_markup=back_uz())
            await state.update_data(msg=msg.message_id)
            return
    data['objection'] = message.text
    await state.set_data(data)
    if user.interface_language == 'uz':
        msg = await message.answer(text=uz.get('photo'), reply_markup=back_uz())
        await state.update_data(msg=msg.message_id)
    else:
        msg = await message.answer(text=ru.get('photo'), reply_markup=back_ru())
        await state.update_data(msg=msg.message_id)
    await state.set_state(Messeage.photo)


@dp.message(StateFilter(Messeage.photo))
async def extra_number(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(tg_id=message.from_user.id).first()
    data = await state.get_data()
    if 'msg' in data:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data['msg'])
    await message.delete()
    if message.text in [ortga, nazad]:
        await state.set_state(Messeage.objective)
        if user.interface_language == 'uz':
            msg = await message.answer(text=uz.get('objection'),reply_markup=back_uz())
            await state.update_data(msg=msg.message_id)
            return
        else:
            msg = await message.answer(text=ru.get('objection'), reply_markup=back_ru())
            await state.update_data(msg=msg.message_id)
            return
    if not message.photo:
        await message.answer("Iltimos, rasm yuboring!")
        return

    photo_file_id = message.photo[-1].file_id

    data['photo'] = photo_file_id
    await state.set_state(Messeage.accept)
    if user.interface_language == 'uz':
        msg = await message.answer(text=uz.get('thanks'), reply_markup=back_uz())
        await state.update_data(msg=msg.message_id)
        return
    else:
        msg = await message.answer(text=ru.get('thanks'), reply_markup=back_ru())
        await state.update_data(msg=msg.message_id)
        return



@dp.message(StateFilter(Messeage.accept))
async def accept(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if 'msg' in data:
        del data['msg']
    if "sub_msg1" in data:
        del data['sub_msg1']
    if "inviter_id" in data:
        del data['inviter_id']
    await state.set_data(data)
    data = await state.get_data()
    data['chat_id'] = message.from_user.id
    user_temp = User.objects.filter(tg_id=message.from_user.id).first()
    otziv = Otziv.objects.create(**data)
    otziv.save()
    save_to_google_sheets(**data)
    await state.clear()



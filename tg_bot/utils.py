import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot
from decouple import config
# from aiogram.enums import ChatMemberStatus
# from aiogram.types import ChatMember
from dispatcher import TOKEN


bot = Bot(token=TOKEN)


def format_phone_number(phone_number: str) -> str | bool:
    phone_number = ''.join(c for c in phone_number if c.isdigit())

    # Prepend +998 if missing
    if phone_number.startswith('998'):
        phone_number = '+' + phone_number
    elif not phone_number.startswith('+998'):
        phone_number = '+998' + phone_number

    # Check final phone number length
    if len(phone_number) == 13:
        return phone_number
    else:
        return False


def passport_number_checker(passport_number: str) -> bool:
    return bool(re.fullmatch(r"^[A-Z]{2}\d{7}$", passport_number))


def save_to_google_sheets(rating,opinion,objection,photo):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(filename=config('FILE_PLACE'))
    client = gspread.authorize(creds)
    sheet = client.open("Isab security client opinion").sheet1
    sheet.append_row([rating,opinion,objection,photo])



# async def check_user_subscription(user_id: int) -> bool:
#     results = {}
#     chat_ids = list(ChannelsToSubscribe.objects.values_list("link", flat=True))
#     for chat_id in chat_ids:
#         try:
#             chat_member: ChatMember = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
#             subscribed_statuses = {ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}
#             results[chat_id] = chat_member.status in subscribed_statuses
#         except Exception as e:
#             print(f"❌ Error checking {chat_id}: {e}")
#             results[chat_id] = False
#
#     return all(results.values())
#

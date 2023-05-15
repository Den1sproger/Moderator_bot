import json

from aiogram import types
from bot_config import *



def update_json(message: types.Message,
                remove_warning: bool = False,
                update_warnings: bool = False) -> None | int:
    
    with open(USERS_FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_chat_id = str(message.from_user.id)
    if ((not remove_warning) and (user_chat_id not in data.keys())) or update_warnings:
        # if is not nesessary to remove the 1 of 3 warnings and user is not in users.json
        # or if is nesessary to update the number of warning on 3
        data.update({user_chat_id: 3})
        warnings = None

    elif remove_warning and (user_chat_id not in data.keys()):
        # if is nesessary to remove the 1 of 3 warnings and user is not in users.json
        # add new user in json with 2 warnings
        warnings = 2
        data.update({user_chat_id: warnings})

    elif remove_warning:        # if is nesessary to remove the 1 of 3 warnings 
        warnings = data.get(user_chat_id)
        warnings -= 1
        data.update({user_chat_id: warnings})

    else:               # if user send the + and user there is in json 
        warnings = None
        
    with open(USERS_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return warnings


@dp.message_handler(lambda message: message.text == '+' and message.from_user.id != ADMIN)
async def add_user(message: types.Message) -> None:
    # if user send the +
    update_json(message)


@dp.message_handler(lambda message: message.text != '+' and message.from_user.id != ADMIN)
async def moderate(message: types.Message) -> None:
    # if user send not +
    warnings = update_json(message, remove_warning=True)
    if warnings == 0:
        # banned (kicked) the user in group
        await bot.ban_chat_member(
            chat_id=message.chat.id, user_id=message.from_user.id,
            until_date=60
        )
        update_json(message, update_warnings=True)    # update the number of warnings on 3

    await message.delete()

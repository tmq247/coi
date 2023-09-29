from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import Message

from AnonXMusic.misc import SUDOERS ,db
from AnonXMusic import app, userbot
from AnonXMusic.utils.database import set_cmode
from AnonXMusic.utils.decorators.admins import AdminActual
from config import BANNED_USERS
from AnonXMusic.core.userbot import assistants


@app.on_message(filters.command(["lienket"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def playmode_(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(_["cplay_1"].format(message.chat.title))
    query = message.text.split(None, 2)[1].lower().strip()
    if (str(query)).lower() == "disable":
        await set_cmode(message.chat.id, None)
        return await message.reply_text(_["cplay_7"])
    elif str(query) == "linked":
        chat = await assistants.get_chat(message.chat.id)
        if chat.linked_chat:
            chat_id = assistants.linked_chat.id
            await set_cmode(message.chat.id, chat_id)
            return await message.reply_text(
                _["cplay_3"].format(chat.linked_chat.title, chat.linked_chat.id)
            )
        else:
            return await message.reply_text(_["cplay_2"])
    else:
        try:
            chat = await assistants.get_chat(query)
        except:
            return await message.reply_text(_["cplay_4"])
        if chat.type != ChatType.SUPERGROUP:
            return await message.reply_text(_["cplay_5"])
        try:
            async for user in assistants.get_chat_members(
                chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if user.status == ChatMemberStatus.MEMBER:    #ADMINISTRATOR:
                    cusn = message.from_user.username#user.user.username
                    crid = message.from_user.id#user.user.id
        except:
            return await message.reply_text(_["cplay_4"])
        if crid != message.from_user.id:
            return await message.reply_text(_["cplay_6"].format(chat.title, cusn))
        await set_cmode(message.chat.id, chat.id)
        return await message.reply_text(_["cplay_3"].format(chat.title, chat.id))

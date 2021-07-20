import asyncio
from logging import getLogger
from typing import Dict, Set
import random

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.raw import functions

from ShrutixMusic import nand
from ShrutixMusic.utils.database import get_assistant

LOGGER = getLogger(__name__)

vc_logger_enabled = {}
vc_active_users: Dict[int, Set[int]] = {}
active_vc_chats: Set[int] = set()


async def get_group_call_participants(userbot, peer):
    try:
        full_chat = await userbot.invoke(functions.channels.GetFullChannel(channel=peer))
        if not hasattr(full_chat.full_chat, "call") or not full_chat.full_chat.call:
            return []
        call = full_chat.full_chat.call
        participants = await userbot.invoke(
            functions.phone.GetGroupParticipants(call=call, ids=[], sources=[], offset="", limit=100)
        )
        return participants.participants
    except Exception:
        return []


async def monitor_vc_chat(chat_id):
    userbot = await get_assistant(chat_id)
    if not userbot:
        return

    while chat_id in active_vc_chats and vc_logger_enabled.get(chat_id, False):
        try:
            peer = await userbot.resolve_peer(chat_id)
            plist = await get_group_call_participants(userbot, peer)

            new_users = {p.peer.user_id for p in plist if hasattr(p, "peer")}
            old_users = vc_active_users.get(chat_id, set())

            joined = new_users - old_users
            left = old_users - new_users

            tasks = []
            for u in joined:
                tasks.append(handle_user_join(chat_id, u, userbot))
            for u in left:
                tasks.append(handle_user_leave(chat_id, u, userbot))

            if tasks:
                await asyncio.gather(*tasks)

            vc_active_users[chat_id] = new_users

        except Exception:
            pass

        await asyncio.sleep(2)


async def check_and_monitor_vc(chat_id):
    if not vc_logger_enabled.get(chat_id, False):
        return
    userbot = await get_assistant(chat_id)
    if not userbot:
        return
    try:
        peer = await userbot.resolve_peer(chat_id)
        plist = await get_group_call_participants(userbot, peer)
        if plist and chat_id not in active_vc_chats:
            active_vc_chats.add(chat_id)
            asyncio.create_task(monitor_vc_chat(chat_id))
    except:
        pass


async def handle_user_join(chat_id, user_id, userbot):
    try:
        user = await userbot.get_users(user_id)
        name = user.first_name or "User"
        mention = f'<b><a href="tg://user?id={user_id}">{name}</a></b>'

        join_msgs = [
            f"🎤 {mention} <b>ᴊᴜꜱᴛ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴠᴄ — ʟᴇᴛ'ꜱ ᴍᴀᴋᴇ ɪᴛ ʟɪᴠᴇʟʏ!</b> 🎶",
            f"✨ {mention} <b>ɪꜱ ɴᴏᴡ ɪɴ ᴛʜᴇ ᴠᴄ — ᴡᴇʟᴄᴏᴍᴇ ᴀʙᴏᴀʀᴅ!</b> 🌙",
        ]

        msg = random.choice(join_msgs)
        sent = await nand.send_message(chat_id, msg)
        asyncio.create_task(delete_after_delay(sent, 10))
    except Exception:
        pass


async def handle_user_leave(chat_id, user_id, userbot):
    try:
        user = await userbot.get_users(user_id)
        name = user.first_name or "User"
        mention = f'<b><a href="tg://user?id={user_id}">{name}</a></b>'

        leave_msgs = [
            f"👋 {mention} <b>ʟᴇꜰᴛ ᴛʜᴇ ᴠᴄ — ʜᴏᴩᴇ ᴛᴏ ꜱᴇᴇ ʏᴏᴜ ʙᴀᴄᴋ ꜱᴏᴏɴ!</b> 🌟",
            f"📕 {mention} <b>ꜱᴛᴇᴩᴩᴇᴅ ᴏᴜᴛ — ᴅᴏɴ'ᴛ ᴛᴀᴋᴇ ᴛᴏᴏ ʟᴏɴɢ, ᴡᴇ'ʟʟ ᴍɪꜱꜱ ʏᴏᴜ!</b> 💖",
        ]

        msg = random.choice(leave_msgs)
        sent = await nand.send_message(chat_id, msg)
        asyncio.create_task(delete_after_delay(sent, 10))
    except Exception:
        pass


async def delete_after_delay(msg, sec):
    try:
        await asyncio.sleep(sec)
        await msg.delete()
    except:
        pass


@nand.on_message(filters.command("vclogger") & filters.group)
async def vclogger_cmd(_, message: Message):
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) == 1:
        return await message.reply_text(
            "Use: /vclogger on | off | enable | disable"
        )

    mode = args[1].lower()

    if mode in ["on", "enable", "enabled"]:
        vc_logger_enabled[chat_id] = True
        active_vc_chats.add(chat_id)
        asyncio.create_task(monitor_vc_chat(chat_id))
        return await message.reply_text(
            "✅ <b>VC Logging ENABLED</b>\n(Current State):<b>ᴛʀᴜᴇ</b>"
        )

    if mode in ["off", "disable", "disabled"]:
        vc_logger_enabled[chat_id] = False
        if chat_id in active_vc_chats:
            active_vc_chats.remove(chat_id)
        return await message.reply_text(
            "🚫 <b>VC Logging DISABLED</b>\n(Current State):<b>ꜰᴀʟꜱᴇ</b>"
        )

    return await message.reply_text(
        "Use: /vclogger on | off | enable | disable"
    )


@nand.on_message(filters.group)
async def auto_trigger(_, message: Message):
    chat_id = message.chat.id
    asyncio.create_task(check_and_monitor_vc(chat_id))

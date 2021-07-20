import asyncio
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from motor.motor_asyncio import AsyncIOMotorClient
import config


MONGO_URL = (
    getattr(config, "MONGO_DB_URI", None)
    or getattr(config, "MONGO_URL", None)
    or getattr(config, "MONGO_URI", None)
)

LOGGER_ID = getattr(config, "LOGGER_ID", None)

if not MONGO_URL:
    raise Exception("❌ MONGO_URL missing in config!")

if LOGGER_ID is None:
    raise Exception("❌ LOGGER_ID missing in config!")


mongo = AsyncIOMotorClient(MONGO_URL)
possible_keys = ["chat_id", "id", "_id", "group_id", "chatid"]


async def restart_broadcast(nand):
    try:
        bot = await nand.get_me()

        # --- CLEAN BOT NAME ---
        bot_name = bot.first_name

        # --- TEXT (NO HTML/MARKDOWN) ---
        text = (
            f"✨ ᴛʜɪs ɪs {bot_name}\n\n"
            "ᴛʜᴇ ғᴀsᴛᴇsᴛ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ʙᴏᴛ ғᴏʀ ɢʀᴏᴜᴘs.\n"
            "ᴘʟᴀʏ ʜᴅ ᴀᴜᴅɪᴏ / ᴠɪᴅᴇᴏ, sᴍᴏᴏᴛʜ ᴘᴇʀғᴏʀᴍᴀɴᴄᴇ.\n"
            "ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ғᴏʀ ᴇxᴛʀᴀ ғᴇᴀᴛᴜʀᴇs 🚀"
        )

        # --- BUTTON WITH BOT LINK ---
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ",
                        url=f"https://t.me/{bot.username}?startgroup=s"
                    )
                ]
            ]
        )

        # AUTO DETECT DATABASE
        db_names = await mongo.list_database_names()
        db = mongo[db_names[0]]

        all_colls = await db.list_collection_names()
        used_collection = None
        used_key = None

        for col_name in all_colls:
            col = db[col_name]
            sample = await col.find_one({})
            if not sample:
                continue

            for k in possible_keys:
                if k in sample:
                    used_collection = col
                    used_key = k
                    break

            if used_collection is not None:
                break

        if used_collection is None:
            await nand.send_message(LOGGER_ID, "⚠ No chat collection found in MongoDB!")
            return

        sent = 0

        async for chat in used_collection.find({}):
            cid = chat.get(used_key)
            if not cid:
                continue

            try:
                await nand.send_message(cid, text, reply_markup=button)
                sent += 1
                await asyncio.sleep(0.5)
            except:
                pass

        await nand.send_message(LOGGER_ID, f"🔥 Restart Broadcast Sent to {sent} chats.")

    except Exception as e:
        await nand.send_message(LOGGER_ID, f"⚠ Broadcast Error:\n{e}")

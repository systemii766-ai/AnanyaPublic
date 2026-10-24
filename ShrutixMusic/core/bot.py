from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode, ButtonStyle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config
from ..logging import LOGGER


class Shruti(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")

        super().__init__(
            name="ShrutixMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()

        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username or config.BOT_USERNAME
        self.mention = self.me.mention or self.name

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Add Me To Group",
                        url=f"https://t.me/{self.username}?startgroup=true",
                        style=ButtonStyle.DANGER,
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📢 Support",
                        url=config.SUPPORT_CHAT,
                        style=ButtonStyle.SUCCESS,
                    ),
                    InlineKeyboardButton(
                        "💻 Repo",
                        url="https://github.com/ZoxxOP/AnanyaPublic",
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
            ]
        )

        text = (
            "✨ <b>ʙᴏᴛ ɪs ɴᴏᴡ ʟɪᴠᴇ ✨</b>\n\n"
            f"🚀 <b>{self.name} ʜᴀs sᴜᴄᴄᴇssғᴜʟʟʏ sᴛᴀʀᴛᴇᴅ!</b>\n\n"
            "⚒️ <u><b>ʙᴏᴛ ᴅᴇᴛᴀɪʟs :</b></u>\n"
            f"🪪 <b>ID:</b> <code>{self.id}</code>\n"
            f"👤 <b>Name:</b> {self.name}\n"
            f"📎 <b>Username:</b> @{self.username}\n\n"
            "✅ <b>Everything is set! Bot is online and ready to groove 🎶</b>"
        )

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=text,
                reply_markup=buttons,
            )

        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot failed to access the log group/channel. "
                "Add bot to the log group."
            )
            raise

        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot failed to access log group. "
                f"Reason: {type(ex).__name__}: {ex}"
            )
            raise

        try:
            a = await self.get_chat_member(
                config.LOGGER_ID,
                self.id,
            )

            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Please make the bot admin in the log group."
                )
                raise RuntimeError(
                    "Bot is not administrator in LOGGER_ID chat."
                )

        except Exception as ex:
            LOGGER(__name__).error(
                f"Log group permission check failed: "
                f"{type(ex).__name__}: {ex}"
            )
            raise

        LOGGER(__name__).info(
            f"Music Bot Started as {self.name}"
        )

    async def stop(self):
        await super().stop()

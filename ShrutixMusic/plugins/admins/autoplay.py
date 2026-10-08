import random

from pyrogram import filters
from pyrogram.enums import ButtonStyle, ChatMemberStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from ShrutixMusic import nand
from ShrutixMusic.utils.database import autoplay_off, autoplay_on, is_autoplay
from ShrutixMusic.utils.decorators import AdminRightsCheck
from config import BANNED_USERS


def _autoplay_button(chat_id, mode):
    styles = [
        ButtonStyle.PRIMARY,
        ButtonStyle.SUCCESS,
        ButtonStyle.DANGER,
    ]

    return InlineKeyboardButton(
        text="🔁 Aᴜᴛᴏᴩʟᴀʏ: ᴏɴ" if mode else "🔁 Aᴜᴛᴏᴩʟᴀʏ: ᴏꜰꜰ",
        callback_data=f"autoplay_toggle {chat_id}",
        style=random.choice(styles),
    )


@nand.on_message(
    filters.command("autoplay")
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def autoplay_command(client, message: Message, _, chat_id):
    args = message.text.split()
    action = args[1].lower() if len(args) > 1 else None

    if action in ("on", "enable", "enabled"):
        await autoplay_on(chat_id)
        mode = True
        text = "🔁 Aᴜᴛᴏᴩʟᴀʏ Tᴜʀɴᴇᴅ ᴏɴ ✅"

    elif action in ("off", "disable", "disabled"):
        await autoplay_off(chat_id)
        mode = False
        text = "🔁 Aᴜᴛᴏᴩʟᴀʏ Tᴜʀɴᴇᴅ ᴏꜰꜰ ❌"

    else:
        return await message.reply_text(
            "🔁 <b>Aᴜᴛᴏᴩʟᴀʏ</b>\n\n"
            "Cᴀʟʟʙᴀᴄᴋ:\n"
            "<code>/autoplay off</code>\n"
            "<code>/autoplay on</code>"
        )

    await message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [[_autoplay_button(chat_id, mode)]]
        ),
    )


@nand.on_callback_query(
    filters.regex(r"^autoplay_toggle\s+-?\d+$")
    & ~BANNED_USERS
)
async def autoplay_toggle(client, callback_query):
    try:
        chat_id = int(
            callback_query.data.split(None, 1)[1]
        )

        member = await client.get_chat_member(
            chat_id,
            callback_query.from_user.id,
        )

        if member.status not in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        ):
            await callback_query.answer(
                "Oɴʟʏ Aᴅᴍɪᴍꜱ Cᴀɴ Cᴏɴᴛʀᴏʟ Aᴜᴛᴏᴩʟᴀʏ ❌",
                show_alert=True,
            )
            return

        current = await is_autoplay(chat_id)

        if current:
            await autoplay_off(chat_id)
            new_mode = False
            toast = "🔁 Aᴜᴛᴏᴩʟᴀʏ ᴏꜰꜰ ❌"
        else:
            await autoplay_on(chat_id)
            new_mode = True
            toast = "🔁 Aᴜᴛᴏᴩʟᴀʏ ᴏɴ ✅"

        await callback_query.answer(toast)

        message = callback_query.message

        if not message:
            return

        markup = message.reply_markup

        if not markup:
            return

        new_keyboard = []

        for row in markup.inline_keyboard:
            new_row = []

            for button in row:
                if (
                    button.callback_data
                    and button.callback_data.startswith(
                        "autoplay_toggle "
                    )
                ):
                    new_row.append(
                        _autoplay_button(
                            chat_id,
                            new_mode,
                        )
                    )
                else:
                    new_row.append(button)

            new_keyboard.append(new_row)

        new_markup = InlineKeyboardMarkup(new_keyboard)

        try:
            await message.edit_reply_markup(new_markup)
        except Exception as e:
            if "MESSAGE_NOT_MODIFIED" not in str(e):
                raise

    except Exception as e:
        print(
            f"AUTOPLAY CALLBACK ERROR: "
            f"{type(e).__name__}: {e}"
        )

        try:
            await callback_query.answer(
                "Autoplay error ❌",
                show_alert=True,
            )
        except Exception:
            pass

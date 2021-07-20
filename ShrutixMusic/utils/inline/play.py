import random

from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton
from ShrutixMusic.utils.formatters import time_to_seconds
from config import SUPPORT_CHAT, SUPPORT_CHANNEL, BOT_USERNAME


def random_style():
    return random.choice(
        [
            ButtonStyle.PRIMARY,
            ButtonStyle.SUCCESS,
            ButtonStyle.DANGER,
        ]
    )


def track_markup(_, videoid, user_id, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style=random_style(),
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style=random_style(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=random_style(),
            )
        ],
    ]


def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = int((played_sec / duration_sec) * 100)

    if percentage <= 10:
        bar = "◉──────────"
    elif percentage <= 20:
        bar = "─◉─────────"
    elif percentage <= 30:
        bar = "──◉────────"
    elif percentage <= 40:
        bar = "───◉───────"
    elif percentage <= 50:
        bar = "────◉──────"
    elif percentage <= 60:
        bar = "─────◉─────"
    elif percentage <= 70:
        bar = "──────◉────"
    elif percentage <= 80:
        bar = "───────◉───"
    elif percentage <= 90:
        bar = "────────◉──"
    else:
        bar = "─────────◉─"

    return [
        [
            InlineKeyboardButton(
                "▷",
                callback_data=f"ADMIN Resume|{chat_id}",
                style=random_style(),
            ),
            InlineKeyboardButton(
                "II",
                callback_data=f"ADMIN Pause|{chat_id}",
                style=random_style(),
            ),
            InlineKeyboardButton(
                "‣‣I",
                callback_data=f"ADMIN Skip|{chat_id}",
                style=random_style(),
            ),
            InlineKeyboardButton(
                "▢",
                callback_data=f"ADMIN Stop|{chat_id}",
                style=random_style(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                style=random_style(),
            )
        ],
        [
            InlineKeyboardButton(
                "⏮️ -20s",
                callback_data=f"ADMIN Back|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text="↻",
                callback_data=f"ADMIN Replay|{chat_id}",
                style=ButtonStyle.SUCCESS,
            ),
            InlineKeyboardButton(
                "+20s ⏭️",
                callback_data=f"ADMIN Forward|{chat_id}",
                style=ButtonStyle.DANGER,
            ),
        ],
        [
            InlineKeyboardButton(
                "ᴜᴩᴅᴀᴛᴇ",
                url=SUPPORT_CHANNEL,
                style=random_style(),
            ),
            InlineKeyboardButton(
                "sᴜᴘᴘᴏʀᴛ",
                url=SUPPORT_CHAT,
                style=random_style(),
            ),
        ],
    ]


def stream_markup(_, chat_id):
    return [
        [
            InlineKeyboardButton(
                "▷",
                callback_data=f"ADMIN Resume|{chat_id}",
                style=random_style(),
            ),
            InlineKeyboardButton(
                "II",
                callback_data=f"ADMIN Pause|{chat_id}",
                style=random_style(),
            ),
            InlineKeyboardButton(
                "⏭",
                callback_data=f"ADMIN Skip|{chat_id}",
                style=random_style(),
            ),
            InlineKeyboardButton(
                "▢",
                callback_data=f"ADMIN Stop|{chat_id}",
                style=random_style(),
            ),
        ],
        [
            InlineKeyboardButton(
                "ᴄʟᴏsᴇ",
                callback_data="close",
                style=random_style(),
            )
        ],
    ]


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"AviaxPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
                style=random_style(),
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"AviaxPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
                style=random_style(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=random_style(),
            ),
        ],
    ]


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
                style=random_style(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=random_style(),
            ),
        ],
    ]


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"

    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style=random_style(),
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style=random_style(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                style=random_style(),
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
                style=random_style(),
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                style=random_style(),
            ),
        ],
    ]

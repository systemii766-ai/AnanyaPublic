import random

from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton

import config
from ShrutixMusic import nand


def random_style():
    return random.choice(
        [
            ButtonStyle.PRIMARY,
            ButtonStyle.SUCCESS,
            ButtonStyle.DANGER,
        ]
    )


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{nand.username}?startgroup=true",
                style=random_style(),
            ),
            InlineKeyboardButton(
                text=_["S_B_2"],
                url=config.SUPPORT_CHAT,
                style=random_style(),
            ),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                callback_data="settings_back_helper",
                style=ButtonStyle.DANGER,
            ),
            InlineKeyboardButton(
                text=_["L_N_G"],
                callback_data="LG",
                style=ButtonStyle.PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{nand.username}?startgroup=true",
                style=ButtonStyle.SUCCESS,
            )
        ],
    ]
    return buttons

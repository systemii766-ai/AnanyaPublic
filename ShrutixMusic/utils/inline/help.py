import random
from typing import Union

from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def random_style():
    return random.choice(
        [
            ButtonStyle.PRIMARY,
            ButtonStyle.SUCCESS,
            ButtonStyle.DANGER,
        ]
    )


def help_pannel(_, START: Union[bool, int] = None):
    first = [
        InlineKeyboardButton(
            text=_["CLOSE_BUTTON"],
            callback_data="close",
            style=random_style(),
        )
    ]

    second = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data="settingsback_helper",
            style=random_style(),
        )
    ]

    mark = second if START else first

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["H_B_1"],
                    callback_data="help_callback hb1",
                    style=ButtonStyle.DANGER,
                ),
                InlineKeyboardButton(
                    text=_["H_B_2"],
                    callback_data="help_callback hb2",
                    style=ButtonStyle.SUCCESS,
                ),
                InlineKeyboardButton(
                    text=_["H_B_6"],
                    callback_data="help_callback hb6",
                    style=ButtonStyle.PRIMARY,
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_8"],
                    callback_data="help_callback hb8",
                    style=ButtonStyle.SUCCESS,
                ),
                InlineKeyboardButton(
                    text=_["H_B_11"],
                    callback_data="help_callback hb11",
                    style=ButtonStyle.PRIMARY,
                ),
                InlineKeyboardButton(
                    text=_["H_B_12"],
                    callback_data="help_callback hb12",
                    style=ButtonStyle.DANGER,
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_13"],
                    callback_data="help_callback hb13",
                    style=ButtonStyle.PRIMARY,
                ),
                InlineKeyboardButton(
                    text=_["H_B_15"],
                    callback_data="help_callback hb15",
                    style=ButtonStyle.DANGER,
                ),
                InlineKeyboardButton(
                    text=_["E_X_T"],
                    callback_data="help_callback extra",
                    style=ButtonStyle.SUCCESS,
                ),
            ],
            mark,
        ]
    )


def help_back_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="settingsback_helper",
                    style=random_style(),
                )
            ]
        ]
    )


def extra_menu(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["H_B_16"],
                    callback_data="help_callback hb16",
                    style=ButtonStyle.DANGER,
                ),
                InlineKeyboardButton(
                    text=_["H_B_17"],
                    callback_data="help_callback hb17",
                    style=ButtonStyle.SUCCESS,
                ),
                InlineKeyboardButton(
                    text=_["H_B_18"],
                    callback_data="help_callback hb18",
                    style=ButtonStyle.PRIMARY,
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_19"],
                    callback_data="help_callback hb19",
                    style=random_style(),
                ),
                InlineKeyboardButton(
                    text=_["H_M_E"],
                    callback_data="help_callback back_to_help",
                    style=random_style(),
                ),
            ],
        ]
    )


def private_help_panel(_):
    from ShrutixMusic import nand

    return [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{nand.username}?start=help",
                style=random_style(),
            )
        ]
    ]

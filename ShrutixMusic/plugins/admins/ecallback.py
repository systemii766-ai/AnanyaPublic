from pyrogram import filters
from ShrutixMusic import nand
from config import BANNED_USERS
from config import SUPPORT_CHAT
from ShrutixMusic.utils.inline.help import help_pannel, extra_menu, help_back_markup
from strings import helpers
from ShrutixMusic.utils.decorators.language import languageCB


@nand.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def help_cb(client, CallbackQuery, _):

    data = CallbackQuery.data.split(None, 1)[1]
    keyboard = help_back_markup(_)

    # EXTRA MENU PAGE
    if data == "extra":
        return await CallbackQuery.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=extra_menu(_),
        )

    # BACK TO MAIN HELP PANEL
    if data == "back_to_help":
        return await CallbackQuery.edit_message_text(
            _["help_1"],
            reply_markup=help_pannel(_, START=True),
        )

    # OLD HELP BUTTONS
    if data == "hb1":
        return await CallbackQuery.edit_message_text(helpers.HELP_1, reply_markup=keyboard)
    if data == "hb2":
        return await CallbackQuery.edit_message_text(helpers.HELP_2, reply_markup=keyboard)
    if data == "hb3":
        return await CallbackQuery.edit_message_text(helpers.HELP_3, reply_markup=keyboard)
    if data == "hb4":
        return await CallbackQuery.edit_message_text(helpers.HELP_4, reply_markup=keyboard)
    if data == "hb5":
        return await CallbackQuery.edit_message_text(helpers.HELP_5, reply_markup=keyboard)
    if data == "hb6":
        return await CallbackQuery.edit_message_text(helpers.HELP_6, reply_markup=keyboard)
    if data == "hb7":
        return await CallbackQuery.edit_message_text(helpers.HELP_7, reply_markup=keyboard)
    if data == "hb8":
        return await CallbackQuery.edit_message_text(helpers.HELP_8, reply_markup=keyboard)
    if data == "hb9":
        return await CallbackQuery.edit_message_text(helpers.HELP_9, reply_markup=keyboard)
    if data == "hb10":
        return await CallbackQuery.edit_message_text(helpers.HELP_10, reply_markup=keyboard)
    if data == "hb11":
        return await CallbackQuery.edit_message_text(helpers.HELP_11, reply_markup=keyboard)
    if data == "hb12":
        return await CallbackQuery.edit_message_text(helpers.HELP_12, reply_markup=keyboard)
    if data == "hb13":
        return await CallbackQuery.edit_message_text(helpers.HELP_13, reply_markup=keyboard)
    if data == "hb14":
        return await CallbackQuery.edit_message_text(helpers.HELP_14, reply_markup=keyboard)
    if data == "hb15":
        return await CallbackQuery.edit_message_text(helpers.HELP_15, reply_markup=keyboard)
    if data == "hb16":
        return await CallbackQuery.edit_message_text(helpers.HELP_16, reply_markup=keyboard)
    if data == "hb17":
        return await CallbackQuery.edit_message_text(helpers.HELP_17, reply_markup=keyboard)
    if data == "hb18":
        return await CallbackQuery.edit_message_text(helpers.HELP_18, reply_markup=keyboard)
    if data == "hb19":
        return await CallbackQuery.edit_message_text(helpers.HELP_19, reply_markup=keyboard)

    # SAFE TRY BLOCK
    try:
        await CallbackQuery.answer()
    except:
        pass

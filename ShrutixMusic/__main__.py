import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from ShrutixMusic import LOGGER, nand, userbot
from ShrutixMusic.core.call import Shruti
from ShrutixMusic.misc import sudo
from ShrutixMusic.plugins import ALL_MODULES
from ShrutixMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS
from ShrutixMusic.rb import restart_broadcast


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    await sudo()

    # Load banned users
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    # 1️⃣ START MAIN BOT FIRST
    await nand.start()

    # 2️⃣ IMPORT ALL PLUGINS (after bot start)
    for all_module in ALL_MODULES:
        importlib.import_module("ShrutixMusic.plugins" + all_module)

    LOGGER("ShrutixMusic.plugins").info("Successfully Imported Modules...")

    # 3️⃣ START ASSISTANT + USERBOT
    await userbot.start()
    await Shruti.start()

    # 4️⃣ START VC STREAM CALL
    try:
        await Shruti.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ShrutixMusic").error(
            "Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass

    # 5️⃣ LOAD DECORATORS
    await Shruti.decorators()

    LOGGER("ShrutixMusic").info(
        "Shrutix Music Bot Started Successfully.\nDon't forget to visit @ShrutiBots"
    )

    # 6️⃣ ⭐ RUN BROADCAST AT VERY END ⭐
    await restart_broadcast(nand)

    # 7️⃣ KEEP BOT ALIVE
    await idle()

    # 8️⃣ STOP CLIENTS ON EXIT
    await nand.stop()
    await userbot.stop()
    LOGGER("ShrutixMusic").info("Stopping ShrutixMusic Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())

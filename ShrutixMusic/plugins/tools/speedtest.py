import asyncio
import speedtest

from pyrogram import filters
from pyrogram.types import Message

from ShrutixMusic import nand
from ShrutixMusic.misc import SUDOERS
from ShrutixMusic.utils.decorators.language import language


def testspeed():
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    return test.results.dict()


@nand.on_message(filters.command(["speedtest", "spt"]) & SUDOERS)
@language
async def speedtest_function(client, message: Message, _):
    m = await message.reply_text(_["server_11"])

    try:
        await m.edit_text(_["server_12"])

        loop = asyncio.get_running_loop()

        result = await loop.run_in_executor(
            None,
            testspeed
        )

        await m.edit_text(_["server_14"])

        output = _["server_15"].format(
            result["client"]["isp"],
            result["client"]["country"],
            result["server"]["name"],
            result["server"]["country"],
            result["server"]["cc"],
            result["server"]["sponsor"],
            result["server"]["latency"],
            result["ping"],
        )

        await message.reply_text(output)

        await m.delete()

    except Exception as e:
        await m.edit_text(
            f"<b>Speedtest Error:</b>\n\n<code>{e}</code>"
        )

import logging

from pyrogram.types import InlineKeyboardMarkup
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    MediumQualityVideo,
)

from ShrutixMusic import YouTube, nand
from ShrutixMusic.misc import db
from ShrutixMusic.platforms.Youtube import get_autoplay
from ShrutixMusic.utils.database import get_lang, is_autoplay
from ShrutixMusic.utils.formatters import seconds_to_min
from ShrutixMusic.utils.inline.play import stream_markup
from ShrutixMusic.utils.stream.queue import put_queue
from ShrutixMusic.utils.thumbnails import get_thumb
from strings import get_string


LOGGER = logging.getLogger(__name__)


async def _first_downloadable(tracks, video):
    for track in tracks or []:
        try:
            video_id = (
                track.get("video_id")
                or track.get("vidid")
                or track.get("id")
            )

            if not video_id:
                continue

            title = (
                track.get("title")
                or "Autoplay Track"
            ).title()

            duration = seconds_to_min(
                track.get("duration") or 0
            )

            file_path, direct = await YouTube.download(
                video_id,
                None,
                video=video,
                videoid=True,
            )

            if file_path:
                return (
                    video_id,
                    title,
                    duration,
                    file_path,
                    direct,
                )

        except Exception:
            continue

    return None


async def try_autoplay(client, chat_id, popped):
    if not popped:
        return False

    if not await is_autoplay(chat_id):
        return False

    video_id = popped.get("vidid")

    if not video_id:
        return False

    if video_id in ("telegram", "soundcloud"):
        return False

    original_chat_id = (
        popped.get("chat_id")
        or chat_id
    )

    video = (
        str(popped.get("streamtype")).lower()
        == "video"
    )

    try:
        tracks = await get_autoplay(video_id)
    except Exception:
        return False

    if not tracks:
        return False

    picked = await _first_downloadable(
        tracks,
        video,
    )

    if not picked:
        return False

    (
        next_id,
        title,
        duration,
        file_path,
        direct,
    ) = picked

    try:
        if video:
            stream = AudioVideoPiped(
                file_path,
                audio_parameters=HighQualityAudio(),
                video_parameters=MediumQualityVideo(),
            )
        else:
            stream = AudioPiped(
                file_path,
                audio_parameters=HighQualityAudio(),
            )

        await client.change_stream(
            chat_id,
            stream,
        )

    except Exception:
        return False

    try:
        await put_queue(
            chat_id,
            original_chat_id,
            file_path if direct else f"vid_{next_id}",
            title,
            duration,
            "Autoplay",
            next_id,
            nand.id,
            "video" if video else "audio",
        )
    except Exception:
        pass

    try:
        language = await get_lang(
            original_chat_id
        )

        _ = get_string(language)

        img = await get_thumb(next_id)

        if not img:
            return True

        button = stream_markup(
            _,
            chat_id,
        )

        run = await nand.send_photo(
            chat_id=original_chat_id,
            photo=img,
            caption=_["stream_1"].format(
                f"https://t.me/{nand.username}?start=info_{next_id}",
                title[:23],
                duration,
                "Autoplay",
            ),
            reply_markup=InlineKeyboardMarkup(
                button
            ),
        )

        try:
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
        except Exception:
            pass

    except Exception:
        LOGGER.exception(
            "Autoplay thumbnail error"
        )

    return True

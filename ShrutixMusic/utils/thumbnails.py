import os
import re
import aiohttp
import aiofiles
import traceback

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from py_yt import VideosSearch


def changeImageSize(maxWidth, maxHeight, image):
    ratio = min(maxWidth / image.size[0], maxHeight / image.size[1])
    newSize = (int(image.size[0] * ratio), int(image.size[1] * ratio))
    return image.resize(newSize, Image.Resampling.LANCZOS)


def truncate(text, max_chars=50):
    words = text.split()
    text1, text2 = "", ""

    for word in words:
        if len(text1 + " " + word) <= max_chars and not text2:
            text1 += " " + word
        else:
            text2 += " " + word

    return [text1.strip(), text2.strip()]


def fit_text(draw, text, max_width, font_path, start_size, min_size):
    size = start_size

    while size >= min_size:
        font = ImageFont.truetype(font_path, size)

        if draw.textlength(text, font=font) <= max_width:
            return font

        size -= 1

    return ImageFont.truetype(font_path, min_size)


def get_overlay_content_box(overlay_img: Image.Image) -> tuple:
    alpha = overlay_img.split()[-1]
    threshold = 20
    binary = alpha.point(lambda p: 255 if p > threshold else 0)
    return binary.getbbox()


async def gen_thumb(videoid: str):
    os.makedirs("cache", exist_ok=True)

    url = f"https://www.youtube.com/watch?v={videoid}"

    try:
        results = VideosSearch(url, limit=1)
        data = await results.next()

        if not data or not data.get("result"):
            print(f"[gen_thumb] No YouTube result found: {videoid}")
            return None

        result = data["result"][0]

        title = re.sub(
            r"\W+",
            " ",
            result.get("title", "Unsupported Title")
        ).title()

        duration = result.get("duration")

        if not duration:
            duration = "00:00"
        else:
            duration = str(duration).strip()

        thumbnails = result.get("thumbnails", [])

        if not thumbnails:
            print(f"[gen_thumb] Thumbnail URL not found: {videoid}")
            return None

        thumbnail = thumbnails[0]["url"].split("?")[0]

        views = result.get(
            "viewCount",
            {}
        ).get(
            "short",
            "Unknown Views"
        )

        channel = result.get(
            "channel",
            {}
        ).get(
            "name",
            "Unknown Channel"
        )

        thumb_cache = f"cache/thumb{videoid}.png"

        timeout = aiohttp.ClientTimeout(total=30)

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        async with aiohttp.ClientSession(
            timeout=timeout,
            headers=headers
        ) as session:

            async with session.get(thumbnail) as resp:

                if resp.status != 200:
                    print(
                        f"[gen_thumb] Thumbnail download failed: "
                        f"HTTP {resp.status}"
                    )
                    return None

                image_data = await resp.read()

                if not image_data:
                    print("[gen_thumb] Empty thumbnail response")
                    return None

                async with aiofiles.open(
                    thumb_cache,
                    mode="wb"
                ) as f:
                    await f.write(image_data)

        if not os.path.exists(thumb_cache):
            print("[gen_thumb] Thumbnail file was not created")
            return None

        youtube = Image.open(thumb_cache).convert("RGBA")

        image1 = changeImageSize(
            1280,
            720,
            youtube
        ).convert("RGBA")

        gradient = Image.new(
            "RGBA",
            image1.size,
            (0, 0, 0, 255)
        )

        blurred = image1.filter(
            ImageFilter.GaussianBlur(5)
        )

        enhancer = ImageEnhance.Brightness(blurred)

        blurred = enhancer.enhance(0.3)

        background = Image.alpha_composite(
            gradient,
            blurred
        )

        draw = ImageDraw.Draw(
            background,
            "RGBA"
        )

        font_path = "ShrutixMusic/assets/font3.ttf"
        font2_path = "ShrutixMusic/assets/font2.ttf"
        player_path = "ShrutixMusic/assets/akash.png"

        if not os.path.exists(font_path):
            print(f"[gen_thumb] Missing font: {font_path}")
            return None

        if not os.path.exists(font2_path):
            print(f"[gen_thumb] Missing font: {font2_path}")
            return None

        if not os.path.exists(player_path):
            print(f"[gen_thumb] Missing overlay: {player_path}")
            return None

        player = Image.open(
            player_path
        ).convert("RGBA").resize(
            (1280, 720),
            Image.Resampling.LANCZOS
        )

        overlay_box = get_overlay_content_box(player)

        if overlay_box:
            content_x1, content_y1, content_x2, content_y2 = overlay_box
        else:
            content_x1 = 0
            content_y1 = 0
            content_x2 = 1280
            content_y2 = 720

        background.paste(
            player,
            (0, 0),
            player
        )

        panel_overlay = Image.new(
            "RGBA",
            background.size,
            (0, 0, 0, 0)
        )

        panel_draw = ImageDraw.Draw(
            panel_overlay,
            "RGBA"
        )

        panel_draw.rounded_rectangle(
            [
                content_x1,
                content_y1,
                content_x2,
                content_y2
            ],
            radius=70,
            fill=(0, 0, 0, 75)
        )

        background = Image.alpha_composite(
            background,
            panel_overlay
        )

        draw = ImageDraw.Draw(
            background,
            "RGBA"
        )

        panel_width = content_x2 - content_x1
        panel_height = content_y2 - content_y1

        thumb_size = int(panel_height * 0.55)

        thumb_size = max(
            150,
            min(
                thumb_size,
                panel_height - 40
            )
        )

        thumb_x = content_x1 + 76

        thumb_y = (
            content_y1
            + (
                panel_height
                - thumb_size
            ) // 2
            + 40
        )

        if thumb_x + thumb_size > content_x2:
            thumb_x = content_x2 - thumb_size - 20

        if thumb_y + thumb_size > content_y2:
            thumb_y = content_y2 - thumb_size - 20

        mask = Image.new(
            "L",
            (thumb_size, thumb_size),
            0
        )

        draw_mask = ImageDraw.Draw(mask)

        radius = int(
            thumb_size * 0.25
        )

        draw_mask.rounded_rectangle(
            [
                0,
                0,
                thumb_size,
                thumb_size
            ],
            radius=radius,
            fill=255
        )

        thumb_square = youtube.resize(
            (thumb_size, thumb_size),
            Image.Resampling.LANCZOS
        )

        thumb_square.putalpha(mask)

        background.paste(
            thumb_square,
            (thumb_x, thumb_y),
            thumb_square
        )

        text_x = thumb_x + thumb_size + 30

        title_y = thumb_y + 10

        info_y = (
            title_y
            + int(thumb_size * 0.33)
        )

        time_y = (
            info_y
            + int(thumb_size * 0.28)
        )

        def truncate_text(text, max_chars=30):
            if len(text) > max_chars:
                return text[:max_chars - 3] + "..."

            return text

        short_title = truncate_text(
            title,
            max_chars=20
        )

        short_channel = truncate_text(
            channel,
            max_chars=20
        )

        title_font = fit_text(
            draw,
            short_title,
            600,
            font_path,
            42,
            28
        )

        draw.text(
            (text_x, title_y),
            short_title,
            fill=(255, 255, 255, 255),
            font=title_font
        )

        info_text = (
            f"{short_channel} • {views}"
        )

        info_font = ImageFont.truetype(
            font2_path,
            22
        )

        draw.text(
            (text_x, info_y),
            info_text,
            fill=(200, 200, 200, 255),
            font=info_font
        )

        time_font = ImageFont.truetype(
            font2_path,
            26
        )

        duration_text = str(duration).strip()

        if not duration_text:
            duration_text = "00:00"

        if ":" not in duration_text:
            duration_text = (
                f"00:{duration_text.zfill(2)}"
            )

        time_display = (
            f"00:00 / {duration_text}"
        )

        draw.text(
            (text_x, time_y),
            time_display,
            fill=(200, 200, 200, 255),
            font=time_font
        )

        watermark_font = ImageFont.truetype(
            font2_path,
            24
        )

        watermark_text = "@TeamAnanyaBots"

        bbox = draw.textbbox(
            (0, 0),
            watermark_text,
            font=watermark_font,
            stroke_width=1
        )

        text_width = (
            bbox[2] - bbox[0]
        )

        text_height = (
            bbox[3] - bbox[1]
        )

        x = (
            background.width
            - text_width
            - 25
        )

        y = (
            background.height
            - text_height
            - 25
        )

        draw.text(
            (x, y),
            watermark_text,
            font=watermark_font,
            fill=(0, 0, 0, 230),
            stroke_width=1,
            stroke_fill=(0, 0, 0, 230)
        )

        try:
            os.remove(thumb_cache)
        except Exception:
            pass

        tpath = f"cache/{videoid}.png"

        background.save(
            tpath,
            "PNG"
        )

        if not os.path.exists(tpath):
            print(
                f"[gen_thumb] Final thumbnail was not created: {tpath}"
            )
            return None

        print(
            f"[gen_thumb] Thumbnail created: {tpath}"
        )

        return tpath

    except Exception as e:
        print(
            f"[gen_thumb Error] {e}"
        )

        traceback.print_exc()

        return None


async def get_thumb(videoid, user=None):
    return await gen_thumb(videoid)

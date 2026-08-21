"""Generate LinkedIn brand assets for GrowthLabs AI.

Reproduces the site's logo (indigo rounded square, three white bars) and
builds the company-page banner in the site's indigo->violet gradient.
Outputs: logo-400.png (page logo), banner-1128x191.png (cover image),
banner-1584x396.png (personal profile banner).
"""
from PIL import Image, ImageDraw, ImageFont

INDIGO = (79, 70, 229)     # #4f46e5
VIOLET = (109, 40, 217)    # #6d28d9
DEEP = (55, 48, 163)       # #3730a3
WHITE = (255, 255, 255)

FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"


def make_logo(size=400, path="logo-400.png"):
    # Site logo: 28x28 viewBox, rx=6, bars at (7,10,3,8) (12,7,3,14) (17,12,3,6)
    s = size / 28
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(6 * s), fill=INDIGO)
    for (x, y, w, h) in [(7, 10, 3, 8), (12, 7, 3, 14), (17, 12, 3, 6)]:
        d.rectangle([x * s, y * s, (x + w) * s, (y + h) * s], fill=WHITE)
    img.save(path)
    print("wrote", path)


def gradient(w, h):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for x in range(w):
        t = x / max(w - 1, 1)
        if t < 0.55:
            u = t / 0.55
            c = tuple(int(DEEP[i] + (INDIGO[i] - DEEP[i]) * u) for i in range(3))
        else:
            u = (t - 0.55) / 0.45
            c = tuple(int(INDIGO[i] + (VIOLET[i] - INDIGO[i]) * u) for i in range(3))
        for y in range(h):
            px[x, y] = c
    return img


def make_banner(w, h, path, title_px, sub_px, margin_px):
    img = gradient(w, h)
    d = ImageDraw.Draw(img)
    title_font = ImageFont.truetype(FONT_BOLD, title_px)
    sub_font = ImageFont.truetype(FONT_REG, sub_px)

    # soft decorative circles, echoing the site's blurred blobs
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([w * 0.72, -h * 0.6, w * 1.05, h * 0.55], fill=(255, 255, 255, 18))
    od.ellipse([w * 0.82, h * 0.5, w * 1.15, h * 1.6], fill=(255, 255, 255, 14))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    # mini logo mark
    mark = int(h * 0.30)
    s = mark / 28
    mx, my = margin_px, int(h * 0.18)
    d.rounded_rectangle([mx, my, mx + mark, my + mark], radius=int(6 * s), fill=WHITE)
    for (x, y, bw, bh) in [(7, 10, 3, 8), (12, 7, 3, 14), (17, 12, 3, 6)]:
        d.rectangle([mx + x * s, my + y * s, mx + (x + bw) * s, my + (y + bh) * s], fill=INDIGO)

    tx = mx + mark + int(h * 0.12)
    d.text((tx, my - int(title_px * 0.12)), "GrowthLabs AI", font=title_font, fill=WHITE)

    d.text(
        (margin_px, my + mark + int(h * 0.10)),
        "Know exactly what to fix next in your business.",
        font=sub_font,
        fill=(224, 231, 255),
    )
    img.save(path)
    print("wrote", path)


make_logo(400, "logo-400.png")
make_banner(1128, 191, "banner-1128x191.png", title_px=44, sub_px=22, margin_px=48)
make_banner(1584, 396, "banner-1584x396.png", title_px=88, sub_px=42, margin_px=90)

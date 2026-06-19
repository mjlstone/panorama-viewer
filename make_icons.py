"""Generate PWA icons (multi-size PNG + maskable) for the panorama viewer."""
from PIL import Image, ImageDraw, ImageFilter
import os

OUT = os.path.join(os.path.dirname(__file__), "icons")
os.makedirs(OUT, exist_ok=True)

def make_icon(size, maskable=False):
    """Draw a globe with longitude/latitude lines on a dark gradient background."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Background: rounded square with dark gradient-ish fill
    pad = int(size * 0.06) if not maskable else int(size * 0.0)
    radius = int(size * 0.22)
    bg_box = [pad, pad, size - pad, size - pad]
    # Solid dark background (maskable needs full bleed)
    d.rounded_rectangle(bg_box, radius=radius, fill=(14, 17, 22, 255))

    # Soft glow circle behind globe
    glow_r = int(size * 0.30)
    cx = cy = size // 2
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - glow_r, cy - glow_r, cx + glow_r, cy + glow_r],
               fill=(78, 161, 255, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(size * 0.04))
    img.alpha_composite(glow)

    # Globe
    R = int(size * 0.27)
    # Globe body gradient
    globe = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gdd = ImageDraw.Draw(globe)
    gdd.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(40, 90, 160, 255))
    img.alpha_composite(globe)

    # Latitude / longitude lines on the globe (clip to circle)
    line_w = max(1, int(size * 0.012))
    overlay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    line_color = (220, 235, 255, 230)

    # Latitude lines (horizontal chords inside circle)
    import math
    for frac in (-0.66, -0.33, 0.0, 0.33, 0.66):
        y = cy + R * frac
        half = math.sqrt(max(0, R * R - (R * frac) ** 2))
        od.line([cx - half, y, cx + half, y], fill=line_color, width=line_w)
    # Equator a bit thicker
    od.line([cx - R, cy, cx + R, cy],
            fill=(255, 255, 255, 255), width=line_w + 1)

    # Longitude lines (ellipses = meridians)
    for k in (0.35, 0.7):
        w = R * k
        od.ellipse([cx - w, cy - R, cx + w, cy + R],
                   outline=line_color, width=line_w)

    # Mask overlay to globe circle
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - R, cy - R, cx + R, cy + R], fill=255)
    overlay.putalpha(mask)
    img.alpha_composite(overlay)

    # Rim highlight
    d.ellipse([cx - R, cy - R, cx + R, cy + R],
              outline=(150, 200, 255, 200), width=line_w)

    return img

# Standard sizes used by PWA manifests + apple-touch-icon
sizes = [192, 512, 180, 32, 16]
for s in sizes:
    im = make_icon(s)
    im.save(os.path.join(OUT, f"icon-{s}.png"))
    print("wrote", f"icon-{s}.png")

# Maskable (Android adaptive) — full-bleed background
im = make_icon(512, maskable=True)
im.save(os.path.join(OUT, "icon-maskable-512.png"))
print("wrote icon-maskable-512.png")

# Apple touch icon (180, no transparency for better iOS rendering)
apple = make_icon(180)
bg = Image.new("RGB", (180, 180), (14, 17, 22))
bg.paste(apple, (0, 0), apple)
bg.save(os.path.join(OUT, "apple-touch-icon.png"))
print("wrote apple-touch-icon.png")

# Favicon 32
make_icon(32).save(os.path.join(OUT, "favicon-32.png"))
print("wrote favicon-32.png")

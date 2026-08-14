"""Gera o banner do perfil GitHub com a paleta exata do portfólio."""
from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling
W, H = 1280 * S, 340 * S

BG = (10, 10, 10)
INK = (245, 245, 245)
MUTED = (163, 163, 163)
PRIMARY = (34, 197, 94)
PRIMARY_SOFT = (74, 222, 128)
BORDER = (39, 39, 42)

UB = "/usr/share/fonts/truetype/ubuntu/Ubuntu[wdth,wght].ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def ubuntu(size, weight=400):
    f = ImageFont.truetype(UB, size)
    try:
        f.set_variation_by_axes([100, weight])
    except Exception:
        pass
    return f


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- grade de pontos sutil -------------------------------------------------
step = 26 * S
for y in range(0, H, step):
    for x in range(0, W, step):
        d.ellipse([x, y, x + 1 * S, y + 1 * S], fill=(24, 24, 27))

# --- glow verde radial (canto esquerdo) ------------------------------------
glow = Image.new("RGB", (W, H), BG)
gd = ImageDraw.Draw(glow)
cx, cy = int(W * 0.16), int(H * 0.52)
for i in range(70, 0, -1):
    r = int(i / 70 * 380 * S)
    t = 1 - i / 70
    col = (
        int(BG[0] + (PRIMARY[0] - BG[0]) * t * 0.16),
        int(BG[1] + (PRIMARY[1] - BG[1]) * t * 0.16),
        int(BG[2] + (PRIMARY[2] - BG[2]) * t * 0.16),
    )
    gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
img = Image.blend(img, glow, 0.55)
d = ImageDraw.Draw(img)

# --- barra de acento vertical ----------------------------------------------
bar_x, bar_top, bar_bot = 78 * S, 96 * S, 244 * S
for y in range(bar_top, bar_bot):
    t = (y - bar_top) / (bar_bot - bar_top)
    col = (
        int(PRIMARY[0] + (PRIMARY_SOFT[0] - PRIMARY[0]) * t),
        int(PRIMARY[1] + (PRIMARY_SOFT[1] - PRIMARY[1]) * t),
        int(PRIMARY[2] + (PRIMARY_SOFT[2] - PRIMARY[2]) * t),
    )
    d.rectangle([bar_x, y, bar_x + 3 * S, y + 1], fill=col)

x0 = 110 * S

# --- eyebrow ---------------------------------------------------------------
f_eyebrow = ImageFont.truetype(MONO, 15 * S)
d.text((x0, 100 * S), "F U L L - S T A C K   D E V E L O P E R", font=f_eyebrow, fill=PRIMARY)

# --- nome ------------------------------------------------------------------
f_name = ubuntu(62 * S, 500)
d.text((x0 - 3 * S, 128 * S), "Ramony Menezes Lima", font=f_name, fill=INK)

# --- linha de stack --------------------------------------------------------
f_stack = ubuntu(21 * S, 400)
d.text((x0, 210 * S), "React 19  ·  TypeScript  ·  Firebase  ·  Cloud Functions  ·  Node.js",
       font=f_stack, fill=MUTED)

# --- rodapé ----------------------------------------------------------------
f_foot = ImageFont.truetype(MONO, 14 * S)
d.text((x0, 258 * S), "Uberlandia, MG  //  ramonyml.github.io", font=f_foot, fill=(110, 110, 115))

# --- bloco de código decorativo (direita) ----------------------------------
box_x, box_y = 830 * S, 84 * S
box_w, box_h = 372 * S, 172 * S
d.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h],
                    radius=10 * S, fill=(20, 20, 20), outline=BORDER, width=1 * S)
# barra de título
d.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + 30 * S],
                    radius=10 * S, fill=(31, 31, 31))
d.rectangle([box_x, box_y + 20 * S, box_x + box_w, box_y + 30 * S], fill=(31, 31, 31))
d.line([box_x, box_y + 30 * S, box_x + box_w, box_y + 30 * S], fill=BORDER, width=1 * S)
for i, c in enumerate([(80, 80, 84), (80, 80, 84), PRIMARY]):
    d.ellipse([box_x + (16 + i * 15) * S, box_y + 11 * S,
               box_x + (16 + i * 15) * S + 8 * S, box_y + 19 * S], fill=c)

f_code = ImageFont.truetype(MONO, 13 * S)
lines = [
    [("const ", PRIMARY_SOFT), ("dev", INK), (" = {", MUTED)],
    [("  focus:  ", MUTED), ("'produto real'", (150, 200, 160))],
    [("  stack:  ", MUTED), ("'React + Firebase'", (150, 200, 160))],
    [("  extra:  ", MUTED), ("'redes / GPON'", (150, 200, 160))],
    [("  ships:  ", MUTED), ("true", PRIMARY)],
    [("};", MUTED)],
]
ty = box_y + 46 * S
for parts in lines:
    tx = box_x + 20 * S
    for text, col in parts:
        d.text((tx, ty), text, font=f_code, fill=col)
        tx += d.textlength(text, font=f_code)
    ty += 19 * S

# --- borda inferior --------------------------------------------------------
d.rectangle([0, H - 2 * S, W, H], fill=BORDER)
for x in range(0, int(W * 0.34)):
    t = 1 - x / (W * 0.34)
    d.rectangle([x, H - 2 * S, x + 1, H],
                fill=(int(PRIMARY[0] * t), int(PRIMARY[1] * t), int(PRIMARY[2] * t)))

img.resize((W // S, H // S), Image.LANCZOS).save(
    "banner.png",
    optimize=True,
)
print("ok")

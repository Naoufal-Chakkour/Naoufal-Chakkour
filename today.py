import os
import urllib.request
import json
from datetime import datetime

from PIL import Image, ImageOps

USERNAME = "Naoufal-Chakkour"

API_URL = f"https://api.github.com/users/{USERNAME}"

headers = {
    "User-Agent": "Naoufal-GitHub-Profile"
}

TOKEN = os.environ.get("GH_TOKEN")

if TOKEN:
    headers["Authorization"] = f"Bearer {TOKEN}"


# ============================================================
# GITHUB DATA
# ============================================================

request = urllib.request.Request(API_URL, headers=headers)

with urllib.request.urlopen(request) as response:
    data = json.loads(response.read().decode())

repos = data.get("public_repos", 0)
followers = data.get("followers", 0)
following = data.get("following", 0)

avatar_url = data.get("avatar_url")

updated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")


# ============================================================
# DOWNLOAD AVATAR
# ============================================================

avatar_path = "avatar.png"

avatar_request = urllib.request.Request(
    avatar_url,
    headers={"User-Agent": "Naoufal-GitHub-Profile"}
)

with urllib.request.urlopen(avatar_request) as response:
    with open(avatar_path, "wb") as file:
        file.write(response.read())


# ============================================================
# ASCII CONVERSION
# ============================================================

ASCII_CHARS = "@#8&o:*. "


def image_to_ascii(path, width=60):

    image = Image.open(path).convert("L")

    aspect_ratio = image.height / image.width

    height = max(1, int(width * aspect_ratio * 0.48))

    image = image.resize((width, height))

    image = ImageOps.autocontrast(image)

    pixels = list(image.getdata())

    lines = []

    for y in range(height):

        line = ""

        for x in range(width):

            value = pixels[y * width + x]

            index = int(
                value / 255 * (len(ASCII_CHARS) - 1)
            )

            line += ASCII_CHARS[index]

        lines.append(line)

    return lines


ascii_art = image_to_ascii(avatar_path)


# ============================================================
# CREATE ASCII SVG
# ============================================================

def create_ascii_svg(filename):

    char_width = 12
    line_height = 15

    width = 42 * char_width + 80
    height = len(ascii_art) * line_height + 100

    svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{width}"
height="{height}"
viewBox="0 0 {width} {height}">

<defs>

<filter
id="glow"
x="-50%"
y="-50%"
width="200%"
height="200%">

<feGaussianBlur
stdDeviation="2.5"
result="blur"/>

<feMerge>

<feMergeNode in="blur"/>

<feMergeNode in="SourceGraphic"/>

</feMerge>

</filter>

</defs>

<rect
width="100%"
height="100%"
rx="14"
fill="#0d1117"/>

<text
x="40"
y="35"
font-family="monospace"
font-size="11"
fill="#00ff66">

NAOUFAL@GITHUB

</text>

<text
x="40"
y="60"
font-family="monospace"
font-size="9"
fill="#58a6ff">

ASCII AVATAR

</text>
'''

    y = 85

    for line in ascii_art:

        escaped = (
            line
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        svg += f'''
<text
x="40"
y="{y}"
font-family="monospace"
font-size="12"
font-weight="bold"
fill="#00ff66"
filter="url(#glow)"
xml:space="preserve">{escaped}</text>
'''

        y += line_height

    svg += '''
</svg>
'''

    with open(filename, "w", encoding="utf-8") as file:
        file.write(svg)


os.makedirs("assets", exist_ok=True)

create_ascii_svg(
    "assets/avatar-ascii.svg"
)


# ============================================================
# PROFILE ANALYTICS
# ============================================================

def create_profile_svg(
    filename,
    background,
    card,
    text,
    accent
):

    svg = f'''<svg
width="1000"
height="300"
viewBox="0 0 1000 300"
xmlns="http://www.w3.org/2000/svg">

<defs>

<filter
id="glow"
x="-50%"
y="-50%"
width="200%"
height="200%">

<feGaussianBlur
stdDeviation="5"
result="blur"/>

<feMerge>

<feMergeNode in="blur"/>

<feMergeNode in="SourceGraphic"/>

</feMerge>

</filter>

</defs>

<rect
width="1000"
height="300"
rx="16"
fill="{background}"/>

<rect
x="25"
y="25"
width="950"
height="250"
rx="12"
fill="{card}"
stroke="{accent}"
stroke-width="2"/>

<text
x="60"
y="75"
font-family="monospace"
font-size="24"
font-weight="bold"
fill="{accent}">

NAOUFAL CHAKKOUR

</text>

<text
x="60"
y="105"
font-family="monospace"
font-size="13"
fill="{text}">

GITHUB ACTIVITY MONITOR

</text>

<line
x1="60"
y1="130"
x2="940"
y2="130"
stroke="{accent}"
opacity="0.35"/>

<text
x="90"
y="180"
font-family="monospace"
font-size="13"
fill="{text}">

PUBLIC REPOSITORIES

</text>

<text
x="90"
y="220"
font-family="monospace"
font-size="30"
font-weight="bold"
fill="{accent}"
filter="url(#glow)">

{repos}

</text>

<text
x="360"
y="180"
font-family="monospace"
font-size="13"
fill="{text}">

FOLLOWERS

</text>

<text
x="360"
y="220"
font-family="monospace"
font-size="30"
font-weight="bold"
fill="{accent}"
filter="url(#glow)">

{followers}

</text>

<text
x="630"
y="180"
font-family="monospace"
font-size="13"
fill="{text}">

FOLLOWING

</text>

<text
x="630"
y="220"
font-family="monospace"
font-size="30"
font-weight="bold"
fill="{accent}"
filter="url(#glow)">

{following}

</text>

<circle
cx="900"
cy="215"
r="7"
fill="{accent}"
filter="url(#glow)"/>

<text
x="60"
y="255"
font-family="monospace"
font-size="10"
fill="{text}">

LAST UPDATE: {updated}

</text>

</svg>
'''

    with open(filename, "w", encoding="utf-8") as file:
        file.write(svg)


create_profile_svg(
    "assets/naoufal-dark.svg",
    "#0d1117",
    "#161b22",
    "#8b949e",
    "#00ff66"
)

create_profile_svg(
    "assets/naoufal-light.svg",
    "#ffffff",
    "#f6f8fa",
    "#57606a",
    "#16883a"
)


# ============================================================
# CLEANUP
# ============================================================

if os.path.exists(avatar_path):
    os.remove(avatar_path)


print("Naoufal profile assets generated successfully.")
print("Generated:")
print(" - assets/avatar-ascii.svg")
print(" - assets/naoufal-dark.svg")
print(" - assets/naoufal-light.svg")

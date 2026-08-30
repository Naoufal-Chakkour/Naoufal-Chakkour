import os
import urllib.request
import json
from datetime import datetime

USERNAME = "Naoufal-Chakkour"

TOKEN = os.environ.get("GH_TOKEN", "")

url = f"https://api.github.com/users/{USERNAME}"

headers = {
    "User-Agent": "Naoufal-GitHub-Profile"
}

if TOKEN:
    headers["Authorization"] = f"Bearer {TOKEN}"

request = urllib.request.Request(url, headers=headers)

with urllib.request.urlopen(request) as response:
    data = json.loads(response.read().decode())

repos = data.get("public_repos", 0)
followers = data.get("followers", 0)
following = data.get("following", 0)

updated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")


def create_svg(filename, background, card, text, accent):

    svg = f'''<svg width="1000" height="300"
viewBox="0 0 1000 300"
xmlns="http://www.w3.org/2000/svg">

<defs>

<filter id="glow"
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


os.makedirs("assets", exist_ok=True)

create_svg(
    "assets/naoufal-dark.svg",
    "#0d1117",
    "#161b22",
    "#8b949e",
    "#00ff66"
)

create_svg(
    "assets/naoufal-light.svg",
    "#ffffff",
    "#f6f8fa",
    "#57606a",
    "#16883a"
)

print("Profile SVGs generated successfully.")

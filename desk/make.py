# Builds the profile README's pictures: python3 desk/make.py
#   desk-dark.svg / desk-light.svg  the banner at the top: the ID card from salroid.me on its lanyard, and a terminal,
#                                   on GitHub's own canvas and colours (Primer) so it reads as part of the page
#   focus-<theme>.svg               the wide "current focus" card under the intro
#   project-Filmy-<theme>.svg       the Filmy card from salroid.me's Projects page, linked to the repo. Other repos aren't drawn: GitHub's
#                                   pinned repos show below the README.
#   skills-<theme>.svg              the toolbox: groups of chips
#   numbers-<theme>.svg             GitHub highlights as stat tiles
#   contact-<key>-<theme>.svg       one pill per way to reach salroid; the README wraps each in its link
# Star, fork and join-year figures are read from GitHub on each run, so run this again to refresh them.
# Anything worth clicking is also in the README as text: GitHub shows these as images, with no links.
# id.png is salroid.me's card, the full-colour original (site/public/img/id_v.png, 675 px): the CDN copy is
# palette-reduced and bands the photo.
import base64, json, pathlib, subprocess
here = pathlib.Path(__file__).parent
card = base64.b64encode((here / 'id.png').read_bytes()).decode()

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
REDUCED = '@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }'

THEMES = {
    'dark':  dict(bg='#0d1117', dot='#21262d', win='#161b22', bar='#1c2128', line='#30363d', fg='#e6edf3',
                  mute='#8b949e', green='#3fb950', blue='#58a6ff', orange='#ff6a3d', shade=.6),
    'light': dict(bg='#ffffff', dot='#e6e9ed', win='#f6f8fa', bar='#eaeef2', line='#d0d7de', fg='#1f2328',
                  mute='#59636e', green='#1a7f37', blue='#0969da', orange='#d94d1a', shade=.18),
}


def banner(t):
    c = THEMES[t]
    W, H = 1000, 450
    prompt = f'<tspan fill="{c["green"]}">~</tspan> <tspan fill="{c["blue"]}">$</tspan>'
    lines = [
        (f'{prompt} whoami', c['fg']),
        ('Sajal Gupta, a.k.a. salroid', c['fg']),
        ('builds, designs and writes', c['mute']),
        ('', None),
        (f'{prompt} cat now.txt', c['fg']),
        ('building Lumen: 15 apps on one core', c['mute']),
        ('', None),
        (f'{prompt} <tspan class="blink" fill="{c["orange"]}">▍</tspan>', c['fg']),
    ]
    text = ''.join(f'<text x="30" y="{92 + i * 32}" fill="{col}">{s}</text>' for i, (s, col) in enumerate(lines) if s)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<title>salroid: Sajal Gupta's ID card and a terminal</title>
<defs>
  <style>
    .sway {{ animation: sway 7s ease-in-out infinite; transform-origin: 200px -40px; }}
    @keyframes sway {{ 0%,100% {{ transform: rotate(-2.5deg); }} 50% {{ transform: rotate(1deg); }} }}
    .blink {{ animation: blink 1.1s steps(1) infinite; }} @keyframes blink {{ 50% {{ opacity: 0; }} }}
    {REDUCED}
  </style>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="{c['dot']}"/></pattern>
  <filter id="lift" x="-30%" y="-20%" width="160%" height="150%"><feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#000" flood-opacity="{c['shade']}"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="{c['bg']}"/>
<rect width="{W}" height="{H}" fill="url(#dots)"/>

<g transform="translate(430 64)" filter="url(#lift)">
  <rect width="470" height="330" rx="10" fill="{c['win']}" stroke="{c['line']}"/>
  <path d="M0 10 a10 10 0 0 1 10 -10 h450 a10 10 0 0 1 10 10 v26 h-470z" fill="{c['bar']}"/>
  <line x1="0" x2="470" y1="36" y2="36" stroke="{c['line']}"/>
  <circle cx="20" cy="18" r="6" fill="#ff5f57"/><circle cx="40" cy="18" r="6" fill="#febc2e"/><circle cx="60" cy="18" r="6" fill="#28c840"/>
  <text x="235" y="23" font-family="{MONO}" font-size="12.5" fill="{c['mute']}" text-anchor="middle">salroid — zsh</text>
  <g font-family="{MONO}" font-size="18">{text}</g>
</g>

<g class="sway" filter="url(#lift)">
  <image x="103" y="-103" width="194" height="505" href="data:image/png;base64,{card}"/>
</g>
</svg>'''


# ---------- current focus ----------
FOCUS = ['Lumen', 'Agents + MCP', 'ESP32 desk gadgets', 'Mobile-first UI']

def focus(t):
    c = THEMES[t]
    W, H = 1000, 128
    # no columns: spread the four items across the card by the width of their text (~11 px a character at 20 px)
    widths = [30 + len(a) * 11 for a in FOCUS]
    gap = (W - 88 - sum(widths)) / (len(FOCUS) - 1)
    cols, x = '', 44
    for i, (a, w) in enumerate(zip(FOCUS, widths)):
        cols += (f'<g transform="translate({x:.0f} 84)"><text font-family="{MONO}" font-size="13" fill="{c["orange"]}">0{i + 1}</text>'
                 f'<text x="30" font-family="{SANS}" font-size="20" font-weight="600" fill="{c["fg"]}">{a}</text></g>')
        if i:
            cols += f'<line x1="{x - gap / 2:.0f}" x2="{x - gap / 2:.0f}" y1="66" y2="94" stroke="{c["line"]}"/>'
        x += w + gap
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<title>Current focus: {', '.join(FOCUS)}</title>
<defs><linearGradient id="wash" x1="0" x2="1"><stop offset="0" stop-color="{c['orange']}" stop-opacity=".10"/><stop offset=".55" stop-color="{c['orange']}" stop-opacity="0"/></linearGradient></defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{c['win']}" stroke="{c['line']}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="url(#wash)"/>
<rect x="0" y="20" width="4" height="{H - 40}" rx="2" fill="{c['orange']}"/>
<circle cx="50" cy="38" r="5" fill="{c['green']}"><animate attributeName="opacity" values="1;.25;1" dur="2.4s" repeatCount="indefinite"/></circle>
<text x="66" y="43" font-family="{MONO}" font-size="14" letter-spacing="3" fill="{c['fg']}">CURRENT FOCUS</text>
{cols}
</svg>'''


# ---------- projects ----------
def github(path):
    # curl, not urllib: python.org's macOS Python ships without CA certificates
    out = subprocess.run(['curl', '-sf', '--max-time', '20', 'https://api.github.com/' + path],
                         capture_output=True, check=True).stdout
    return json.loads(out)

def repos():
    return {r['name']: r for r in github('users/salRoid/repos?per_page=100')}

STAR = 'M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z'
def filmy_card(t, r):
    # The card from salroid.me's Projects page: the phone on an orange panel, cut off at the bottom edge, and the
    # text beside it, in the site's own fonts (Newsreader for the title and numbers, Space Grotesk for the rest).
    c = THEMES[t]
    W, H, SPLIT = 1000, 460, 500
    b64 = lambda f: base64.b64encode((here / f).read_bytes()).decode()
    serif, sans = "Newsreader, Georgia, 'Times New Roman', serif", "'Space Grotesk', " + SANS
    desc = ['Discover, track and explore movies and TV shows.', 'Built for Android with clean architecture —',
            'thousands of installs and a design language', 'that puts content before chrome.']
    pills, x = '', 548
    for label, solid in (('Featured', 1), ('Android', 0), ('Kotlin', 0)):
        w = len(label) * 7.4 + 28
        fill, stroke, col = (f'{c["orange"]}22', 'none', c['orange']) if solid else ('none', c['line'], c['mute'])
        pills += (f'<rect x="{x}" y="56" width="{w:.0f}" height="30" rx="15" fill="{fill}" stroke="{stroke}"/>'
                  f'<text x="{x + w / 2:.1f}" y="76" font-family="{sans}" font-size="13" font-weight="500" fill="{col}" text-anchor="middle">{label}</text>')
        x += w + 8
    xs, gap = [], 548
    for n in (f"{r['stargazers_count']:,}★", str(r['forks_count']), '10k+'):
        xs.append(gap); gap += max(len(n) * 16, 70) + 36  # serif figures are ~16 px wide at 30 px
    stats = ''.join(f'<text x="{xs[i]}" y="330" font-family="{serif}" font-size="30" fill="{c["orange"]}">{n}</text>'
                    f'<text x="{xs[i]}" y="354" font-family="{sans}" font-size="11" letter-spacing="2" fill="{c["mute"]}">{l}</text>'
                    for i, (n, l) in enumerate([(f"{r['stargazers_count']:,}★", 'STARS'), (str(r['forks_count']), 'FORKS'), ('10k+', 'INSTALLS')]))
    lines = ''.join(f'<text x="548" y="{190 + i * 25}" font-family="{sans}" font-size="15.5" fill="{c["mute"]}">{d}</text>' for i, d in enumerate(desc))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<title>Filmy, your movie guide: {r['stargazers_count']} stars, {r['forks_count']} forks, 10k+ installs</title>
<defs>
  <style>
    @font-face {{ font-family: Newsreader; src: url(data:font/woff2;base64,{b64('newsreader.woff2')}) format('woff2'); font-weight: 200 800; }}
    @font-face {{ font-family: 'Space Grotesk'; src: url(data:font/woff2;base64,{b64('spacegrotesk.woff2')}) format('woff2'); font-weight: 300 700; }}
  </style>
  <clipPath id="card"><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18"/></clipPath>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="{c['win']}"/>
<g clip-path="url(#card)">
  <rect width="{SPLIT}" height="{H}" fill="#E0683A"/>
  <image x="64" y="26" width="372" height="{H - 26}" preserveAspectRatio="xMidYMax meet" href="data:image/png;base64,{b64('filmy.png')}"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{c['orange']}" stroke-opacity=".55"/>
{pills}
<text x="548" y="148" font-family="{serif}" font-size="36" fill="{c['fg']}">Filmy — your movie guide</text>
{lines}
{stats}
<rect x="548.5" y="388.5" width="188" height="44" rx="22" fill="none" stroke="{c['line']}"/>
<text x="574" y="416" font-family="{sans}" font-size="15" font-weight="500" fill="{c['fg']}">View on GitHub</text>
<path d="M707 421 l9 -9 M708 412 h8 v8" stroke="{c['fg']}" stroke-width="1.7" fill="none" stroke-linecap="round"/>
</svg>'''


# ---------- cards with a header line, like the focus card ----------
def framed(c, W, H, label, title, body, note=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<title>{title}</title>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{c['win']}" stroke="{c['line']}"/>
<text x="44" y="43" font-family="{MONO}" font-size="14" letter-spacing="3" fill="{c['fg']}">{label}</text>
<text x="{W - 44}" y="43" font-family="{MONO}" font-size="13" fill="{c['mute']}" text-anchor="end">{note}</text>
{body}
</svg>'''

SKILLS = [
    ('LANGUAGES', ['TypeScript', 'JavaScript', 'Java', 'Kotlin', 'Python', 'C++']),
    ('FRONTEND', ['React', 'Next.js', 'React Native', 'Framer Motion', 'TipTap']),
    ('BACKEND', ['Node.js', 'Express', 'PostgreSQL', 'Prisma', 'AWS', 'Docker']),
    ('PLATFORM', ['ServiceNow', 'Android', 'MCP', 'Claude', 'ESP32']),
]

def skills(t):
    c = THEMES[t]
    W, CH, SIZE = 1000, 8.43, 14  # monospace: every character is .6em wide, so a chip fits its word exactly
    rows = []
    for i, (label, chips) in enumerate(SKILLS):
        y = 70 + i * 48
        out = f'<text x="44" y="{y + 20}" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{c["orange"]}">{label}</text>'
        x = 200
        for chip in chips:
            w = len(chip) * CH + 28
            out += (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="{c["bg"]}" stroke="{c["line"]}"/>'
                    f'<text x="{x + w / 2:.1f}" y="{y + 20}" font-family="{MONO}" font-size="{SIZE}" fill="{c["fg"]}" text-anchor="middle">{chip}</text>')
            x += w + 10
        rows.append(out)
    H = 70 + len(SKILLS) * 48 + 18
    title = 'Toolbox: ' + '; '.join(f'{l.title()}: {", ".join(ch)}' for l, ch in SKILLS)
    return framed(c, W, H, 'TOOLBOX', title, ''.join(rows))

def contributions(since):
    # every year's contribution graph (the same data as the calendar on the profile), summed
    import re, datetime
    total = 0
    for y in range(int(since), datetime.date.today().year + 1):
        html = subprocess.run(['curl', '-s', f'https://github.com/users/salRoid/contributions?from={y}-01-01&to={y}-12-31'],
                              capture_output=True, text=True).stdout
        total += sum(int(n) for n in re.findall(r'>(\d+) contributions? on', html))
    return total

def numbers(t, gh, user):
    c = THEMES[t]
    W, H = 1000, 160
    own = [r for r in gh.values() if not r['fork']]
    tiles = [
        (f"{sum(r['stargazers_count'] for r in own):,}", 'stars across my repos'),
        (f"{gh['Filmy']['forks_count']}", 'forks of Filmy'),
        (user['created_at'][:4], 'the year I joined GitHub'),
        (f"{contributions(user['created_at'][:4]):,}", 'contributions, all time'),
    ]
    body = ''.join(f'''{f'<line x1="{x - 22}" x2="{x - 22}" y1="68" y2="128" stroke="{c["line"]}"/>' if i else ''}
<text x="{x}" y="102" font-family="{SANS}" font-size="34" font-weight="700" fill="{c['orange'] if i == 0 else c['fg']}">{n}</text>
<text x="{x}" y="126" font-family="{SANS}" font-size="15" fill="{c['mute']}">{label}</text>'''
                   for i, (n, label), x in ((i, tl, 44 + i * 236) for i, tl in enumerate(tiles)))
    title = 'GitHub highlights: ' + '; '.join(f'{n} {l}' for n, l in tiles)
    return framed(c, W, H, 'BY THE NUMBERS', title, body)

# ---------- get in touch: one tile each, so every one can be its own link ----------
CONTACTS = [  # key, label, shown text, icon (24-unit paths; f = filled, s = stroked)
    ('web', 'WEBSITE', 'salroid.me', 's', '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>'),
    ('mail', 'EMAIL', 'gupta.sajal631@gmail.com', 's', '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 7 8.5-7"/>'),
    ('x', 'X', '@salRoid', 'f', '<path d="M18.9 1.15h3.68l-8.04 9.19L24 22.85h-7.4l-5.8-7.59-6.64 7.59H.47l8.6-9.83L0 1.15h7.6l5.24 6.93ZM17.6 20.64h2.04L6.49 3.24H4.3Z"/>'),
    ('instagram', 'INSTAGRAM', '@sal_roid', 's', '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" fill="currentColor" stroke="none"/>'),
    ('linkedin', 'LINKEDIN', 'in/salroid', 's', '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10.5V16M8 7.6v.1M11.5 16v-5.5M11.5 13c0-1.6 1-2.6 2.4-2.6s2.1.9 2.1 2.6V16"/>'),
    ('youtube', 'YOUTUBE', '@salroid', 's', '<rect x="2.5" y="5.5" width="19" height="13" rx="4"/><path d="m10 9.2 5 2.8-5 2.8z" fill="currentColor"/>'),
]

def contact(t, label, text, kind, icon):
    # a pill sized to its text: monospace, so the width is exact (.6em a character)
    c = THEMES[t]
    H, size = 40, 14
    name = 'salroid.me' if label == 'WEBSITE' else label.title().replace('Linkedin', 'LinkedIn').replace('Youtube', 'YouTube')
    W = round(52 + len(name) * size * .6 + 18)
    style = (f'fill="{c["fg"]}"' if kind == 'f' else f'fill="none" stroke="{c["fg"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"')
    scale = (.6 if kind == 'f' else .75)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<title>{label.title()}: {text}</title>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="{H / 2}" fill="{c['win']}" stroke="{c['line']}"/>
<g color="{c['fg']}" {style} transform="translate({22 - 12 * scale} {20 - 12 * scale}) scale({scale})">{icon}</g>
<text x="42" y="25" font-family="{MONO}" font-size="{size}" fill="{c['fg']}">{name}</text>
</svg>'''

for t in THEMES:
    (here / f'desk-{t}.svg').write_text(banner(t))
    for key, label, text, kind, icon in CONTACTS:
        (here / f'contact-{key}-{t}.svg').write_text(contact(t, label, text, kind, icon))
for t in THEMES:
    (here / f'focus-{t}.svg').write_text(focus(t))
gh = repos()
user = github('users/salRoid')
for t in THEMES:
    (here / f'project-Filmy-{t}.svg').write_text(filmy_card(t, gh['Filmy']))
    (here / f'skills-{t}.svg').write_text(skills(t))
    (here / f'numbers-{t}.svg').write_text(numbers(t, gh, user))
print('ok')

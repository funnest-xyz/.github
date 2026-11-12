"""Usage: python scripts/make_banner.py profile/banner.svg

Builds profile/banner.svg: the Funnest mark and line on the left, a real-looking chart on the right
(candles from a seeded random walk with an uptrend, volume, a smooth moving average with an area
fill, grid and price scale, the last price tag, the yellow peak). Deterministic: same file every run."""
import math
import random
import sys

OUT = sys.argv[1]
W, H = 1280, 400
random.seed(20261112)

# ── price series ────────────────────────────────────────────────────
N = 60
bars = []
price = 100.0
for i in range(N):
    drift = 0.55 + 0.5 * math.sin(i / 9.0)  # waves on an uptrend
    if 30 <= i <= 38:
        drift = -1.1  # one pullback
    if i >= N - 5:
        drift = 1.6  # finish on a run to the high
    o = price
    c = o + drift + (abs(random.gauss(0, 0.6)) if i >= N - 5 else random.gauss(0, 1.5))
    h = max(o, c) + abs(random.gauss(0, 0.9))
    l = min(o, c) - abs(random.gauss(0, 0.9))
    v = 0.6 + abs(random.gauss(0, 0.45)) + (0.6 if abs(c - o) > 2 else 0)
    bars.append((o, h, l, c, v))
    price = c

# ── layout ──────────────────────────────────────────────────────────
X0, X1 = 700, 1190  # plot area (clear of the headline)
Y0, Y1 = 58, 286  # price area
VY0, VY1 = 302, 352  # volume area
lo = min(b[2] for b in bars)
hi = max(b[1] for b in bars)
pad = (hi - lo) * 0.08
lo, hi = lo - pad, hi + pad
step = (X1 - X0) / N
body = step * 0.58
y = lambda p: Y1 - (p - lo) / (hi - lo) * (Y1 - Y0)
x = lambda i: X0 + step * (i + 0.5)
vmax = max(b[4] for b in bars)

UP, DOWN = '#F04452', '#3182F6'
parts = []

# grid + price scale
last_y = None  # set below; labels too close to the last-price tag are skipped
for k in range(5):
    p = lo + (hi - lo) * (k + 0.5) / 5
    yy = y(p)
    if abs(yy - y(bars[-1][3])) < 16:
        parts.append(f'<line x1="{X0 - 20}" y1="{yy:.1f}" x2="{X1}" y2="{yy:.1f}" stroke="#FFFFFF" stroke-opacity="0.06"/>')
        continue
    parts.append(f'<line x1="{X0 - 20}" y1="{yy:.1f}" x2="{X1}" y2="{yy:.1f}" stroke="#FFFFFF" stroke-opacity="0.06"/>')
    parts.append(f'<text x="{X1 + 12}" y="{yy + 4:.1f}" fill="#6F6A86" font-family="Inter, \'Segoe UI\', sans-serif" font-size="11">{p * 712:,.0f}</text>')
for k in range(1, 6):
    xx = X0 + (X1 - X0) * k / 6
    parts.append(f'<line x1="{xx:.1f}" y1="{Y0 - 10}" x2="{xx:.1f}" y2="{VY1}" stroke="#FFFFFF" stroke-opacity="0.035"/>')

# moving average (20) with an area under it
ma = []
for i in range(N):
    w = bars[max(0, i - 19): i + 1]
    ma.append(sum(b[3] for b in w) / len(w))
pts = [(x(i), y(ma[i])) for i in range(N)]


def smooth(points):
    """Catmull-Rom → cubic Bézier."""
    d = f'M{points[0][0]:.1f} {points[0][1]:.1f}'
    for i in range(len(points) - 1):
        p0 = points[max(0, i - 1)]
        p1, p2 = points[i], points[i + 1]
        p3 = points[min(len(points) - 1, i + 2)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d


line = smooth(pts)
parts.append(f'<path d="{line} L{pts[-1][0]:.1f} {Y1} L{pts[0][0]:.1f} {Y1} Z" fill="url(#area)"/>')

# volume
for i, (o, h, l, c, v) in enumerate(bars):
    vh = (VY1 - VY0) * v / vmax
    col = UP if c >= o else DOWN
    parts.append(f'<rect x="{x(i) - body / 2:.1f}" y="{VY1 - vh:.1f}" width="{body:.1f}" height="{vh:.1f}" rx="1" fill="{col}" fill-opacity="0.32"/>')

# candles
for i, (o, h, l, c, v) in enumerate(bars):
    col = UP if c >= o else DOWN
    top, bot = y(max(o, c)), y(min(o, c))
    parts.append(f'<line x1="{x(i):.1f}" y1="{y(h):.1f}" x2="{x(i):.1f}" y2="{y(l):.1f}" stroke="{col}" stroke-width="1.2"/>')
    parts.append(f'<rect x="{x(i) - body / 2:.1f}" y="{top:.1f}" width="{body:.1f}" height="{max(1.2, bot - top):.1f}" rx="1" fill="{col}"/>')

# moving average on top, with a soft glow
parts.append(f'<path d="{line}" stroke="#8B6CFF" stroke-opacity="0.35" stroke-width="7" stroke-linecap="round" fill="none" filter="url(#blur)"/>')
parts.append(f'<path d="{line}" stroke="#A48BFF" stroke-width="2.4" stroke-linecap="round" fill="none"/>')

# the peak: yellow dot on the highest high
pk = max(range(N), key=lambda i: bars[i][1])
px, py = x(pk), y(bars[pk][1]) - 10
parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="13" fill="#FFD43B" fill-opacity="0.18"/>')
parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="#FFD43B"/>')

# last price: dashed line and tag
last = bars[-1][3]
ly = y(last)
lcol = UP if bars[-1][3] >= bars[-1][0] else DOWN
parts.append(f'<line x1="{X0 - 20}" y1="{ly:.1f}" x2="{X1}" y2="{ly:.1f}" stroke="{lcol}" stroke-opacity="0.7" stroke-dasharray="3 4"/>')
parts.append(f'<rect x="{X1 + 4}" y="{ly - 11:.1f}" width="64" height="22" rx="5" fill="{lcol}"/>')
parts.append(f'<text x="{X1 + 36}" y="{ly + 4:.1f}" text-anchor="middle" fill="#FFFFFF" font-family="Inter, \'Segoe UI\', sans-serif" font-size="11.5" font-weight="700">{last * 712:,.0f}</text>')

chart = '\n    '.join(parts)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="funnest — Every moment of investing, more fun">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop stop-color="#121019"/>
      <stop offset="1" stop-color="#1A1630"/>
    </linearGradient>
    <radialGradient id="glow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(1000 120) rotate(90) scale(300 460)">
      <stop stop-color="#6C4DFF" stop-opacity="0.30"/>
      <stop offset="1" stop-color="#6C4DFF" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="mark" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse">
      <stop stop-color="#8B6CFF"/>
      <stop offset="1" stop-color="#5A3BF0"/>
    </linearGradient>
    <linearGradient id="area" x1="0" y1="{Y0}" x2="0" y2="{Y1}" gradientUnits="userSpaceOnUse">
      <stop stop-color="#8B6CFF" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#8B6CFF" stop-opacity="0"/>
    </linearGradient>
    <!-- The chart fades in from the left, under the words. -->
    <linearGradient id="fade" x1="{X0 - 30}" y1="0" x2="{X0 + 110}" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="1" stop-color="#FFFFFF"/>
    </linearGradient>
    <mask id="fadeMask" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <rect width="{W}" height="{H}" fill="url(#fade)"/>
    </mask>
    <filter id="blur" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="4"/></filter>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="24"/></clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#glow)"/>
    <g mask="url(#fadeMask)">
    {chart}
    </g>
  </g>

  <!-- Mark + wordmark -->
  <g transform="translate(88 96)">
    <svg width="60" height="60" viewBox="0 0 32 32">
      <rect width="32" height="32" rx="9" fill="url(#mark)"/>
      <path d="M7 13.5C9.5 21.5 17 23.5 23.4 11.2" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>
      <circle cx="24.6" cy="8.6" r="2.9" fill="#FFD43B"/>
    </svg>
    <text x="78" y="45" fill="#FFFFFF" font-family="Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif" font-size="44" font-weight="800" letter-spacing="-1.5">funnest</text>
  </g>

  <text x="88" y="232" fill="#FFFFFF" font-family="Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif" font-size="40" font-weight="800" letter-spacing="-1.2">Every moment of investing,</text>
  <text x="88" y="280" fill="#FFFFFF" font-family="Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif" font-size="40" font-weight="800" letter-spacing="-1.2">more <tspan fill="#FFD43B">fun</tspan>.</text>
  <text x="88" y="330" fill="#9B96B3" font-family="Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif" font-size="19" font-weight="500">Charts, paper trading and a community, in one nest</text>
</svg>
'''
open(OUT, 'w', encoding='utf-8', newline='\n').write(svg)
print('ok', len(svg))

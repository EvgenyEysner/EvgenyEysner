#!/usr/bin/env python3
"""Generate dark.svg and light.svg GitHub profile hero banners."""

from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent
W, H = 1180, 610

PHRASES = [
    "Full Stack Developer",
    "Python & Django",
    "FastAPI",
    "React",
    "Linux & DevOps",
]

SKILLS = [
    "Python",
    "Django",
    "FastAPI",
    "React",
    "JavaScript",
    "Docker",
    "PostgreSQL",
    "Linux",
    "Git",
    "CI/CD",
    "DevOps",
]

INFO = [
    ("LOCATION", "Oldenburg, Germany", "pin"),
    ("STUDIO", "softeis.dev", "studio"),
    ("FOCUS", "Python · Django · FastAPI", "spark"),
    ("PORTFOLIO", "https://softeis.dev", "link"),
    ("EMAIL", "evgeny.eysner@gmail.com", "mail"),
]


def make_ascii(cols: int = 46, rows: int = 30) -> list[str]:
    """Identity monogram for Evgeny Eysner — EE in a cyber-terminal scan."""
    block = [
        "  .**************+*=  -****************-",
        "  -@@@@@@@@@@@@@@@@%  *@@@@@@@@@@@@@@@@+",
        "  :@%@@@%#%%%%%%%#%*  +@%@@@%#%%%%%#%%%=",
        "  :@@@@@+             +@@@@@:",
        "  :@@@@@+             +@@@@@:",
        "  :@@@@@+             +@@@@@:",
        "  :@@@@@#+++++++      +@@@@@*++++++-",
        "  :@@@@@@@@@@@@%.     +@@@@@@@@@@@@*",
        "  :@@@@@%%%%%%%#.     +@@@@@%%%%%%%+",
        "  :@@@@@+             +@@@@@-",
        "  :@@@@@+             +@@@@@:",
        "  :@@@@@+             +@@@@@:",
        "  :@@@@@#++++++++++=  +@%@@@*++++++++++-",
        "  :@@@@@@@@@@@@@@@@%  +@@@@@@@@@@@@@@@@+",
        "  :%%%%%%%%%%%%%%%%#  +%%%%%%%%%%%%%%%%=",
        "",
        "       Evgeny Eysner",
        "       softeis.dev | Oldenburg",
    ]
    width = max(len(s) for s in block)
    return [s.ljust(width) for s in block]


DARK = {
    "bg": "#030712",
    "panel": "#0F172A",
    "panel_op": 0.82,
    "border": "#FFFFFF",
    "border_op": 0.08,
    "text": "#F8FAFC",
    "muted": "#94A3B8",
    "a1": "#7C3AED",
    "a2": "#22D3EE",
    "a3": "#10B981",
    "ascii1": "#67E8F9",
    "ascii2": "#A78BFA",
    "ascii3": "#7C3AED",
    "glow_b": "#2563EB",
    "glow_p": "#7C3AED",
    "glow_e": "#10B981",
    "orb_op": 0.42,
    "noise_op": 0.055,
    "grid_op": 0.045,
    "scan_op": 0.14,
    "glass_op": 0.09,
    "pill_fill_op": 0.10,
    "pill_stroke_op": 0.22,
    "shadow_op": 0.55,
    "titlebar": "#020617",
    "dot_live": "#22D3EE",
    "particle": ["#22D3EE", "#A78BFA", "#34D399"],
    "crt_op": 0.035,
    "cursor": "#22D3EE",
    "soft_white": "#FFFFFF",
    "glow_std": 18,
    "icon_op": 0.9,
}

LIGHT = {
    "bg": "#FFFFFF",
    "panel": "#F8FAFC",
    "panel_op": 0.88,
    "border": "#0F172A",
    "border_op": 0.08,
    "text": "#0F172A",
    "muted": "#475569",
    "a1": "#2563EB",
    "a2": "#06B6D4",
    "a3": "#10B981",
    "ascii1": "#1D4ED8",
    "ascii2": "#0891B2",
    "ascii3": "#0E7490",
    "glow_b": "#93C5FD",
    "glow_p": "#C4B5FD",
    "glow_e": "#6EE7B7",
    "orb_op": 0.28,
    "noise_op": 0.03,
    "grid_op": 0.05,
    "scan_op": 0.08,
    "glass_op": 0.55,
    "pill_fill_op": 0.06,
    "pill_stroke_op": 0.14,
    "shadow_op": 0.10,
    "titlebar": "#F1F5F9",
    "dot_live": "#06B6D4",
    "particle": ["#2563EB", "#06B6D4", "#10B981"],
    "crt_op": 0.025,
    "cursor": "#2563EB",
    "soft_white": "#FFFFFF",
    "glow_std": 14,
    "icon_op": 0.85,
}


def xml(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def lerp_keys(pairs: list[tuple[float, float]]) -> tuple[str, str]:
    """pairs of (time 0-1, value) -> keyTimes, values. Times must be strictly increasing."""
    cleaned: list[tuple[float, float]] = []
    for t, v in pairs:
        t = round(min(1.0, max(0.0, t)), 5)
        if cleaned and t <= cleaned[-1][0]:
            t = round(min(1.0, cleaned[-1][0] + 0.00012), 5)
            if t <= cleaned[-1][0]:
                cleaned[-1] = (cleaned[-1][0], v)
                continue
        cleaned.append((t, v))
    if cleaned[-1][0] < 1.0:
        cleaned.append((1.0, cleaned[-1][1]))
    times, vals = zip(*cleaned)
    return ";".join(f"{t:.5f}" for t in times), ";".join(f"{v:.2f}" for v in vals)


def typewriter_clip(phrases: list[str], char_w: float, dur_each: float = 4.6):
    n = len(phrases)
    total = n * dur_each
    pts_w: list[tuple[float, float]] = [(0.0, 0.0)]
    pts_x: list[tuple[float, float]] = [(0.0, 0.0)]
    for i, phrase in enumerate(phrases):
        base = i / n
        span = 1 / n
        full = len(phrase) * char_w + 2
        t_type_end = base + span * 0.38
        t_hold_end = base + span * 0.70
        t_del_end = base + span * 0.88
        t_gap_end = base + span
        pts_w += [
            (base + 0.0008, 0.0),
            (t_type_end, full),
            (t_hold_end, full),
            (t_del_end, 0.0),
            (t_gap_end - 0.0008, 0.0),
        ]
        pts_x += [
            (base + 0.0008, 0.0),
            (t_type_end, full),
            (t_hold_end, full),
            (t_del_end, 0.0),
            (t_gap_end - 0.0008, 0.0),
        ]
    pts_w.append((1.0, 0.0))
    pts_x.append((1.0, 0.0))
    return total, lerp_keys(pts_w), lerp_keys(pts_x)


def icon_path(kind: str) -> str:
    if kind == "pin":
        return "M7 3.2C4.5 3.2 2.5 5.2 2.5 7.7c0 3.6 4.5 8.6 4.5 8.6s4.5-5 4.5-8.6C11.5 5.2 9.5 3.2 7 3.2zm0 5.1A1.6 1.6 0 1 1 7 5.1a1.6 1.6 0 0 1 0 3.2z"
    if kind == "studio":
        return "M2.4 11.8V5.6L7 3.1l4.6 2.5v6.2H2.4zM4.2 7.2h2.1v2.1H4.2zM7.7 7.2h2.1v2.1H7.7z"
    if kind == "spark":
        return "M7 1.4 8.1 5.2 12 6.4 8.1 7.6 7 11.4 5.9 7.6 2 6.4l3.9-1.2L7 1.4z"
    if kind == "link":
        return "M5.2 9.2 9.2 5.2M5.6 5.2h3.6V8.8"
    if kind == "mail":
        return "M1.8 4.2h10.4v7.2H1.8zM1.8 4.2 7 8.1 12.2 4.2"
    return ""


def social_icon(name: str) -> str:
    if name == "github":
        return (
            "M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.21 11.39.6.11.82-.26.82-.58"
            " 0-.28-.01-1.02-.02-2-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.33-1.76-1.33-1.76"
            "-1.09-.74.08-.73.08-.73 1.2.09 1.84 1.24 1.84 1.24 1.07 1.83 2.8 1.3 3.49 1 .11-.78.42-1.3.76-1.6"
            "-2.66-.3-5.46-1.33-5.46-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.18 0 0 1.01-.32 3.3 1.23"
            " .96-.27 1.98-.4 3-.4s2.04.13 3 .4c2.29-1.55 3.3-1.23 3.3-1.23.66 1.66.24 2.88.12 3.18"
            " .77.84 1.24 1.91 1.24 3.22 0 4.61-2.81 5.62-5.48 5.92.43.37.81 1.1.81 2.22"
            " 0 1.6-.01 2.89-.01 3.29 0 .32.22.7.82.58C20.56 21.8 24 17.3 24 12 24 5.37 18.63 0 12 0z"
        )
    if name == "linkedin":
        return (
            "M20.45 0H3.55A3.55 3.55 0 0 0 0 3.55v16.9A3.55 3.55 0 0 0 3.55 24h16.9A3.55 3.55 0 0 0 24 20.45V3.55"
            "A3.55 3.55 0 0 0 20.45 0zM7.12 20.45H3.56V9h3.56v11.45zM5.34 7.43A2.06 2.06 0 1 1 5.34 3.3a2.06 2.06 0 0 1 0 4.13z"
            "M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.41v1.56h.05"
            "c.47-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28z"
        )
    if name == "web":
        return (
            "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 0c2.5 2.6 4 6.1 4 10s-1.5 7.4-4 10m0-20c-2.5 2.6-4 6.1-4 10s1.5 7.4 4 10"
            "M2 12h20"
        )
    return ""


def build(theme: dict, ascii_lines: list[str], mode: str) -> str:
    pad = 22
    gap = 18
    left_w = 430
    left_x, left_y = pad, pad
    left_h = H - pad * 2
    right_x = left_x + left_w + gap
    right_w = W - pad - right_x
    right_y, right_h = pad, left_h
    pr = 18

    ascii_fs = 16.2
    ascii_lh = 18.4
    ascii_cols = len(ascii_lines[0])
    ascii_rows = len(ascii_lines)
    ascii_w = round(ascii_cols * ascii_fs * 0.60, 2)
    ascii_h = round(ascii_rows * ascii_lh, 2)
    ascii_ox = round(left_x + (left_w - ascii_w) / 2, 2)
    ascii_oy = round(left_y + 54 + (left_h - 54 - 46 - ascii_h) / 2, 2)

    role_fs = 18
    role_cw = role_fs * 0.603
    total_dur, (kt_w, kv_w), (kt_x, kv_x) = typewriter_clip(PHRASES, role_cw)
    y_prompt = right_y + 72
    y_hi = right_y + 104
    y_name = right_y + 144
    y_role = right_y + 180
    y_div1 = right_y + 204
    y_info = right_y + 230
    info_gap = 26
    y_skills_lbl = right_y + 372
    y_pills = right_y + 390
    y_social = right_y + right_h - 50

    phrase_opacity = []
    nph = len(PHRASES)
    for i in range(nph):
        slot0 = i / nph
        slot1 = (i + 1) / nph
        pts: list[tuple[float, float]] = []

        def add(t: float, v: float) -> None:
            t = round(min(1.0, max(0.0, t)), 5)
            if pts and abs(pts[-1][0] - t) < 0.00015:
                pts[-1] = (pts[-1][0], v)
                return
            pts.append((t, v))

        add(0.0, 0)
        add(slot0, 0)
        add(slot0 + 0.0012, 1)
        add(slot1 - 0.0012, 1)
        add(slot1, 0)
        add(1.0, 0)
        phrase_opacity.append(lerp_keys(pts))

    # discrete ASCII reveal heights
    reveal_vals = ";".join(str(round((i + 1) * ascii_lh, 2)) for i in range(ascii_rows))
    reveal_dur = round(ascii_rows * 0.085, 2)
    cursor_ys = ";".join(str(round(i * ascii_lh, 2)) for i in range(ascii_rows))

    # particles
    particles = []
    for i in range(16):
        ang = i * 2.3
        x0 = 80 + (i * 73) % 1020
        y0 = 40 + (i * 97) % 530
        x1 = (x0 + 140 * math.cos(ang)) % W
        y1 = 30 + (y0 + 90 * math.sin(ang * 1.3)) % (H - 40)
        x2 = (x0 + 80 * math.sin(ang)) % W
        y2 = 40 + (y0 + 120 * math.cos(ang)) % (H - 50)
        color = theme["particle"][i % 3]
        dur = 9 + (i % 7) * 1.4
        r = 1.1 + (i % 4) * 0.35
        particles.append((x0, y0, x1, y1, x2, y2, color, dur, r, 0.18 + (i % 5) * 0.07))

    pill_fs = 12
    pills = []
    px0 = right_x + 32
    per_row = 6
    gap_p = 8
    ph = 28
    widths = [round(len(label) * pill_fs * 0.62 + 26) for label in SKILLS]
    for row in range((len(SKILLS) + per_row - 1) // per_row):
        sl = slice(row * per_row, (row + 1) * per_row)
        x_cursor = px0
        y_cursor = y_pills + row * 36
        for i, (label, pw) in enumerate(zip(SKILLS[sl], widths[sl])):
            pills.append((label, x_cursor, y_cursor, pw, ph, row * per_row + i))
            x_cursor += pw + gap_p

    socials = [
        ("github", "GitHub"),
        ("linkedin", "LinkedIn"),
        ("web", "Portfolio"),
    ]

    t = theme
    parts: list[str] = []
    a = parts.append

    a(
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="1180" height="610" viewBox="0 0 1180 610" role="img" '
        f'aria-label="Evgeny Eysner — Full Stack Developer" preserveAspectRatio="xMidYMid meet">'
    )
    a("<title>Evgeny Eysner — Full Stack Developer</title>")
    a(
        f'<desc>Animated GitHub profile banner for Evgeny Eysner. {mode} theme. '
        f"Python, Django, FastAPI, React. Oldenburg, Germany.</desc>"
    )

    # ----- CSS hover only (SMIL handles all looping motion) -----
    a(
        """<style>
      .pill:hover { transform-box: fill-box; transform-origin: center; transform: scale(1.07); }
      .pill:hover .pill-bg { stroke-opacity: 0.55; }
      .social:hover { transform-box: fill-box; transform-origin: center; transform: scale(1.08); }
    </style>"""
    )

    a("<defs>")

    a(
        f'<clipPath id="canvas"><rect width="{W}" height="{H}" rx="28" ry="28"/></clipPath>'
    )
    a(
        f'<clipPath id="leftClip"><rect x="{left_x}" y="{left_y}" width="{left_w}" height="{left_h}" rx="{pr}"/></clipPath>'
    )
    a(
        f'<clipPath id="rightClip"><rect x="{right_x}" y="{right_y}" width="{right_w}" height="{right_h}" rx="{pr}"/></clipPath>'
    )
    a(
        f'<clipPath id="asciiReveal">'
        f'<rect x="-8" y="0" width="{ascii_w + 24}" height="0">'
        f'<animate attributeName="height" calcMode="discrete" values="{reveal_vals}" '
        f'dur="{reveal_dur}s" fill="freeze"/>'
        f"</rect></clipPath>"
    )

    role_x = right_x + 32
    role_y = y_role
    max_role_w = max(len(p) for p in PHRASES) * role_cw + 8
    a(
        f'<clipPath id="roleClip">'
        f'<rect id="roleClipRect" x="{role_x}" y="{role_y - 22}" width="0" height="32">'
        f'<animate attributeName="width" values="{kv_w}" keyTimes="{kt_w}" '
        f'dur="{total_dur}s" repeatCount="indefinite"/>'
        f"</rect></clipPath>"
    )

    a(
        f'<linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">'
        f'<stop offset="0%" stop-color="{t["a1"]}">'
        f'<animate attributeName="stop-color" values="{t["a1"]};{t["a2"]};{t["a3"]};{t["a1"]}" dur="8s" repeatCount="indefinite"/>'
        f"</stop>"
        f'<stop offset="50%" stop-color="{t["a2"]}">'
        f'<animate attributeName="stop-color" values="{t["a2"]};{t["a3"]};{t["a1"]};{t["a2"]}" dur="8s" repeatCount="indefinite"/>'
        f"</stop>"
        f'<stop offset="100%" stop-color="{t["a3"]}">'
        f'<animate attributeName="stop-color" values="{t["a3"]};{t["a1"]};{t["a2"]};{t["a3"]}" dur="8s" repeatCount="indefinite"/>'
        f"</stop>"
        f"</linearGradient>"
    )

    a(
        f'<linearGradient id="asciiGrad" x1="0%" y1="0%" x2="100%" y2="100%" gradientUnits="objectBoundingBox">'
        f'<stop offset="0%" stop-color="{t["ascii1"]}"/>'
        f'<stop offset="50%" stop-color="{t["ascii2"]}"/>'
        f'<stop offset="100%" stop-color="{t["ascii3"]}"/>'
        f'<animateTransform attributeName="gradientTransform" type="rotate" from="0 0.5 0.5" to="360 0.5 0.5" dur="14s" repeatCount="indefinite"/>'
        f"</linearGradient>"
    )

    a(
        f'<linearGradient id="shimmer" x1="-40%" y1="0%" x2="0%" y2="100%">'
        f'<stop offset="0%" stop-color="{t["a2"]}" stop-opacity="0"/>'
        f'<stop offset="50%" stop-color="{t["a2"]}" stop-opacity="0.85"/>'
        f'<stop offset="100%" stop-color="{t["a1"]}" stop-opacity="0"/>'
        f'<animate attributeName="x1" values="-40%;160%" dur="5.5s" repeatCount="indefinite"/>'
        f'<animate attributeName="x2" values="0%;200%" dur="5.5s" repeatCount="indefinite"/>'
        f"</linearGradient>"
    )

    a(
        f'<linearGradient id="glass" x1="0%" y1="0%" x2="0%" y2="100%">'
        f'<stop offset="0%" stop-color="{t["soft_white"]}" stop-opacity="{0.16 if mode == "dark" else 0.7}"/>'
        f'<stop offset="18%" stop-color="{t["soft_white"]}" stop-opacity="0"/>'
        f'<stop offset="100%" stop-color="{t["soft_white"]}" stop-opacity="0"/>'
        f"</linearGradient>"
    )

    a(
        f'<linearGradient id="glassSweep" x1="0%" y1="0%" x2="100%" y2="0%">'
        f'<stop offset="0%" stop-color="{t["soft_white"]}" stop-opacity="0"/>'
        f'<stop offset="50%" stop-color="{t["soft_white"]}" stop-opacity="{t["glass_op"]}"/>'
        f'<stop offset="100%" stop-color="{t["soft_white"]}" stop-opacity="0"/>'
        f'<animate attributeName="x1" values="-80%;120%" dur="7s" repeatCount="indefinite"/>'
        f'<animate attributeName="x2" values="0%;200%" dur="7s" repeatCount="indefinite"/>'
        f"</linearGradient>"
    )

    a(
        f'<linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{t["a2"]}" stop-opacity="0"/>'
        f'<stop offset="45%" stop-color="{t["a2"]}" stop-opacity="{t["scan_op"]}"/>'
        f'<stop offset="100%" stop-color="{t["a1"]}" stop-opacity="0"/>'
        f"</linearGradient>"
    )

    a(
        f'<radialGradient id="orbB" cx="50%" cy="50%" r="50%">'
        f'<stop offset="0%" stop-color="{t["glow_b"]}" stop-opacity="{t["orb_op"]}"/>'
        f'<stop offset="100%" stop-color="{t["glow_b"]}" stop-opacity="0"/>'
        f"</radialGradient>"
    )
    a(
        f'<radialGradient id="orbP" cx="50%" cy="50%" r="50%">'
        f'<stop offset="0%" stop-color="{t["glow_p"]}" stop-opacity="{t["orb_op"]}"/>'
        f'<stop offset="100%" stop-color="{t["glow_p"]}" stop-opacity="0"/>'
        f"</radialGradient>"
    )
    a(
        f'<radialGradient id="orbE" cx="50%" cy="50%" r="50%">'
        f'<stop offset="0%" stop-color="{t["glow_e"]}" stop-opacity="{t["orb_op"] * 0.85}"/>'
        f'<stop offset="100%" stop-color="{t["glow_e"]}" stop-opacity="0"/>'
        f"</radialGradient>"
    )

    a(
        f'<filter id="glow" x="-50%" y="-50%" width="200%" height="200%" color-interpolation-filters="sRGB">'
        f'<feGaussianBlur stdDeviation="3.2" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        f"</filter>"
    )
    a(
        f'<filter id="glowSoft" x="-80%" y="-80%" width="260%" height="260%" color-interpolation-filters="sRGB">'
        f'<feGaussianBlur stdDeviation="{6 if mode == "dark" else 4}" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        f"</filter>"
    )
    a(
        f'<filter id="asciiGlow" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">'
        f'<feGaussianBlur stdDeviation="{1.8 if mode == "dark" else 0.9}" result="b"/>'
        f'<feColorMatrix in="b" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 {0.7 if mode == "dark" else 0.35} 0"/>'
        f'<feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>'
        f"</filter>"
    )
    a(
        f'<filter id="panelShadow" x="-8%" y="-8%" width="116%" height="124%" color-interpolation-filters="sRGB">'
        f'<feDropShadow dx="0" dy="18" stdDeviation="16" flood-color="#020617" flood-opacity="{t["shadow_op"]}"/>'
        f"</filter>"
    )
    a(
        f'<filter id="noise" x="0" y="0" width="100%" height="100%">'
        f'<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch" result="n"/>'
        f'<feColorMatrix type="saturate" values="0"/>'
        f'<feComponentTransfer><feFuncA type="table" tableValues="0 {t["noise_op"] * 4}"/></feComponentTransfer>'
        f"</filter>"
    )
    a(
        f'<filter id="blurOrb" x="-20%" y="-20%" width="140%" height="140%">'
        f'<feGaussianBlur stdDeviation="{t["glow_std"]}"/>'
        f"</filter>"
    )

    a(
        f'<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">'
        f'<path d="M 28 0 L 0 0 0 28" fill="none" stroke="{t["a2"]}" stroke-opacity="{t["grid_op"]}" stroke-width="0.6"/>'
        f"</pattern>"
    )
    a(
        f'<pattern id="crt" width="1180" height="4" patternUnits="userSpaceOnUse">'
        f'<rect width="1180" height="1.2" fill="{t["text"]}" opacity="{t["crt_op"]}"/>'
        f'<animate attributeName="y" values="0;4" dur="0.18s" repeatCount="indefinite"/>'
        f"</pattern>"
    )

    # social symbols
    for key in ("github", "linkedin", "web"):
        fill = "none" if key == "web" else t["text"]
        stroke_extra = (
            f' fill="none" stroke="{t["text"]}" stroke-width="1.7" stroke-linecap="round"'
            if key == "web"
            else f' fill="{t["text"]}"'
        )
        a(f'<symbol id="ic-{key}" viewBox="0 0 24 24"><path d="{social_icon(key)}"{stroke_extra}/></symbol>')

    a("</defs>")

    # ================= SCENE =================
    a('<g clip-path="url(#canvas)">')
    a(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')

    # floating orbs
    a('<g filter="url(#blurOrb)" opacity="0.95">')
    a(
        f'<circle cx="210" cy="90" r="210" fill="url(#orbP)">'
        f'<animate attributeName="cx" values="210;290;170;210" dur="18s" repeatCount="indefinite"/>'
        f'<animate attributeName="cy" values="90;160;60;90" dur="22s" repeatCount="indefinite"/>'
        f"</circle>"
    )
    a(
        f'<circle cx="980" cy="140" r="230" fill="url(#orbB)">'
        f'<animate attributeName="cx" values="980;900;1040;980" dur="20s" repeatCount="indefinite"/>'
        f'<animate attributeName="cy" values="140;80;210;140" dur="16s" repeatCount="indefinite"/>'
        f"</circle>"
    )
    a(
        f'<circle cx="640" cy="520" r="200" fill="url(#orbE)">'
        f'<animate attributeName="cx" values="640;720;560;640" dur="24s" repeatCount="indefinite"/>'
        f'<animate attributeName="cy" values="520;470;560;520" dur="19s" repeatCount="indefinite"/>'
        f"</circle>"
    )
    a("</g>")

    a(f'<rect width="{W}" height="{H}" fill="url(#grid)" opacity="0.9"/>')
    a(f'<rect width="{W}" height="{H}" filter="url(#noise)"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#crt)" opacity="0.7"/>')

    # global sweeping scanline
    a(
        f'<rect x="0" y="-80" width="{W}" height="70" fill="url(#scanGrad)" opacity="0.7">'
        f'<animateTransform attributeName="transform" type="translate" values="0 -80; 0 700" dur="6.5s" repeatCount="indefinite"/>'
        f"</rect>"
    )

    # particles
    a('<g id="particles">')
    for i, (x0, y0, x1, y1, x2, y2, color, dur, r, op) in enumerate(particles):
        a(
            f'<circle r="{r:.2f}" fill="{color}" opacity="0">'
            f'<animateMotion path="M{x0:.1f},{y0:.1f} C{x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f} {x0:.1f},{y0:.1f}" '
            f'dur="{dur:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;{op:.2f};{op:.2f};0" dur="{dur:.1f}s" repeatCount="indefinite"/>'
            f"</circle>"
        )
    a("</g>")

    # ---------- LEFT PANEL ----------
    a(f'<g filter="url(#panelShadow)">')
    a(
        f'<rect x="{left_x}" y="{left_y}" width="{left_w}" height="{left_h}" rx="{pr}" '
        f'fill="{t["panel"]}" fill-opacity="{t["panel_op"]}"/>'
    )
    a("</g>")
    a(f'<g clip-path="url(#leftClip)">')
    a(
        f'<rect x="{left_x}" y="{left_y}" width="{left_w}" height="{left_h}" fill="url(#glass)"/>'
    )
    a(
        f'<rect x="{left_x}" y="{left_y}" width="{left_w}" height="{left_h}" fill="url(#glassSweep)" opacity="0.55"/>'
    )
    a(
        f'<rect x="{left_x}" y="{left_y}" width="{left_w}" height="1" fill="{t["soft_white"]}" opacity="{0.12 if mode == "dark" else 0.8}"/>'
    )
    a("</g>")

    # left HUD
    a(
        f'<text x="{left_x + 22}" y="{left_y + 32}" fill="{t["muted"]}" font-size="10.5" '
        f"""font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" """
        f'letter-spacing="2.4">IDENTITY_SCAN</text>'
    )
    a(
        f'<circle cx="{left_x + left_w - 58}" cy="{left_y + 28}" r="3.4" fill="{t["dot_live"]}" filter="url(#glow)">'
        f'<animate attributeName="opacity" values="1;0.25;1" dur="1.5s" repeatCount="indefinite"/>'
        f"</circle>"
    )
    a(
        f'<text x="{left_x + left_w - 48}" y="{left_y + 32}" fill="{t["dot_live"]}" font-size="10.5" '
        f"""font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" """
        f'letter-spacing="1.8">LIVE</text>'
    )

    # corner brackets around ASCII
    bx, by = ascii_ox - 10, ascii_oy - 8
    bw, bh = ascii_w + 20, ascii_h + 16
    brk = t["a2"]
    for x, y, dx1, dy1, dx2, dy2 in (
        (bx, by, 16, 0, 0, 16),
        (bx + bw, by, -16, 0, 0, 16),
        (bx, by + bh, 16, 0, 0, -16),
        (bx + bw, by + bh, -16, 0, 0, -16),
    ):
        a(
            f'<path d="M{x + dx1},{y} L{x},{y} L{x},{y + dy2}" fill="none" stroke="{brk}" '
            f'stroke-width="1.2" stroke-opacity="0.55" stroke-linecap="round"/>'
        )

    # ASCII group with float
    a(f'<g transform="translate({ascii_ox:.2f},{ascii_oy:.2f})">')
    a("<g>")
    a(
        '<animateTransform attributeName="transform" type="translate" '
        'values="0 0; 0 -6; 0 0; 0 5; 0 0" dur="8.5s" repeatCount="indefinite"/>'
    )
    a('<g clip-path="url(#asciiReveal)" filter="url(#asciiGlow)">')
    for i, line in enumerate(ascii_lines):
        y = (i + 1) * ascii_lh
        a(
            f'<text x="0" y="{y:.2f}" xml:space="preserve" fill="url(#asciiGrad)" '
            f'font-size="{ascii_fs}" font-weight="600" '
            f"""font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace">"""
            f"{xml(line)}</text>"
        )
    a("</g>")
    # scanline over ASCII
    a(
        f'<rect x="-6" y="-20" width="{ascii_w + 12:.1f}" height="28" fill="url(#scanGrad)">'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0 -30; 0 {ascii_h + 20:.1f}" dur="3.8s" repeatCount="indefinite"/>'
        f"</rect>"
    )
    # typing cursor
    a(
        f'<rect x="{ascii_w - 8:.1f}" y="0" width="6.5" height="{ascii_lh - 3:.1f}" fill="{t["cursor"]}" opacity="0.95" filter="url(#glow)">'
        f'<animate attributeName="y" calcMode="discrete" values="{cursor_ys}" dur="{reveal_dur}s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.46;0.5;1" dur="1.05s" repeatCount="indefinite"/>'
        f"</rect>"
    )
    a("</g></g>")

    # left footer
    a(
        f'<text x="{left_x + 22}" y="{left_y + left_h - 22}" fill="{t["muted"]}" font-size="10.5" '
        f"""font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" """
        f'letter-spacing="1.2">EE // SOFTEIS</text>'
    )
    a(
        f'<text x="{left_x + left_w - 22}" y="{left_y + left_h - 22}" fill="{t["a2"]}" font-size="10.5" '
        f"""font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" """
        f'text-anchor="end" opacity="0.85">v2.0</text>'
    )

    # left border + shimmer
    a(
        f'<rect x="{left_x + 0.6}" y="{left_y + 0.6}" width="{left_w - 1.2}" height="{left_h - 1.2}" rx="{pr - 0.4}" '
        f'fill="none" stroke="{t["border"]}" stroke-opacity="{t["border_op"]}" stroke-width="1"/>'
    )
    a(
        f'<rect x="{left_x + 0.6}" y="{left_y + 0.6}" width="{left_w - 1.2}" height="{left_h - 1.2}" rx="{pr - 0.4}" '
        f'fill="none" stroke="url(#shimmer)" stroke-width="1.15" stroke-opacity="0.7"/>'
    )

    # ---------- RIGHT PANEL (terminal) ----------
    a('<g filter="url(#panelShadow)">')
    a(
        f'<rect x="{right_x}" y="{right_y}" width="{right_w}" height="{right_h}" rx="{pr}" '
        f'fill="{t["panel"]}" fill-opacity="{t["panel_op"]}"/>'
    )
    a("</g>")

    # title bar
    a(f'<g clip-path="url(#rightClip)">')
    a(
        f'<rect x="{right_x}" y="{right_y}" width="{right_w}" height="42" fill="{t["titlebar"]}" fill-opacity="0.92"/>'
    )
    a(
        f'<rect x="{right_x}" y="{right_y}" width="{right_w}" height="42" fill="url(#glassSweep)" opacity="0.35"/>'
    )
    # traffic lights
    for i, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        a(
            f'<circle cx="{right_x + 22 + i * 16}" cy="{right_y + 21}" r="5.2" fill="{col}" opacity="0.95"/>'
        )
    a(
        f'<text x="{right_x + right_w / 2}" y="{right_y + 26}" text-anchor="middle" fill="{t["muted"]}" font-size="12" '
        f"""font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">"""
        f"evgeny@softeis — zsh</text>"
    )
    a(
        f'<line x1="{right_x}" y1="{right_y + 42}" x2="{right_x + right_w}" y2="{right_y + 42}" '
        f'stroke="{t["border"]}" stroke-opacity="{t["border_op"]}"/>'
    )

    # glass sweep over body
    a(
        f'<rect x="{right_x}" y="{right_y + 42}" width="{right_w}" height="{right_h - 42}" fill="url(#glass)" opacity="0.8"/>'
    )
    a(
        f'<rect x="{right_x + 80}" y="{right_y}" width="140" height="{right_h}" fill="url(#glassSweep)" opacity="0.25" transform="skewX(-18)"/>'
    )
    a("</g>")

    # terminal content
    tx = right_x + 32
    sans = "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    mono = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace"

    # prompt
    a(
        f'<text x="{tx}" y="{y_prompt}" fill="{t["muted"]}" font-size="12" font-family="{mono}">'
        f'<tspan fill="{t["a3"]}">❯</tspan>'
        f'<tspan dx="8">./introduce.sh</tspan>'
        f"</text>"
    )

    # Hi 👋
    a(
        f'<g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.35s" fill="freeze"/>'
        f'<text x="{tx}" y="{y_hi}" fill="{t["muted"]}" font-size="15" font-family="{sans}">Hi 👋</text>'
        f"</g>"
    )

    # I'm {NAME}
    a(
        f'<g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="0.7s" fill="freeze"/>'
        f'<text x="{tx}" y="{y_name}" font-size="32" font-weight="600" font-family="{sans}" fill="url(#accent)" letter-spacing="-0.4">'
        f"I'm Evgeny Eysner</text>"
        f"</g>"
    )

    # typing roles
    a(f'<g clip-path="url(#roleClip)">')
    for i, phrase in enumerate(PHRASES):
        kt, kv = phrase_opacity[i]
        a(
            f'<text x="{tx}" y="{role_y}" font-size="{role_fs}" font-weight="500" font-family="{mono}" fill="url(#accent)">'
            f"{xml(phrase)}"
            f'<animate attributeName="opacity" values="{kv}" keyTimes="{kt}" dur="{total_dur}s" repeatCount="indefinite"/>'
            f"</text>"
        )
    a("</g>")
    # cursor at clip edge
    a(
        f'<rect width="8" height="20" y="{role_y - 16}" fill="{t["cursor"]}" filter="url(#glow)">'
        f'<animate attributeName="x" values="{";".join(str(round(role_x + float(v), 2)) for v in kv_x.split(";"))}" '
        f'keyTimes="{kt_x}" dur="{total_dur}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.45;0.5;1" dur="1.05s" repeatCount="indefinite"/>'
        f"</rect>"
    )

    # divider
    a(
        f'<line x1="{tx}" y1="{y_div1}" x2="{right_x + right_w - 32}" y2="{y_div1}" '
        f'stroke="{t["border"]}" stroke-opacity="{t["border_op"]}">'
        f'<animate attributeName="stroke-opacity" values="0;0;{t["border_op"]}" keyTimes="0;0.55;1" dur="2.2s" fill="freeze"/>'
        f"</line>"
    )

    # info rows
    for i, (label, value, kind) in enumerate(INFO):
        gy = y_info + i * info_gap
        delay = round(1.55 + i * 0.18, 2)
        a(f'<g opacity="0">')
        a(
            f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay}s" fill="freeze"/>'
        )
        a(
            f'<animateTransform attributeName="transform" type="translate" from="0 8" to="0 0" dur="0.45s" begin="{delay}s" fill="freeze"/>'
        )
        a(
            f'<g transform="translate({tx},{gy - 10})" fill="none" stroke="{t["a2"]}" stroke-width="1.35" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="0.9">'
            f'<path d="{icon_path(kind)}"/></g>'
        )
        a(
            f'<text x="{tx + 22}" y="{gy}" font-size="10.5" font-family="{mono}" fill="{t["muted"]}" letter-spacing="1.6">{label}</text>'
        )
        a(
            f'<text x="{tx + 148}" y="{gy}" font-size="13.5" font-family="{sans}" fill="{t["text"]}">{xml(value)}</text>'
        )
        a("</g>")

    # skills label
    a(
        f'<g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.4s" fill="freeze"/>'
        f'<text x="{tx}" y="{y_skills_lbl}" font-size="10.5" font-family="{mono}" fill="{t["muted"]}" letter-spacing="1.8">SKILLS</text>'
        f"</g>"
    )

    # pills
    for label, px, py, pw, ph, idx in pills:
        delay = round(2.55 + idx * 0.08, 2)
        pulse_dur = 3.2 + (idx % 4) * 0.35
        a(f'<g class="pill" opacity="0">')
        a(
            f'<animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{delay}s" fill="freeze"/>'
        )
        a(f'<g transform="translate({px + pw / 2:.1f},{py + ph / 2:.1f})">')
        a(
            f'<animateTransform attributeName="transform" type="scale" values="1;1.035;1" '
            f'dur="{pulse_dur:.2f}s" begin="{delay}s" repeatCount="indefinite" additive="sum"/>'
        )
        a(f'<g transform="translate({-pw / 2:.1f},{-ph / 2:.1f})">')
        a(
            f'<rect class="pill-bg" x="0" y="0" width="{pw}" height="{ph}" rx="14" '
            f'fill="{t["a1"]}" fill-opacity="{t["pill_fill_op"]}" '
            f'stroke="{t["a2"]}" stroke-opacity="{t["pill_stroke_op"]}" stroke-width="1"/>'
        )
        # inner glow pulse
        a(
            f'<rect x="0.5" y="0.5" width="{pw - 1}" height="{ph - 1}" rx="13.5" fill="none" '
            f'stroke="{t["a2"]}" stroke-width="1" opacity="0.0">'
            f'<animate attributeName="opacity" values="0;0.45;0" dur="{pulse_dur:.2f}s" begin="{delay}s" repeatCount="indefinite"/>'
            f"</rect>"
        )
        a(
            f'<text x="{pw / 2:.1f}" y="{ph / 2 + 4:.1f}" text-anchor="middle" font-size="{pill_fs}" '
            f'font-weight="500" font-family="{sans}" fill="{t["text"]}">{xml(label)}</text>'
        )
        a("</g></g></g>")

    # socials
    sx0 = tx
    sy0 = y_social
    a(
        f'<g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="3.5s" fill="freeze"/>'
    )
    for i, (key, label) in enumerate(socials):
        sx = sx0 + i * 52
        a(f'<g class="social" transform="translate({sx},{sy0})" filter="url(#glowSoft)">')
        a(
            f'<circle cx="14" cy="14" r="16" fill="{t["a2"]}" fill-opacity="0.06" stroke="{t["border"]}" stroke-opacity="{t["border_op"] + 0.04}"/>'
        )
        a(
            f'<circle cx="14" cy="14" r="16" fill="none" stroke="{t["a2"]}" stroke-opacity="0">'
            f'<animate attributeName="stroke-opacity" values="0.08;0.35;0.08" dur="{3.4 + i * 0.4:.1f}s" repeatCount="indefinite"/>'
            f"</circle>"
        )
        a(
            f'<use href="#ic-{key}" xlink:href="#ic-{key}" x="4" y="4" width="20" height="20" opacity="{t["icon_op"]}"/>'
        )
        a(f'<title>{label}</title>')
        a("</g>")
    a("</g>")

    # right border + shimmer
    a(
        f'<rect x="{right_x + 0.6}" y="{right_y + 0.6}" width="{right_w - 1.2}" height="{right_h - 1.2}" rx="{pr - 0.4}" '
        f'fill="none" stroke="{t["border"]}" stroke-opacity="{t["border_op"]}" stroke-width="1"/>'
    )
    a(
        f'<rect x="{right_x + 0.6}" y="{right_y + 0.6}" width="{right_w - 1.2}" height="{right_h - 1.2}" rx="{pr - 0.4}" '
        f'fill="none" stroke="url(#shimmer)" stroke-width="1.15" stroke-opacity="0.65"/>'
    )

    # outer canvas border shimmer
    a(
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="27" fill="none" '
        f'stroke="{t["border"]}" stroke-opacity="{t["border_op"]}" stroke-width="1.2"/>'
    )
    a(
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="27" fill="none" '
        f'stroke="url(#shimmer)" stroke-width="1.3" stroke-opacity="0.55"/>'
    )

    a("</g>")  # canvas clip
    a("</svg>")
    return "\n".join(parts)


def main() -> None:
    ascii_lines = make_ascii()
    for name, theme, mode in (("dark", DARK, "dark"), ("light", LIGHT, "light")):
        svg = build(theme, ascii_lines, mode)
        path = OUT / f"{name}.svg"
        path.write_text(svg, encoding="utf-8")
        print(f"wrote {path} ({path.stat().st_size / 1024:.1f} KB) ascii={len(ascii_lines)}x{len(ascii_lines[0])}")
        print("ASCII preview:")
        if name == "dark":
            for line in ascii_lines:
                print(line)


if __name__ == "__main__":
    main()

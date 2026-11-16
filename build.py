"""Build the guild board with Python's standard library."""
import argparse
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEXT_FIELDS = "title place patron reward notice objective lead truth motive outcome".split()


def load_quests():
    quests = []
    numbers = set()
    for path in sorted((ROOT / "quests").glob("*.json")):
        q = json.loads(path.read_text(encoding="utf-8"))
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", path.stem):
            raise ValueError(f"Invalid filename: {path.name}")
        number = q["number"]
        if type(number) is not int or number < 1 or number in numbers:
            raise ValueError(f"Invalid or duplicate number: {path.name}")
        numbers.add(number)
        difficulty = q["difficulty"]
        if type(difficulty) is not int or not 1 <= difficulty <= 5:
            raise ValueError(f"Difficulty must be 1–5: {path.name}")
        q.setdefault("special", False)
        if type(q["special"]) is not bool:
            raise ValueError(f"special must be boolean: {path.name}")
        for field in TEXT_FIELDS:
            if not isinstance(q[field], str) or not q[field].strip():
                raise ValueError(f"Missing {field}: {path.name}")
            q[field] = escape(q[field])
        q["pacing"] = escape(q.get("pacing", "玩家停滯時，讓委託人指出下一個可以拜訪的人。"))
        routes = q["routes"]
        if not isinstance(routes, list) or len(routes) < 2 or any(
            not isinstance(pair, list) or len(pair) != 2 or
            not all(isinstance(s, str) and s.strip() for s in pair) for pair in routes
        ):
            raise ValueError(f"Invalid routes: {path.name}")
        q["routes"] = [(escape(a), escape(b)) for a, b in routes]
        q["slug"] = path.stem
        quests.append(q)
    if not quests:
        raise ValueError("At least one quest is required")
    return sorted(quests, key=lambda q: q["number"])


def page(title, content, prefix=""):
    return f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}｜星燈港冒險者公會</title><link rel="stylesheet" href="{prefix}style.css?v=wenkai-1"></head>
<body class="{'quest-page' if prefix else 'board-page'}"><header><a class="brand" href="{prefix}index.html"><span class="sign" aria-hidden="true">✦</span> 星燈港冒險者公會</a><span lang="en">STARLAMP HARBOR GUILD</span></header>
<main>{content}</main><footer>星燈港公會檔案室 <span>D&amp;D 原創短篇冒險</span></footer>{'<script src="../return-board.js" defer></script>' if prefix else ''}</body></html>
"""


def clock_face():
    """Restore the painted texture under the two static hands before animating them."""
    return '''<svg class="guild-clock" hidden viewBox="0 0 1536 1024" preserveAspectRatio="xMidYMid slice"
role="img" aria-label="台灣時間">
<defs>
<radialGradient id="brass"><stop stop-color="#ffe3a0"/><stop offset=".82" stop-color="#dda54c"/><stop offset="1" stop-color="#98632c"/></radialGradient>
<clipPath id="painted-hands">
<path d="M772 180 L766 187 L743 168 L736 165 L731 155 L723 148 L733 151 L741 153 L745 157 L768 173 Z"/>
<path d="M772 180 L773 172 L807 148 L807 146 L816 145 L843 131 L821 150 L817 155 L812 156 L779 185 Z"/>
<circle cx="772" cy="180" r="10.5"/></clipPath>
</defs>
<g clip-path="url(#painted-hands)">
<image href="assets/guild-clock-board.webp" width="1536" height="1024"
transform="translate(0 360) scale(1 -1)"/></g>
<g transform="translate(772 180)">
<path id="hour-hand" d="M0 8 L-3 -7 L-2 -31 L-4 -33 L0 -47 L4 -33 L2 -31 L3 -7 Z" fill="#edbb64" stroke="#65421e"/>
<path id="minute-hand" d="M0 11 L-2 -6 L-1.6 -51 L-3 -53 L0 -66 L3 -53 L1.6 -51 L2 -6 Z" fill="#ffda88" stroke="#64411f"/>
<circle r="6" fill="url(#brass)" stroke="#6d4727"/></g></svg>'''


def card(q):
    stars = "★" * q["difficulty"]
    return f"""<div class="pin-slot"><a class="pin-note" data-difficulty="{q['difficulty']}" href="quests/{q['slug']}.html"
aria-label="{q['title']}，{q['place']}，難度 {q['difficulty']} 星">
<span class="pin-label">{q['place']}<span class="pin-stars">{stars}</span></span>
<div class="pin-copy"><h3>{q['title']}</h3><p>{q['notice']}</p></div></a></div>"""


def detail(q):
    routes = "".join(f"<dt>{action}</dt><dd>{clue}</dd>" for action, clue in q["routes"])
    return page(q["title"], f"""<a class="back" href="../index.html">← 返回委託布告欄</a>
<article class="sheet"><div class="meta"><span>{q['place']}</span></div>
<h1>{q['title']}</h1><blockquote>{q['notice']}</blockquote>
<dl class="facts"><dt>委託人</dt><dd>{q['patron']}</dd><dt>任務報酬</dt><dd>{q['reward']}</dd></dl>
<h2>任務目標</h2><p>{q['objective']}</p><h2>調查起點</h2><p>{q['lead']}</p>
<details><summary>主持人筆記 <small>含劇透</small></summary><h3>事件真相</h3><p>{q['truth']}</p>
<h3>人物動機</h3><p>{q['motive']}</p><h3>調查路線</h3><dl>{routes}</dl>
<h3>帶團節奏</h3><p>{q["pacing"]}</p><h3>可能的收場</h3><p>{q['outcome']}</p></details><span class="scroll-end" aria-hidden="true"></span></article>""", "../")


def priority(q):
    return q.get("special", False) or q["difficulty"] == 5


def arrange_quests(quests):
    """Replay arrivals so rebuilds reproduce promotions and displacements."""
    ordered = []
    for q in sorted(quests, key=lambda item: item["number"]):
        if not priority(q):
            ordered.append(q)
            continue
        start = 0
        while len(ordered[start:start + 5]) == 5 and all(
            item["difficulty"] == 5 for item in ordered[start:start + 5]
        ):
            start += 5
        first = ordered[start:start + 5]
        tail = ordered[start + 5:]
        displaced = []
        if len(first) == 5:
            victim = min(first, key=lambda item: (item["difficulty"], item["number"]))
            first.remove(victim)
            displaced.append(victim)
        insert_at = max((i + 1 for i, item in enumerate(first) if priority(item)), default=0)
        first.insert(insert_at, q)
        ordered = ordered[:start] + first + tail + displaced
    return ordered


def board_leaf(group):
    # Keep data order separate from physical pin positions.
    slots = list(range(1, 6))
    centered = next((q for q in group if priority(q)), None)
    if centered:
        slots.remove(3)
    rendered = []
    for q in group:
        slot = 3 if q is centered else slots.pop(0)
        rendered.append(card(q).replace('class="pin-slot"', f'class="pin-slot" data-slot="{slot}"', 1))
    return '<div class="board-leaf">' + "".join(rendered) + '</div>'


def noticeboard(quests):
    quests = arrange_quests(quests)
    groups = [quests[start:start + 5] for start in range(0, len(quests), 5)]
    leaves = "".join(
        board_leaf(group)
        for group in groups
    )
    return f'''<div class="flip-demo">
<div class="flip-stage">{clock_face()}<div class="board-recess" aria-hidden="true"></div>
<div class="flip-panel">
<div class="grid flip-face flip-front"></div>
<div class="grid flip-face flip-back" inert aria-hidden="true"></div>
<div class="board-edge" aria-hidden="true"></div>
</div></div>
<div class="flip-controls" {'hidden' if len(groups) <= 1 else ''}><button type="button" class="flip-button">翻到下一面 ↻</button></div>
<div class="board-storage" hidden>{leaves}</div>
</div><script src="board.js" defer></script><script src="flip.js" defer></script>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--preview", action="store_true", help="Also generate/check the local flip preview")
    args = parser.parse_args()
    quests = load_quests()
    board = noticeboard(quests)
    pages = {ROOT / "index.html": page("冒險委託布告欄", f"""<section class="hero">
<div class="kicker" lang="en">ADVENTURERS’ GUILD</div><h1>冒險委託布告欄</h1>
<p>櫃台的星燈亮了。今晚，你要接下哪一封委託？</p></section>
<section aria-labelledby="posted"><div class="sectionhead"><h2 id="posted">委託揭示板</h2><span>{len(quests)} 件委託</span></div>
{board}</section>""")}
    if args.preview:
        pages[ROOT / "flip-preview.html"] = page("公告板翻面預覽", f"""
<a class="back" href="index.html">← 返回公會首頁</a>{board}""")
    for q in quests:
        pages[ROOT / "quests" / (q["slug"] + ".html")] = detail(q)
    for path, content in pages.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"Rebuild required: {path.name}")
        else:
            path.write_text(content, encoding="utf-8")
    print(f"{len(pages)} pages {'verified' if args.check else 'built'}")


if __name__ == "__main__":
    main()

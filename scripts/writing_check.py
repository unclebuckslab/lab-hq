"""The automated half of the writing-rules check (handbook/WRITING_RULES.md).

    python scripts/writing_check.py <draft.md> [--json]

Marks the phrases the rules name, plus emoji. It catches the obvious hits cheaply; the Editor
subagent is the judge for everything a phrase list can't see (rhythm, a hedge in new words,
a one-line paragraph landing a point). Text inside quotation marks is skipped: quoting what a
company said isn't the lab using the phrase. Exits 1 when anything is marked.

Add a phrase here when the Editor keeps catching it, and add an editor eval case for it.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PHRASES = {
    1: ["in today's fast-moving world", "in today's fast-paced world", "let's dive in", "let's dive into",
        "in conclusion", "ultimately,", "at the end of the day", "without further ado"],
    2: ["truly", "incredibly", "genuinely", "it's important to note", "it is important to note",
        "arguably", "a wide range of", "it's worth noting", "needless to say"],
    3: ["game-changer", "game changer", "unlock the potential", "navigate the landscape", "plays a crucial role",
        "robust", "seamless", "delve", "tapestry"],
    4: ["here's the thing", "it's not just", "it isn't just"],
}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
QUOTED = re.compile(r'"[^"\n]*"|“[^”\n]*”')
CODE = re.compile(r"`[^`\n]*`")


def check(text: str) -> list[dict]:
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        visible = CODE.sub(lambda m: " " * len(m.group()), QUOTED.sub(lambda m: " " * len(m.group()), line))
        low = visible.lower().replace("’", "'")
        for rule, phrases in PHRASES.items():
            for p in phrases:
                for m in re.finditer(r"(?<![a-z])" + re.escape(p) + (r"(?![a-z])" if p[-1].isalpha() else ""), low):
                    hits.append({"line": n, "rule": rule, "text": line[m.start():m.end()]})
        for m in EMOJI.finditer(visible):
            hits.append({"line": n, "rule": 5, "text": m.group()})
    return hits


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print(__doc__)
        return 2
    hits = check(Path(args[0]).read_text(encoding="utf-8"))
    if "--json" in args:
        print(json.dumps(hits, indent=1))
    else:
        for h in hits:
            print(f"line {h['line']}: rule {h['rule']}: {h['text']}")
        print(f"{len(hits)} marked" if hits else "Nothing marked")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())

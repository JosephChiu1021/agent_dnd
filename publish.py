"""Build a clean GitHub Pages artifact without preview pages."""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "_site"


def main():
    subprocess.run([sys.executable, str(ROOT / "build.py"), "--check"], check=True)
    if SITE.is_symlink() or SITE.resolve() != ROOT.resolve() / "_site":
        raise SystemExit("Refusing an unexpected output path")
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    for name in ("index.html", "style.css", "board.js", "flip.js", "return-board.js"):
        shutil.copy2(ROOT / name, SITE / name)
    shutil.copytree(ROOT / "assets", SITE / "assets")
    (SITE / "quests").mkdir()
    for source in sorted((ROOT / "quests").glob("*.json")):
        shutil.copy2(source.with_suffix(".html"), SITE / "quests" / source.with_suffix(".html").name)
    (SITE / ".nojekyll").touch()
    print("Formal website ready in _site (preview pages excluded)")


if __name__ == "__main__":
    main()

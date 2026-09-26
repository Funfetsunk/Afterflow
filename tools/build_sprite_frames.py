"""Build a character's SpriteFrames resource from its exported animation frames.

tools/export_assets.py writes frames as assets/characters/<name>/<name>_<anim>_<d>_<i>.png
(d = s, e, n, w). This writes resources/sprites/<name>_frames.tres with one
animation per animation and direction, named <anim>_<d> (idle_s,
walk_e, ...), which is what the player script plays. Frame rates are set here
and can be tweaked in the editor afterwards (re-running overwrites them).

Usage (from the project root, after tools/export_assets.py):
    python tools/build_sprite_frames.py awa idle:4:4 walk:6:10 swing:4:16:once
    python tools/build_sprite_frames.py NAME ANIM:FRAMES:FPS[:once] ...

`:once` makes an animation play once instead of looping (attacks).
"""

import argparse
import re
from pathlib import Path

DIRS = "senw"


def main():
    parser = argparse.ArgumentParser(description="Exported frames -> SpriteFrames .tres")
    parser.add_argument("name")
    parser.add_argument("anims", nargs="+", help="ANIM:FRAMES:FPS[:once]")
    args = parser.parse_args()

    ext, anims = [], []
    for spec in args.anims:
        anim, frames, fps, *once = spec.split(":")
        loop = "false" if once == ["once"] else "true"
        for d in DIRS:
            refs = []
            for i in range(int(frames)):
                path = f"res://assets/characters/{args.name}/{args.name}_{anim}_{d}_{i}.png"
                if not Path(path.removeprefix("res://")).exists():
                    raise SystemExit(f"Missing frame {path}; run tools/export_assets.py first")
                ext.append(f'[ext_resource type="Texture2D" path="{path}" id="{len(ext) + 1}"]')
                refs.append(f'{{"duration": 1.0, "texture": ExtResource("{len(ext)}")}}')
            anims.append("{\n" + f'"frames": [{", ".join(refs)}],\n"loop": {loop},\n'
                         f'"name": &"{anim}_{d}",\n"speed": {float(fps)}\n' + "}")

    out = Path(f"resources/sprites/{args.name}_frames.tres")
    out.parent.mkdir(parents=True, exist_ok=True)
    # keep the resource's uid across rebuilds, so scenes' references stay valid
    old = re.search(r'uid="([^"]+)"', out.read_text().splitlines()[0]) if out.exists() else None
    uid = f' uid="{old.group(1)}"' if old else ""
    out.write_text(f'[gd_resource type="SpriteFrames" format=3{uid}]\n\n' + "\n".join(ext)
                   + "\n\n[resource]\nanimations = [" + ", ".join(anims) + "]\n")
    print(f"{out}: {len(anims)} animations, {len(ext)} frames")


if __name__ == "__main__":
    main()

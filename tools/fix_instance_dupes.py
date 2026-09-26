"""Repair scenes whose instanced sub-scenes had their children saved as local copies.

Godot MCP's scene-instancing command can leave an instance's children owned by
the outer scene, so saving writes a full copy of each child ("[node ... type=...
parent="Player"]"). On load Godot builds the instance's real children and then
the copies: "An incoming node's name clashes with ..." and, after another save,
duplicates renamed Sprite2, Feet2, ...

This folds every such copy back into a plain property override of the real
child (so deliberate changes such as a pickup's texture are kept, later copies
winning), drops `type=` from instance roots, and leaves genuinely added nodes
(e.g. a Camera added under the Player instance) alone.

Usage (from the project root; close or reload the scenes in the editor after):
    python tools/fix_instance_dupes.py scenes/world/*.tscn
"""

import re
import sys
from pathlib import Path

HEADER = re.compile(r"^\[(\w+)(.*)\]\s*$")
ATTR = re.compile(r'(\w+)=("(?:[^"\\]|\\.)*"|\w+\([^)]*\)|\[[^\]]*\]|[^\s\]]+)')


def blocks(text):
    """Split a .tscn into [header_line, body_lines] blocks (first block: file header)."""
    out, cur = [], None
    for line in text.split("\n"):
        if HEADER.match(line):
            cur = [line, []]
            out.append(cur)
        elif cur is not None:
            cur[1].append(line)
    return out


def attrs(header):
    kind, rest = HEADER.match(header).groups()
    return kind, dict(ATTR.findall(rest))


def unq(v):
    return v[1:-1] if v and v.startswith('"') else v


def node_paths(scene_file):
    """Relative paths ('Sprite', 'Hitbox/Shape') of every non-root node in a scene."""
    paths = set()
    for header, _ in blocks(Path(scene_file).read_text(encoding="utf-8")):
        kind, a = attrs(header)
        if kind != "node" or "parent" not in a:
            continue
        parent = unq(a["parent"])
        name = unq(a["name"])
        paths.add(name if parent == "." else f"{parent}/{name}")
    return paths


def canonical(rel, known):
    """Map 'Hitbox2/Shape2' -> 'Hitbox/Shape' when the stripped path is a real child."""
    parts, fixed = rel.split("/"), []
    for p in parts:
        cand = "/".join(fixed + [p])
        if cand in known:
            fixed.append(p)
            continue
        stripped = re.sub(r"\d+$", "", p)
        if "/".join(fixed + [stripped]) in known:
            fixed.append(stripped)
        else:
            return None
    return "/".join(fixed)


def fix(path):
    text = Path(path).read_text(encoding="utf-8")
    bl = blocks(text)
    ext = {}
    instances = {}                      # node path in this scene -> set of child rel paths
    for header, _ in bl:
        kind, a = attrs(header)
        if kind == "ext_resource":
            ext[unq(a.get("id"))] = unq(a.get("path"))
    for header, _ in bl:
        kind, a = attrs(header)
        if kind == "node" and "instance" in a:
            rid = re.search(r'ExtResource\("([^"]+)"\)', a["instance"]).group(1)
            parent = unq(a.get("parent", "."))
            npath = unq(a["name"]) if parent == "." else f"{parent}/{unq(a['name'])}"
            instances[npath] = node_paths(ext[rid].replace("res://", ""))

    out, overrides, order, changed = [], {}, [], 0
    for header, body in bl:
        kind, a = attrs(header)
        if kind == "node" and "instance" in a and "type" in a:
            header = re.sub(r' type="[^"]+"', "", header)          # an instance root has no type of its own
            changed += 1
        if kind == "node" and "type" in a and "parent" in a:
            parent = unq(a["parent"])
            owner = next((ip for ip in sorted(instances, key=len, reverse=True)
                          if parent == ip or parent.startswith(ip + "/")), None)
            if owner is not None:
                rel_parent = parent[len(owner) + 1:]
                rel = f"{rel_parent}/{unq(a['name'])}" if rel_parent else unq(a["name"])
                real = canonical(rel, instances[owner])
                if real is not None:                            # a copy of the instance's own child
                    key = f"{owner}/{real}"
                    props = overrides.setdefault(key, {})
                    if key not in order:
                        order.append(key)
                    for line in body:
                        if " = " in line and not line.startswith((" ", "\t")):
                            k, v = line.split(" = ", 1)
                            props[k] = v
                        elif line.strip() and props:
                            last = list(props)[-1]          # continuation of a multi-line value
                            props[last] += "\n" + line
                    changed += 1
                    continue
        out.append((header, body))

    lines = []
    for header, body in out:
        lines.append(header)
        lines.extend(body)
    text_out = "\n".join(lines).rstrip("\n") + "\n"
    for key in order:
        parent, name = key.rsplit("/", 1)
        text_out += f'\n[node name="{name}" parent="{parent}"]\n'
        for k, v in overrides[key].items():
            text_out += f"{k} = {v}\n"
    Path(path).write_text(text_out, encoding="utf-8")
    print(f"{path}: {changed} blocks folded into {len(order)} overrides")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        fix(p)

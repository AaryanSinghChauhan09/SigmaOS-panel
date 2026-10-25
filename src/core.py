"""Panel applet host for SigmaOS-panel (inspired by xfce-panel).

Principles: registry of known applets (information hiding), pure layout model,
fail-fast on unknown/duplicate applets, deterministic left/right-pack
rendering, plan vs apply separation (the panel itself is the execute layer).
"""
import argparse, json, os, sys, tempfile

ENGINE = {
    "name": "sigma-panel",
    "summary": "Panel applet host with layout planner",
    "language": "python",
    "verbs": ["applets", "add", "remove", "layout-plan"],
    "principles": ["Information Hiding", "Encapsulation", "Fail-Fast",
                   "KISS", "DRY", "Deterministic Testing"],
}

cli_doc = """\
$ sigma-panel applets
$ sigma-panel add clock --pack end
$ sigma-panel remove clock
$ sigma-panel layout-plan
[start] menu-button > window-list   ~~~panel stretch~~~   [end] sound < clock
"""

DEFAULT_STORE = os.path.expanduser("~/.config/sigma-panel/layout.json")

APPLETS = {
    "menu-button": {"name": "Menu Button", "pack": "start"},
    "show-desktop": {"name": "Show Desktop", "pack": "start"},
    "window-list": {"name": "Window List", "pack": "start"},
    "spacer": {"name": "Spacer", "pack": "start"},
    "systray": {"name": "System Tray", "pack": "end"},
    "sound": {"name": "Sound Indicator", "pack": "end"},
    "network": {"name": "Network Indicator", "pack": "end"},
    "power": {"name": "Power Indicator", "pack": "end"},
    "clock": {"name": "Clock", "pack": "end"},
}


class PanelError(ValueError):
    pass


def load_layout(path):
    """Load the layout store; validate every entry (fail-fast on corruption)."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    layout = []
    for entry in data:
        if entry.get("id") not in APPLETS or entry.get("pack") not in ("start", "end"):
            raise PanelError(f"bad layout entry: {entry!r}")
        layout.append({"id": entry["id"], "pack": entry["pack"]})
    return layout


def save_layout(path, layout):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".sigma-tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(layout, fh, indent=2)
    os.replace(tmp, path)


def add_applet(layout, applet_id, pack=None, position=None):
    """Return a NEW layout with applet_id added. Pure."""
    if applet_id not in APPLETS:
        raise PanelError(f"unknown applet: {applet_id} "
                         f"(have: {', '.join(sorted(APPLETS))})")
    if any(a["id"] == applet_id for a in layout):
        raise PanelError(f"applet already in layout: {applet_id}")
    pack = pack or APPLETS[applet_id]["pack"]
    if pack not in ("start", "end"):
        raise PanelError(f"pack must be start|end, got {pack!r}")
    entry = {"id": applet_id, "pack": pack}
    out = list(layout)
    if position is None:
        out.append(entry)
    elif 0 <= position <= len(out):
        out.insert(position, entry)
    else:
        raise PanelError(f"position out of range: {position}")
    return out


def remove_applet(layout, applet_id):
    """Return a NEW layout without applet_id. Fail-fast if absent."""
    for i, a in enumerate(layout):
        if a["id"] == applet_id:
            return layout[:i] + layout[i + 1:]
    raise PanelError(f"applet not in layout: {applet_id}")


def render_layout(layout):
    """Pure, deterministic render of the panel geometry."""
    start = [a["id"] for a in layout if a["pack"] == "start"]
    end = [a["id"] for a in layout if a["pack"] == "end"]
    left = "[start] " + (" > ".join(start) if start else "(empty)")
    right = "[end] " + (" < ".join(end) if end else "(empty)")
    return f"{left}   ~~~panel stretch~~~   {right}"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog=ENGINE["name"], description=ENGINE["summary"])
    p.add_argument("--store", default=DEFAULT_STORE, help="layout store (JSON)")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("applets", help="list known applets and layout membership")
    a.add_argument("--available", action="store_true", help="list the registry only")
    ad = sub.add_parser("add", help="add an applet to the layout")
    ad.add_argument("applet_id")
    ad.add_argument("--pack", choices=("start", "end"), default=None)
    ad.add_argument("--position", type=int, default=None)
    rm = sub.add_parser("remove", help="remove an applet from the layout")
    rm.add_argument("applet_id")
    sub.add_parser("layout-plan", help="render the current layout")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        layout = load_layout(args.store)
        if args.cmd == "applets":
            if args.available:
                for aid in sorted(APPLETS):
                    print(f"{aid}\t{APPLETS[aid]['name']}\tpack={APPLETS[aid]['pack']}")
            else:
                placed = {a["id"] for a in layout}
                for aid in sorted(APPLETS):
                    mark = "*" if aid in placed else "-"
                    print(f"{mark} {aid}\t{APPLETS[aid]['name']}")
        elif args.cmd == "add":
            layout = add_applet(layout, args.applet_id, pack=args.pack,
                                position=args.position)
            save_layout(args.store, layout)
            print(f"added {args.applet_id} ({len(layout)} applet(s))")
        elif args.cmd == "remove":
            layout = remove_applet(layout, args.applet_id)
            save_layout(args.store, layout)
            print(f"removed {args.applet_id} ({len(layout)} applet(s))")
        elif args.cmd == "layout-plan":
            print(render_layout(layout))
        return 0
    except (PanelError, OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


def self_test() -> None:
    layout = []
    layout = add_applet(layout, "menu-button")
    layout = add_applet(layout, "window-list")
    layout = add_applet(layout, "clock")
    assert [a["id"] for a in layout] == ["menu-button", "window-list", "clock"]
    assert [a["pack"] for a in layout] == ["start", "start", "end"]
    # explicit position + pack override
    layout = add_applet(layout, "systray", pack="end", position=0)
    assert layout[0] == {"id": "systray", "pack": "end"}
    # fail-fast paths
    for bad in (lambda: add_applet(layout, "no-such-applet"),
                lambda: add_applet(layout, "clock"),            # duplicate
                lambda: add_applet(layout, "spacer", position=99)):
        try:
            bad()
        except PanelError:
            pass
        else:
            raise AssertionError("expected PanelError")
    layout = remove_applet(layout, "window-list")
    assert "window-list" not in [a["id"] for a in layout]
    try:
        remove_applet(layout, "window-list")
    except PanelError:
        pass
    else:
        raise AssertionError("removing a missing applet should fail")
    text = render_layout(layout)
    assert text.index("menu-button") < text.index("~~~panel stretch~~~") < text.index("clock")
    assert render_layout([]) == "[start] (empty)   ~~~panel stretch~~~   [end] (empty)"
    # persistence round-trip (tempdir only)
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "layout.json")
        save_layout(path, layout)
        assert load_layout(path) == layout
        assert load_layout(os.path.join(d, "none.json")) == []
        with open(path, "w", encoding="utf-8") as fh:
            fh.write('[{"id": "bogus", "pack": "start"}]')
        try:
            load_layout(path)
        except PanelError:
            pass
        else:
            raise AssertionError("corrupt store not caught")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

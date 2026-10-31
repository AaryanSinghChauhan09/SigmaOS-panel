# SigmaOS Panel

Python command-line tool for maintaining a panel layout. It lists a fixed
registry of applet identifiers, adds or removes identifiers from a JSON layout,
and renders a deterministic text plan with `start` and `end` packing.

## Commands and data

- `sigma-panel applets` lists registered applets and layout membership.
- `sigma-panel add ID --pack start|end` and `remove ID` update the layout.
- `sigma-panel layout-plan` prints the current text layout.
- The default store is `~/.config/sigma-panel/layout.json`; `--store PATH`
  selects another file.

The write commands modify only this layout file. They do not install applets,
launch indicators, create a taskbar window, or connect to a desktop session.
Unknown and duplicate applets and malformed stored entries fail with an error.

## Development

`make build` compiles the Python sources. `make test` runs the unittest suite.
The temporary self-test uses a temporary directory for persistence checks.
This component is inspired by the modular applet model of
[Xfce Panel](https://github.com/linuxmint/xfce-panel); it does not implement
Xfce plugins or a graphical panel backend.

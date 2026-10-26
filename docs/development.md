# Development

## Setup

You need Python 3.11+ and the headless `bpy` package (used for all testing
in this project, Blender 5.2.3):

```
pip install --break-system-packages bpy
```

Alternatively, run the test scripts from inside Blender's own bundled
Python (`blender --background --python tests/test_addon.py`-style
invocation), though the test scripts are written to be run directly with
`python3 -I` against the `bpy` package as shown below.

## Running tests

```
python3 -I tests/test_char_map.py
python3 -I tests/test_addon.py
```

`-I` (isolated mode) is used so an uploaded or downloaded file sharing a
name with a standard-library module can never shadow it.

## Building packages

```
python3 scripts/build.py
```

Produces `dist/blocky_text_generator-legacy-v<version>.zip` and
`dist/blocky_text_generator-extension-v<version>.zip`. Bump `VERSION` in
`scripts/build.py`, `addon/blender_manifest.toml`'s `version` field, and
`scripts/templates/legacy_init.py`'s `bl_info["version"]` together when
releasing.

## Project conventions

- No comments in any `addon/` source file (see CONTRIBUTING.md) — explain
  things here instead.
- `modules/` contains no `bpy.types.Operator` / `Panel` / `PropertyGroup`
  subclasses; those live only in `ui/`, so generation logic can be
  exercised without going through the operator dialog if needed.
- Keep `char_map.py` a pure data module matching
  `original_source/mc_text_generator.js` exactly;
  `tests/test_char_map.py` enforces this automatically by parsing the
  original `.js` file and diffing it against the Python data.

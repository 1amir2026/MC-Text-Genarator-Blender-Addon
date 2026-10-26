# Contributing

Contributions are welcome. A few guidelines specific to this project:

## No comments in source code

Generated and contributed Python source files in `addon/` must not contain
explanatory comments (inline, standalone, TODO, or commented-out code). Use
clear function, class, and variable names instead. Put explanations in
`docs/`.

## Keep the character map in sync

`addon/modules/char_map.py` is a direct, verified transcription of the
`charMap` object in `original_source/mc_text_generator.js`. If you change a
letter's geometry, update both the data and `tests/test_char_map.py`'s
expectations stay correct by re-running:

```
python3 tests/test_char_map.py
```

## Running the test suite

From the project root, with a Python environment that has `bpy` installed
(`pip install bpy`) or inside Blender's own Python:

```
python3 tests/test_char_map.py
python3 tests/test_addon.py
```

Both must pass before a change is merged.

## Building the installable packages

```
python3 scripts/build.py
```

This produces both the legacy (3.6-4.1) and extension (4.2+) zip packages
in `dist/`.

## Reporting issues

Please include your Blender version, the installation method used (legacy
add-on vs. extension), and the exact text/settings that triggered the
problem.

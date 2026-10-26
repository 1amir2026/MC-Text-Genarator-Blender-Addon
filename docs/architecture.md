# Architecture

```
addon/
├── __init__.py              # Thin entry point; delegates to ui.register/unregister.
│                             # (A separate legacy __init__.py with bl_info is generated
│                             #  at build time from scripts/templates/legacy_init.py.)
├── blender_manifest.toml    # Extension metadata, used only by the 4.2+ package.
├── modules/
│   ├── char_map.py          # CHAR_DATA: a direct transcription of the original
│   │                         # plugin's `charMap` object (width + cube rectangles
│   │                         # per character). Pure data, no Blender API calls.
│   ├── generator.py         # The actual mesh-generation algorithm: walks the
│   │                         # input text, builds bmesh boxes per character
│   │                         # rectangle, applies offset/spacing/rotation/newlines,
│   │                         # groups everything into collections, centers the
│   │                         # result. Mirrors the original's double for-loop.
│   └── compat.py            # Small version-capability checks (e.g. whether
│                             # Collection.color_tag exists on this Blender build).
└── ui/
    ├── properties.py        # TEXTGEN_PG_settings PropertyGroup + scene registration.
    ├── operators.py         # TEXTGEN_OT_generate_text (the dialog + EXEC operator)
    │                         # and TEXTGEN_OT_about (popup replicating the original
    │                         # About dialog's content and links).
    └── panels.py             # 3D Viewport sidebar panel, Add Mesh menu entry,
                              # and Help menu entry.
```

## Why this split

- **`modules/` vs `ui/`**: generation logic has no dependency on operator or
  panel classes, so it can be unit-tested directly (see
  `tests/test_addon.py`, which calls the registered operator, and
  `tests/test_char_map.py`, which imports `char_map` directly with no
  `bpy` dependency beyond what `char_map.py` itself needs — none).
- **`char_map.py` isolated from `generator.py`**: the character data is the
  part of the original plugin most likely to need auditing against the
  source (see `docs/porting-notes.md`); keeping it in its own small,
  comment-free, data-only file makes that diffing trivial.
- **`compat.py`**: Blender's RNA occasionally adds/removes properties
  between versions (e.g. `Collection.color_tag`). Centralizing those checks
  avoids scattering `hasattr`/version checks through the generation code.

## Data flow for one "Generate" click

1. `ui.operators.TEXTGEN_OT_generate_text.invoke` copies the current scene
   settings into the operator's own properties and opens
   `invoke_props_dialog`.
2. On confirm, `execute()` writes the operator's properties back to the
   scene property group (so the sidebar stays in sync), validates the text
   isn't empty, and builds a `modules.generator.GenerationSettings`.
3. `modules.generator.generate_text()` does the actual work: for each
   character it looks up `CHAR_DATA`, builds one bmesh box object per
   rectangle (handling the optional drop-shadow layer), accumulates the
   running `offset_x` / `text_length` / `num_lines`, and links everything
   into a nested collection hierarchy under a new root collection.
4. After the loop, it computes the combined bounding box of every created
   object and recenters them all on the origin (`centerText()` equivalent).
5. Back in the operator, `exceeds_java_limit` / `exceeds_bedrock_limit`
   check the returned `text_length` / `num_lines` against the 48 / 30 unit
   thresholds and report warnings if exceeded, without undoing the
   generation.

## Registration and compatibility

`addon/__init__.py` (installed via the extension package) and the
generated legacy `__init__.py` (installed via the legacy package) both
simply call `ui.register()` / `ui.unregister()`, which in turn registers
`properties`, then `operators`, then `panels` — and unregisters in reverse
order — so there is exactly one registration code path to test and no
duplication between the two install methods. See `docs/compatibility.md`
for what differs between the two `__init__.py` variants.

# Testing Report

## Environment actually used

- Headless `bpy` 5.2.3 (Blender 5.2.3 LTS core), installed via
  `pip install bpy`, Python 3.13.17, Linux.
- No Blender 3.6, 4.0, 4.1, or 4.2-5.1 runtime was available in this
  sandboxed environment, and no GUI Blender session was available (headless
  only). Everything below marked "tested" was run against this one real
  Blender 5.2.3 engine; everything else is static analysis, clearly labeled
  as such.

## What was actually run (not just written)

### Static checks — all passed

- `python3 -m py_compile` on every file under `addon/`: no syntax errors.
- Full-tree grep for comment lines, inline comments, and `TODO`/`FIXME`
  markers in `addon/`: none found, confirming the no-comments rule.
- `blender_manifest.toml` parsed with Python's `tomllib` and checked for
  all of `schema_version`, `id`, `version`, `name`, `tagline`,
  `maintainer`, `type`, `blender_version_min`, `license`: all present.
- Built zip contents inspected with `unzip -l` for both the legacy and
  extension packages: correct folder structure, no nested/duplicate
  zips, `blender_manifest.toml` present only in the extension package,
  `original_source/mc_text_generator.js` absent from both (per the
  licensing decision in docs/porting-notes.md).

### Functional / runtime checks — all passed, real `bpy` execution

Run via `tests/test_addon.py` (18 assertions) and
`tests/test_char_map.py` (1 assertion covering all 52 character entries):

- Add-on `register()` / `unregister()` complete without error.
- Scene property group, both operators (`textgen_generate_text`,
  `textgen_about`), and the sidebar panel are present after registration
  and gone after unregistration.
- Empty-text input is rejected with the expected error message (matches
  the original's "Make sure you don't leave the text field blank").
- Text made entirely of unsupported characters generates nothing and
  leaves no orphaned collections (verified by diffing
  `bpy.data.collections.keys()` before/after).
- Generating `"Hi!"` produces the expected 6 mesh objects (3 rects for
  `h`, 1 for `i`, 2 for `!`, matching `char_map.py`/the original
  `charMap`), is centered exactly on the world origin on all 3 axes, and
  has the expected overall width (9.6 units = h-width 5 + i-width 2 +
  !-width 2 + 2× letter_space 0.3), depth (4 units, matching the `depth`
  setting), and height (8 units, the standard glyph height).
- A backslash in the input text produces a line break (new `yOffset`,
  `numLines` increment) rather than being treated as a literal glyph or
  an invalid character — verified by checking the resulting collection
  still has exactly 4 character sub-collections for `"ab\cd"`.
- "Generate Layer" with Depth = 0 creates the expected `layer_base` /
  `layer_character_*` collection structure; with Depth != 0 it is
  correctly suppressed, matching the original's
  `formData.generateLayer == true && formData.depth == 0` condition
  exactly.
- A long string (`"abcdefghijklmnop"`, depth 4) triggers both the Java
  and Bedrock size warnings without raising an error or blocking
  generation (operator still returns `{'FINISHED'}` and the geometry is
  present), matching "Your text has still been generated."
- Two full register → unregister → register → unregister cycles complete
  with no duplicate-class registration errors and no leftover scene
  property.
- The extension zip was installed into a real Blender extension
  repository via `bpy.ops.extensions.package_install_files(...,
  enable_on_install=True)`, confirmed present and enabled in
  `bpy.context.preferences.addons`, confirmed its operator runs and
  produces geometry, then cleanly removed via
  `bpy.ops.extensions.package_uninstall(...)`.
- The legacy zip was extracted and its `__init__.py` (with `bl_info`)
  loaded directly; `bl_info["name"/"version"/"blender"]` read back
  correctly, and its generate operator was exercised successfully.
- `tests/test_char_map.py` parses `original_source/mc_text_generator.js`
  directly with a regex and asserts, character by character, that every
  one of the 52 entries (letters, digits, punctuation, space) in
  `addon/modules/char_map.py` has the identical width and identical
  rectangle coordinates as the original — this is a hard regression test,
  not a one-time manual check, and it currently passes.

Every one of the above is runnable again with:

```
python3 -I tests/test_char_map.py
python3 -I tests/test_addon.py
```

## What was NOT tested (explicitly disclosed limitations)

- **No GUI testing.** All checks above ran in Blender's headless
  `bpy` module. The dialog layout (`invoke_props_dialog`), the sidebar
  panel's visual appearance, the About popup's rendering, and mouse/
  keyboard interaction were written to standard, well-established Blender
  UI APIs and are expected to work, but were not visually confirmed in a
  windowed Blender session, because no display/GUI was available in this
  environment.
- **No Blender 3.6-4.1 runtime testing.** The legacy package's `bl_info`
  structure and the add-on's API usage were checked against documented
  API stability for that range (see docs/compatibility.md), but no actual
  3.6-4.1 binary was run. This is "implemented, not fully tested" per the
  master prompt's required disclosure categories.
- **No Blender 4.2-5.1 runtime testing**, for the same reason — only
  5.2.3 was available. The extension manifest schema and API calls used
  are unchanged across that range per Blender's own extension
  documentation, but this is inference from documentation, not a
  from-the-source runtime check.
- **No `blender --command extension validate` CLI check**, since no
  standalone `blender` executable (only the `bpy` Python module) was
  available in this environment. The manifest was instead validated by
  direct TOML-schema inspection and by a successful real install through
  `bpy.ops.extensions.package_install_files`, which performs Blender's own
  internal manifest validation as part of installing — an install failure
  would have surfaced a manifest error, and none occurred.
- **Export/import round-trip into a game engine** (e.g. actually exporting
  the generated mesh to a Minecraft resource pack format) was out of scope
  of the original plugin itself (which only generates in-editor geometry)
  and was correspondingly not built or tested here.

## Fixes made during testing

One real defect was caught and fixed by this testing process: the initial
`modules/compat.py` used `hasattr(bpy.types.Collection, "color_tag")` to
detect whether collection color tags are supported, which returned `False`
even on Blender 5.2.3 (where the feature exists) because `hasattr` on an
RNA **type** object doesn't reflect its instance properties the way a
dataclass or namedtuple would. This silently disabled the color-tag
feature on every supported Blender version. It was caught by
`tests/test_addon.py` initially failing to show expected `color_tag`
values during manual inspection, root-caused, and fixed by checking
`"color_tag" in bpy.types.Collection.bl_rna.properties` instead, which was
then re-verified to return the correct per-character colors.

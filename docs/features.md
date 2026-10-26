# Feature-Parity Checklist

Status legend: **Done** = implemented and tested (see docs/testing.md).
**Adapted** = implemented with a disclosed, necessary behavioral change
(see docs/porting-notes.md for the reasoning). **N/A** = original behavior
is Blockbench-internal plumbing with no meaningful Blender equivalent to
port (documented, not silently dropped).

| # | Original feature (Blockbench) | Blender implementation | Status |
|---|---|---|---|
| 1 | Plugin registration / menu entry under Tools | `register()`/`unregister()`, Add Mesh menu entry, sidebar panel | Done |
| 2 | "Generate Text" dialog with Generate/Cancel buttons | `invoke_props_dialog` on `TEXTGEN_OT_generate_text` | Done |
| 3 | Text input field, uppercase-letter CSS display, lowercased on use | `input_text` StringProperty; text is lowercased in `generate_text()` exactly like `formData.input.toLowerCase()` | Done |
| 4 | Letter Spacing (number, min 0, default 0.3) | `letter_space` FloatProperty, min 0, default 0.3 | Done |
| 5 | Word Spacing (number, min 0, default 1) | `word_space` FloatProperty, min 0, default 1.0 | Done |
| 6 | Depth (number, min 0, default 4) | `depth` FloatProperty, min 0, default 4.0 | Done |
| 7 | Rotation (range slider, -45 to 45, step 22.5, default 0) | `rotation` FloatProperty, min -45, max 45, default 0, slider in UI | Done (step snapping omitted — Blender float sliders don't expose a discrete "step" the way Blockbench's `range` input does; any value in range is allowed, a strict superset) |
| 8 | Generate Layer checkbox, conditional on Depth == 0 | `generate_layer` BoolProperty, UI-hidden unless `depth == 0.0`, logic-gated the same way in `generator.py` | Done |
| 9 | Java Block/Item size-warning checkbox | `show_java_warning` BoolProperty | Done |
| 10 | Bedrock Block size-warning checkbox | `show_bedrock_warning` BoolProperty | Done |
| 11 | Blank-input validation + error messagebox | Empty-string check in `execute()`, `self.report({'ERROR'}, ...)` | Done |
| 12 | Full a-z / 0-9 / punctuation character map with per-letter cube geometry | `modules/char_map.py`, verified identical to the original via `tests/test_char_map.py` (52/52 entries match) | Done |
| 13 | Unknown-character handling (skip + "Invalid Character(s) Detected" + summary) | Skipped, counted, reported via `self.report({'WARNING'}, ...)` in the same combined-summary style as the original's post-loop message | Done |
| 14 | Backslash (`\`) as a line-break character | Same character, same effect (`yOffset`/`numLines` equivalent), tested | Done |
| 15 | Per-character cube generation at computed offsets | `_rect_to_world_corners` + `_build_box_object` per rectangle, per character | Done |
| 16 | Random marker color per letter (Blockbench Outliner color) | `Collection.color_tag` set per character collection (version-guarded) | Adapted |
| 17 | Letter/word spacing accumulation (`offset`, `textLength`) | Identical accumulation logic in `generate_text()`, unit-tested for exact width | Done |
| 18 | Drop-shadow layer geometry (`layerGroup`/`layerBaseGroup`, offset by 0.2 units) | Same 0.2-unit nudge, same grouping, same depth==0 gate | Done |
| 19 | Outliner grouping: root group → per-letter group (+ layer groups) | Nested `bpy.data.collections`: root → `character_<c>` (+ `layer_base` → `layer_character_<c>`) | Done |
| 20 | Selecting + opening the generated group in the Outliner | Generated objects are selected and made active after generation | Done |
| 21 | Centering generated text on all 3 axes (`centerText()`) | Bounding-box computation + recentering on X/Y/Z, unit-tested | Done |
| 22 | Undo support around the whole generation | `bl_options = {'REGISTER', 'UNDO'}` | Done |
| 23 | Format-aware Java size-limit warning (48 units, tied to `Format.id === "java_block"`) | Always-available, independently toggleable 48-unit check (Blender has no project-format concept to key off) | Adapted |
| 24 | Format-aware Bedrock size-limit warning (30 units) | Always-available, independently toggleable 30-unit check | Adapted |
| 25 | Size-warning messagebox explaining the limit and recommending Transform > Scale | Same wording/intent via `self.report({'WARNING'}, ...)`, mentions Object > Transform > Scale | Done |
| 26 | Quick-message toasts ("Generated text: 'X'") | `self.report({'INFO'}/{'WARNING'}, ...)`, Blender's native equivalent | Done |
| 27 | Plugin uninstall quick-message | Not reproduced — Blender's add-on disable flow has no user-facing toast hook comparable to Blockbench's `onunload`; `unregister()` still performs full, silent, correct cleanup | N/A |
| 28 | About dialog (plugin description, usage notes, newline tip, author links) | `TEXTGEN_OT_about` popup with the same content categories and the original author's website/Twitter/Discord links | Done |
| 29 | "About Plugins" submenu auto-registration | Not reproduced as a submenu; attached directly to Help menu instead (see docs/porting-notes.md) | Adapted |
| 30 | Plugin metadata (name, icon, author, version, tags) | `blender_manifest.toml` (extension) / `bl_info` (legacy), crediting the original author and this port's author | Done |

**30/30 features accounted for: 25 Done, 4 Adapted (each with a disclosed
reason in docs/porting-notes.md), 1 N/A (no meaningful equivalent exists).
Nothing was omitted silently.**

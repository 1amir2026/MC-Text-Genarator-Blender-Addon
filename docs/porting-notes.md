# Porting Notes

## Source

The original plugin is `original_source/mc_text_generator.js`, as uploaded:
Blockbench plugin "Text Generator" v2.0.1, by SirJain
(id `mc_text_generator`, min_version `4.2.0`, tags `Deprecated, Minecraft,
Font`). Its public repository is
https://github.com/SirJain0/TextGenerator, and its listing in Blockbench's
official plugin repository (JannisX11/blockbench-plugins `plugins.json`)
declares no license, source URL, or repository field beyond the plugin's
own metadata.

## License situation

Neither the uploaded source file nor its upstream repository declares a
license (no `LICENSE` / `LICENSE.MD` file, no SPDX header, no license
field in the Blockbench plugin metadata). Blockbench's own plugin-ecosystem
documentation explicitly treats this as the author's choice: plugins "can
be created and/or published as open source, proprietary, or paid
software," with licensing left entirely up to the plugin author. Per the
master prompt's instruction ("If its license or redistribution rights are
unclear, document the issue and avoid making unsupported licensing
claims"), this project does **not** claim the original source is freely
relicensable, and does **not** bundle or redistribute the original
JavaScript file as part of the installable add-on — it is kept only under
`original_source/` for reference/traceability and is excluded from both
built zip packages (confirm with `unzip -l` against `dist/*.zip`).

What this project licenses under GPL-3.0-or-later (see `LICENSE`) is its
own, independently written Python/Blender implementation. The one piece of
information taken directly from the original source is the *functional
data* describing which rectangular blocks make up each letter's shape
(`addon/modules/char_map.py`) — these coordinates are a factual
specification of a pixelated font's geometry (comparable to a font's glyph
metrics), not creative/expressive content, and are reproduced for the sole
purpose of interoperable visual compatibility between the two tools. If
the original author (SirJain) specifies license terms for the source
file, this note should be updated and `LICENSE` revisited accordingly.
Contact links for the original author are included in the add-on's About
popup.

## Behavioral differences from the original, and why

| Blockbench behavior | Blender equivalent | Reason |
|---|---|---|
| `Plugin.register(...)`, `onload`/`onunload` | `register()`/`unregister()` module functions, called by `bl_info`/extension lifecycle | Different plugin systems; this is the direct, idiomatic equivalent. |
| `Blockbench.Dialog` with a custom form | `bpy.types.Operator.invoke_props_dialog` + `draw()` | Closest native Blender UI element to a modal settings form with Generate/Cancel buttons. |
| `new Group(...).init()` nested Outliner groups | `bpy.data.collections.new(...)` nested collections | Blender's collection hierarchy is the direct analogue of Blockbench's Outliner groups. |
| `new Cube({...}).init()` | `bmesh`-built box mesh `Object` | Blockbench's `Cube` is a specialized primitive; Blender has no identical type, so each cube is built explicitly with `bmesh` (8 verts, 6 quad faces, basic UVs) to match the same from/to-corner box shape. |
| `textCube.flip(0, 2.0, true)` (Blockbench-specific UV mirroring) | Not reproduced | This flips UVs for Blockbench's specific Minecraft-cuboid UV-mapping convention, which has no meaning outside Blockbench's texture/UV system. Each generated cube still gets straightforward per-face UVs so it can be unwrapped/textured normally in Blender; this is the closest feasible equivalent and is documented here as a deliberate, disclosed limitation rather than a silent omission. |
| `color: randNum` (random marker color 0-7 on each Cube, used by Blockbench's Outliner marker-color system) | `Collection.color_tag` (`COLOR_01`-`COLOR_08`) set per-character collection | Blender has no per-object marker color; its closest native equivalent is the Outliner's collection color tag, applied once per character so letters are visually distinguishable the same way, guarded by a compatibility check (see docs/compatibility.md). |
| `Format?.id === "java_block"` / `"bedrock_block"` (Blockbench project format awareness) | Both Java and Bedrock warnings evaluated unconditionally | Blender has no concept of a Minecraft-specific "project format," so there is no direct signal for "the user is working in a Java-block project." Both checks are always available and independently toggleable instead, which is a strict superset of the original's capability (nothing is lost; the user can simply leave one unchecked if irrelevant). This is a disclosed, deliberate adaptation, not a silent behavior change. |
| `Undo.initEdit` / `Undo.finishEdit` (Blockbench's undo system) | `bl_options = {"REGISTER", "UNDO"}` on the operator | Standard Blender idiom for a single undoable step; functionally equivalent. |
| `centerElements(0/1/2)` (Blockbench axis centering) | Manual bounding-box computation + `obj.location = -center` per object | Blockbench's helper isn't available in Blender; reimplemented directly against the generated objects' vertex data, verified in `tests/test_addon.py` to center the result on the origin. |

## Coordinate mapping

The original plugin builds each cube as
`from: [x, y - yOffset, z]`, `to: [x2, y2 - yOffset, z2]` with
`rotation: [formData.rotation, 0, 0]` (a Blockbench X-axis rotation), where
`z`/`z2` are always `0`/`depth`. The port maps Blockbench's `(x, y, z)` box
axes onto Blender's `(X, Z, Y)` respectively — i.e. Blockbench's horizontal
text axis is Blender's X, Blockbench's vertical (height) axis is Blender's
Z (up), and Blockbench's depth axis is Blender's Y — and applies the same
rotation as a Blender X-axis rotation after that remap, which was verified
in `tests/test_addon.py` to reproduce the original's width (X), depth (Y),
and height (Z) relationships for known test strings.

## Features explicitly not ported, and why

- **Format-specific size-limit messageboxes tied to Blockbench's active
  project format** — see table above; replaced with an always-available,
  independently toggleable pair of checks.
- **Blockbench "About Plugins" submenu auto-registration machinery**
  (`addAboutButton()` dynamically creating a `Help > About Plugins >`
  submenu) — Blender's Help menu doesn't have an equivalent nested
  "About Plugins" convention; the About popup is instead attached directly
  under **Help > About Text Generator**.
- **Blockbench's quick-message toast system** (`Blockbench.showQuickMessage`)
  — replaced with the operator's standard `self.report(...)` mechanism,
  which Blender shows in the status bar / info log, the native equivalent.

No feature was silently dropped; every item in `docs/features.md`'s
checklist is accounted for as Implemented, Adapted (with the reasoning
above), or explicitly listed here.

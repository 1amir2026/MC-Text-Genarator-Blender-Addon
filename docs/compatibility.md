# Compatibility

## Supported Blender versions

| Target | Package | Minimum | Status |
|---|---|---|---|
| Blender 3.6 LTS - 4.1.x | `-legacy-` zip, classic add-on install | 3.6.0 | Static analysis only (see docs/testing.md) — no 3.6-4.1 runtime was available in this environment. |
| Blender 4.2 - 4.x | `-extension-` zip, Extensions platform install | 4.2.0 | Static analysis; API used is unchanged in all 4.x releases checked. |
| Blender 5.x | `-extension-` zip, Extensions platform install | — | **Actually tested**: full registration, generation, and extension install/uninstall verified on headless Blender 5.2.3. |

`blender_manifest.toml` declares `blender_version_min = "4.2.0"`, which is
the minimum version the Extensions platform itself supports — this add-on
does not use any API newer than 4.2.

## Two install formats, one codebase

Blender 4.2 replaced the old "drop a folder in `scripts/addons`, define a
`bl_info` dict" model with the Extensions platform (`blender_manifest.toml`
+ a repo-managed install). Both are supported from the same `addon/`
source tree:

- The **extension** package ships `addon/` as-is, including
  `blender_manifest.toml`. Blender derives the add-on's `bl_info`-equivalent
  metadata from that manifest automatically; no `bl_info` dict is present
  or needed in `addon/__init__.py`.
- The **legacy** package ships the same `addon/` tree but swaps in
  `scripts/templates/legacy_init.py` as `__init__.py`, which adds a
  classic `bl_info` dictionary and otherwise does exactly the same
  `ui.register()` / `ui.unregister()` call. `blender_manifest.toml` is
  excluded from this package since pre-4.2 Blender does not read it.

`scripts/build.py` produces both from one source tree so there is never a
risk of the two packages' Python code drifting apart.

## API usage and version sensitivity

- `bpy.types.PropertyGroup`, `bpy.props.*`, `bpy.types.Operator`,
  `bpy.types.Panel`: stable across the entire 3.6-5.x range.
- `bmesh` box construction and `bm.loops.layers.uv.new(...)`: stable across
  the entire supported range.
- `Collection.color_tag`: introduced in Blender 2.93 and present through
  5.x. `modules/compat.py` guards its use with a runtime RNA property
  check (`"color_tag" in bpy.types.Collection.bl_rna.properties`) rather
  than `hasattr()` on the type object, because `hasattr()` on an RNA type
  (as opposed to an instance) does not reliably reflect property
  availability. This makes the add-on degrade gracefully (no color tags,
  no error) on a hypothetical future Blender build that removed the
  property, without requiring a version-number allowlist.
- `window_manager.invoke_props_dialog` / `invoke_popup`: stable across the
  entire supported range.
- `bpy.ops.extensions.package_install_files` / `package_uninstall`: only
  present on Blender 4.2+, and is never called by the add-on itself — it
  is only used by this project's own test tooling to verify the extension
  package installs correctly.

No third-party Python packages are required at runtime; the add-on only
imports `bpy`, `bmesh`, `mathutils`, and the Python standard library.

## Known compatibility gaps

- **Blender 2.8x and earlier**: not targeted. `bl_info["blender"]` in the
  legacy template is set to `(3, 6, 0)` as the declared floor, matching the
  master prompt's instruction to use 3.6 LTS as the legacy baseline; the
  code likely also runs on earlier 2.9x/3.x releases given the stable APIs
  used, but this was not tested and is not claimed as supported.
- **Blender 3.6-4.1 runtime**: genuinely untested in this environment (no
  such build was installable here). Treat as "implemented, not yet
  verified" per docs/testing.md until someone runs it on an actual 3.6-4.1
  install.

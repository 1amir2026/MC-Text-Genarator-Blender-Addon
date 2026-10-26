# Blocky Text Generator for Blender

A Blender add-on that generates blocky, Minecraft-style 3D text, ported from
the Blockbench plugin **Text Generator** by SirJain
(https://github.com/SirJain0/TextGenerator).

## Features

- Generates Minecraft-style blocky letters (a-z, 0-9, and common punctuation)
  as real mesh objects, organized into collections.
- Adjustable letter spacing, word spacing, depth (extrusion thickness) and
  rotation (slant), matching the original plugin's controls.
- Optional drop-shadow "layer" generation when depth is 0, identical to the
  original's `generateLayer` option.
- Multi-line text using a backslash (`\`) as a line break, exactly like the
  original plugin.
- Non-blocking size warnings for Minecraft Java Edition (48x48x48) and
  Bedrock Edition (30x30x30) block/item unit limits, each independently
  toggleable.
- An "About" popup with information about the add-on and the original
  plugin's author/links.
- Available from the 3D Viewport sidebar (**Text Gen** tab), from
  **Add > Mesh > Blocky Text**, and from **Help > About Text Generator**.

See [docs/features.md](docs/features.md) for the full feature-parity
checklist against the original plugin.

## Supported Blender versions

- **Blender 3.6 LTS – 4.1.x**: install the legacy package as a classic
  add-on (`blocky_text_generator-legacy-vX.Y.Z.zip`).
- **Blender 4.2 and newer** (including 5.x): install the extension package
  through the Extensions system (`blocky_text_generator-extension-vX.Y.Z.zip`).

Actually tested: Blender 5.2.3 (headless `bpy`), covering add-on
registration, the extension install/enable/uninstall flow, and all
generation features. See [docs/testing.md](docs/testing.md) for exactly
what was and wasn't verified on real Blender releases.

## Installation

See [docs/installation.md](docs/installation.md) for full, version-specific
steps. Short version:

- **4.2+**: Edit > Preferences > Get Extensions > the dropdown (⌄) in the
  top-right > Install from Disk... > select the `-extension-` zip.
- **3.6 – 4.1**: Edit > Preferences > Add-ons > Install... > select the
  `-legacy-` zip > enable "Text Generator (Blocky Minecraft Text)".

## Usage

1. Open the 3D Viewport sidebar (`N`) and select the **Text Gen** tab, or
   use **Add > Mesh > Blocky Text**.
2. Enter your text, adjust letter/word spacing, depth, and rotation.
3. Click **Generate**. The letters are created as a new collection of mesh
   objects, selected and centered on the origin.

See [docs/user-guide.md](docs/user-guide.md) for details on every option.

## Project layout

```
blockbench_text_generator/
├── addon/              # The installable add-on source
├── original_source/    # The original Blockbench plugin (reference/spec)
├── docs/                # Full documentation
├── tests/               # Automated tests (char-map fidelity + functional)
├── scripts/             # Build tooling and legacy __init__.py template
├── dist/                # Built, installable zip packages
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

## License

See [LICENSE](LICENSE) and [docs/porting-notes.md](docs/porting-notes.md)
for a full explanation: the original Blockbench plugin carries no declared
license, so this port's Blender-side code (everything under `addon/`) is
released separately under GPL-3.0-or-later, and the character-shape *data*
(which letters are made of which rectangles) is treated as an uncopyrightable
functional fact reproduced for compatibility, not as copying creative
expression from the original source file.

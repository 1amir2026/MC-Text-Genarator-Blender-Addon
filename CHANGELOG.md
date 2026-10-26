# Changelog

All notable changes to this project are documented in this file.

## [1.0.0] - 2026-10-26

### Added

- Initial release: a full Blender port of the Blockbench "Text Generator"
  plugin (v2.0.1) by SirJain.
- Blocky Minecraft-style text generation for a-z, 0-9, and the punctuation
  set supported by the original plugin (`. ! - + : ; , ' ? [ ( ] ) / $` and
  space).
- Letter spacing, word spacing, depth, and rotation controls.
- Multi-line text via the `\` line-break character.
- Optional drop-shadow layer generation (depth = 0 only).
- Non-blocking Java (48 units) and Bedrock (30 units) size warnings, each
  independently toggleable.
- 3D Viewport sidebar panel ("Text Gen" tab), Add Mesh menu entry, and About
  popup under the Help menu.
- Legacy add-on package (Blender 3.6 - 4.1) and Extensions-platform package
  (Blender 4.2+) build targets.
- Automated tests: character-map fidelity against the original source, and
  functional/registration tests run against headless Blender 5.2.3.

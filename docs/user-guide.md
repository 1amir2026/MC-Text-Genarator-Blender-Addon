# User Guide

## Where to find it

- **3D Viewport Sidebar**: press `N`, open the **Text Gen** tab.
- **Add Menu**: `Shift+A` in the 3D Viewport > Mesh > **Blocky Text**.
- **Help Menu**: Top bar > Help > **About Text Generator**.

Both the sidebar panel and the Add Mesh menu item open the same generation
operator; the sidebar additionally keeps your last-used settings on the
scene so they persist between generations.

## Options

| Option | Default | Matches original field | Description |
|---|---|---|---|
| Enter Text | (empty) | `input` | The text to generate. Case-insensitive — it is lowercased before lookup, exactly like the original. Leaving it blank and pressing Generate shows an error, exactly like the original. |
| Letter Spacing | 0.3 | `letterSpace` | Extra gap added after each character. |
| Word Spacing | 1.0 | `wordSpace` | Width used for the space character. |
| Depth | 4.0 | `depth` | Extrusion thickness of each letter along Blender's Y axis. 0 makes flat letters. |
| Rotation | 0° (range -45° to 45°) | `rotation` | Slants the text by rotating each cube around the X axis. |
| Generate Layer | Off | `generateLayer` | Only shown/used when Depth is 0. Adds a second, slightly offset copy of the letters (useful as a drop-shadow layer), exactly like the original's conditional checkbox. |
| Show Java Block/Item Warnings | On | `javaCheckbox` | Warns (non-blocking) if the text would exceed Minecraft Java Edition's 48x48x48 unit model limit. |
| Show Bedrock Block Warnings | On | `bedrockCheckbox` | Warns (non-blocking) if the text would exceed Minecraft Bedrock Edition's 30x30x30 unit model limit. |

## Supported characters

Lowercase letters a-z, digits 0-9, and these punctuation marks:
`. ! - + : ; , ' ? [ ( ] ) / $` and the space character. This is the exact
character set from the original plugin. Any other character is skipped
and reported in a warning after generation, exactly as the original did
with "Skipped over invalid character(s)."

## Multi-line text

Type a backslash (`\`) anywhere in the text to start a new line, exactly
like the original plugin's "To make new lines: Type `\`" behavior.

## What gets created

Generating text creates one new collection named `text_<your text>`,
containing one sub-collection per character (`character_<letter>`), each
holding the mesh cube objects for that letter's shape. If "Generate Layer"
produced extra geometry, those live in a `layer_base` sub-collection with
its own `layer_character_<letter>` groups, mirroring the original's
`layerBaseGroup` / `layerGroup` outliner structure.

The generated objects are automatically selected and centered on the world
origin on all three axes after creation, matching the original's
`centerText()` behavior.

## Size warnings

Unlike Blockbench, Blender has no file-format concept (`Format.id`), so
both warnings are always evaluated against the generated text's bounding
size rather than against an active project format. They are purely
informational: generation still completes and the geometry is kept, exactly
as in the original plugin ("Your text has still been generated.").

## Undo

Generation is a single undoable operator step (`bl_options = {"REGISTER",
"UNDO"}`), so `Ctrl+Z` removes everything it created in one step, and the
operator's settings can be adjusted afterward from the "Adjust Last
Operation" panel in the bottom-left of the viewport.

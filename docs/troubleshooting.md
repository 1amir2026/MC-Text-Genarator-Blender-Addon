# Troubleshooting

**"Text Gen" tab doesn't appear in the sidebar.**
Confirm the add-on is actually enabled: Preferences > Add-ons (legacy) or
Preferences > Get Extensions (4.2+), search "Text Generator". If it's
enabled but still missing, make sure you're in the 3D Viewport and the
sidebar is open (`N` key).

**Nothing happens when I click Generate / I see an error about a blank text
field.**
The text field was empty when you confirmed the dialog. Enter at least one
character.

**Some characters are missing from my generated text.**
The add-on reports "Skipped N invalid character(s)" for anything outside
the supported set (a-z, 0-9, and `. ! - + : ; , ' ? [ ( ] ) / $` plus
space), exactly like the original Blockbench plugin. Uppercase letters are
fine — they're lowercased automatically.

**"Generate Layer" checkbox is missing.**
It's only shown when Depth is 0, matching the original plugin's conditional
field. Set Depth to 0 first.

**A size-limit warning appears even though I don't care about Minecraft
block limits.**
Uncheck "Show Java Block/Item Warnings" and/or "Show Bedrock Block
Warnings" in the dialog or sidebar — these are just informational and never
prevent generation.

**Installing the wrong package.**
Blender 4.2+ wants the `-extension-` zip (installed through Get
Extensions); Blender 3.6-4.1 wants the `-legacy-` zip (installed through
Add-ons > Install). Installing the extension zip on < 4.2 Blender, or the
legacy zip's folder structure through the 4.2+ Extensions UI, will fail or
not appear — use the matching installer for your version, see
docs/installation.md.

**Disabling then re-enabling the add-on seems to leave stale menu entries
or errors in the console.**
This was tested for exactly this failure mode (`tests/test_addon.py`
performs two full register/unregister cycles) and did not reproduce in
headless Blender 5.2.3. If you do see this, please file an issue with your
exact Blender version and console output.

**I get a Python traceback mentioning `color_tag`.**
This would indicate a Blender build where
`Collection.bl_rna.properties` doesn't expose `color_tag` in the way this
add-on's compatibility check expects. Please report your exact Blender
version — see docs/compatibility.md for how this is currently detected.

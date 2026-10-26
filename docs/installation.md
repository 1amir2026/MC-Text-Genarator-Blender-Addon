# Installation

Two packages are built from this project, because Blender 4.2 introduced a
new Extensions platform with its own package format that is not compatible
with the older add-on installer, and because this project targets both.

## Blender 4.2 and newer (recommended, includes 5.x)

File: `dist/blocky_text_generator-extension-v1.0.0.zip`

1. Open Blender.
2. Go to **Edit > Preferences > Get Extensions**.
3. Click the dropdown arrow (⌄) in the top-right corner of the Get
   Extensions tab and choose **Install from Disk...**.
4. Select `blocky_text_generator-extension-v1.0.0.zip`.
5. The add-on is installed and enabled automatically.
6. Confirm it is active under **Preferences > Add-ons**, searching for
   "Text Generator".

This package was verified with `bpy.ops.extensions.package_install_files`
in headless Blender 5.2.3: it installs, auto-enables, and uninstalls
cleanly (see [testing.md](testing.md)).

## Blender 3.6 LTS through 4.1.x (legacy add-on format)

File: `dist/blocky_text_generator-legacy-v1.0.0.zip`

1. Open Blender.
2. Go to **Edit > Preferences > Add-ons**.
3. Click **Install...** (top-right of the Add-ons tab).
4. Select `blocky_text_generator-legacy-v1.0.0.zip`.
5. Find "Text Generator (Blocky Minecraft Text)" in the list and enable its
   checkbox.

## Verifying the install

After installing with either method, open the 3D Viewport, press `N` to
open the sidebar, and look for a **Text Gen** tab. You can also check
**Add > Mesh > Blocky Text** and **Help > About Text Generator**.

## Uninstalling

- **Extensions (4.2+)**: Preferences > Get Extensions > find the add-on >
  the dropdown next to it > Uninstall. (Also testable/scriptable via
  `bpy.ops.extensions.package_uninstall`.)
- **Legacy (3.6-4.1)**: Preferences > Add-ons > find the add-on > Remove.

## Building the packages yourself

```
python3 scripts/build.py
```

This regenerates both zips in `dist/` from the source in `addon/`.

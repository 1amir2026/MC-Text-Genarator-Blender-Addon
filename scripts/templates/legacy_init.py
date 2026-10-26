bl_info = {
    "name": "Text Generator (Blocky Minecraft Text)",
    "author": "Ported for Blender by Artin (1amir2026); original Blockbench plugin by SirJain",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Add > Mesh > Blocky Text, View3D > Sidebar > Text Gen",
    "description": "Generates blocky Minecraft-style text as 3D mesh objects",
    "warning": "",
    "doc_url": "https://github.com/1amir2026/blockbench-text-generator-blender",
    "category": "Add Mesh",
}

from . import ui


def register():
    ui.register()


def unregister():
    ui.unregister()

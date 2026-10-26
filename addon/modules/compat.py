import bpy

BLENDER_VERSION = bpy.app.version
IS_EXTENSIONS_CAPABLE = BLENDER_VERSION >= (4, 2, 0)
HAS_COLLECTION_COLOR_TAG = BLENDER_VERSION >= (2, 93, 0)


def supports_collection_color_tag() -> bool:
    if not HAS_COLLECTION_COLOR_TAG:
        return False
    return "color_tag" in bpy.types.Collection.bl_rna.properties

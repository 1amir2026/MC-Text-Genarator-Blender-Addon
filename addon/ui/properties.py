import bpy


class TEXTGEN_PG_settings(bpy.types.PropertyGroup):
    input_text: bpy.props.StringProperty(
        name="Enter Text",
        description="The text that will be converted into 3D geometry",
        default="",
    )
    letter_space: bpy.props.FloatProperty(
        name="Letter Spacing",
        description="The amount of space between each letter",
        default=0.3,
        min=0.0,
    )
    word_space: bpy.props.FloatProperty(
        name="Word Spacing",
        description="The amount of space between words",
        default=1.0,
        min=0.0,
    )
    depth: bpy.props.FloatProperty(
        name="Depth",
        description="The thickness of the letters. If 0, the letters will appear flat",
        default=4.0,
        min=0.0,
    )
    rotation: bpy.props.FloatProperty(
        name="Rotation",
        description="The rotation (slant) of the text, in degrees",
        default=0.0,
        min=-45.0,
        max=45.0,
    )
    generate_layer: bpy.props.BoolProperty(
        name="Generate Layer",
        description=(
            "Generates a second layer of the text which can be used for "
            "things like dropshadows. Only available when Depth is 0"
        ),
        default=False,
    )
    show_java_warning: bpy.props.BoolProperty(
        name="Show Java Block/Item Warnings",
        description=(
            "Warn when the generated text exceeds the 48x48x48 unit limit "
            "used by Minecraft Java Edition block/item models"
        ),
        default=True,
    )
    show_bedrock_warning: bpy.props.BoolProperty(
        name="Show Bedrock Block Warnings",
        description=(
            "Warn when the generated text exceeds the 30x30x30 unit limit "
            "used by Minecraft Bedrock Edition block models"
        ),
        default=True,
    )


CLASSES = (TEXTGEN_PG_settings,)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.text_generator_settings = bpy.props.PointerProperty(
        type=TEXTGEN_PG_settings
    )


def unregister():
    del bpy.types.Scene.text_generator_settings
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)

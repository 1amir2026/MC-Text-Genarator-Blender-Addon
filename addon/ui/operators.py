import bpy

from ..modules.generator import (
    GenerationSettings,
    exceeds_bedrock_limit,
    exceeds_java_limit,
    generate_text,
)

WEBSITE_URL = "https://sirjain0.github.io/"
TWITTER_URL = "https://twitter.com/SirJain2"
DISCORD_URL = "https://discord.gg/wM4CKTbFVN"
PORT_REPO_URL = "https://github.com/1amir2026/blockbench-text-generator-blender"


def _sync_settings_from_operator(scene_settings, op) -> None:
    scene_settings.input_text = op.input_text
    scene_settings.letter_space = op.letter_space
    scene_settings.word_space = op.word_space
    scene_settings.depth = op.depth
    scene_settings.rotation = op.rotation
    scene_settings.generate_layer = op.generate_layer
    scene_settings.show_java_warning = op.show_java_warning
    scene_settings.show_bedrock_warning = op.show_bedrock_warning


def _init_operator_from_settings(op, scene_settings) -> None:
    op.input_text = scene_settings.input_text
    op.letter_space = scene_settings.letter_space
    op.word_space = scene_settings.word_space
    op.depth = scene_settings.depth
    op.rotation = scene_settings.rotation
    op.generate_layer = scene_settings.generate_layer
    op.show_java_warning = scene_settings.show_java_warning
    op.show_bedrock_warning = scene_settings.show_bedrock_warning


class TEXTGEN_OT_generate_text(bpy.types.Operator):
    bl_idname = "object.textgen_generate_text"
    bl_label = "Generate Text"
    bl_description = "Input some text and generate blocky Minecraft-style letters"
    bl_options = {"REGISTER", "UNDO"}

    input_text: bpy.props.StringProperty(name="Enter Text", default="")
    letter_space: bpy.props.FloatProperty(name="Letter Spacing", default=0.3, min=0.0)
    word_space: bpy.props.FloatProperty(name="Word Spacing", default=1.0, min=0.0)
    depth: bpy.props.FloatProperty(name="Depth", default=4.0, min=0.0)
    rotation: bpy.props.FloatProperty(name="Rotation", default=0.0, min=-45.0, max=45.0)
    generate_layer: bpy.props.BoolProperty(name="Generate Layer", default=False)
    show_java_warning: bpy.props.BoolProperty(name="Show Java Block/Item Warnings", default=True)
    show_bedrock_warning: bpy.props.BoolProperty(name="Show Bedrock Block Warnings", default=True)

    def invoke(self, context, event):
        scene_settings = context.scene.text_generator_settings
        _init_operator_from_settings(self, scene_settings)
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "input_text")
        layout.separator()
        layout.prop(self, "letter_space")
        layout.prop(self, "word_space")
        layout.prop(self, "depth")
        layout.prop(self, "rotation", slider=True)
        if self.depth == 0.0:
            layout.prop(self, "generate_layer")
        layout.separator()
        layout.prop(self, "show_java_warning")
        layout.prop(self, "show_bedrock_warning")

    def execute(self, context):
        scene_settings = context.scene.text_generator_settings
        _sync_settings_from_operator(scene_settings, self)

        if self.input_text == "":
            self.report({"ERROR"}, "Make sure you don't leave the text field blank")
            return {"CANCELLED"}

        settings = GenerationSettings(
            text=self.input_text,
            letter_space=self.letter_space,
            word_space=self.word_space,
            depth=self.depth,
            rotation_degrees=self.rotation,
            generate_layer=self.generate_layer,
        )

        bpy.ops.object.select_all(action="DESELECT")

        result = generate_text(context, settings)

        if result.invalid_char_count == 0:
            self.report({"INFO"}, "Generated text: '%s'" % self.input_text)
        else:
            self.report(
                {"WARNING"},
                "Generated text: '%s'. Skipped %d invalid character(s)."
                % (self.input_text, result.invalid_char_count),
            )

        if self.show_java_warning and exceeds_java_limit(result, self.letter_space):
            self.report(
                {"WARNING"},
                "Generated text exceeds the 48x48x48 unit limit used by Minecraft "
                "Java Edition block/item models. Scale it down with Object > Transform "
                "> Scale before exporting.",
            )

        if self.show_bedrock_warning and exceeds_bedrock_limit(result, self.letter_space):
            self.report(
                {"WARNING"},
                "Generated text exceeds the 30x30x30 unit limit used by Minecraft "
                "Bedrock Edition block models. Scale it down with Object > Transform "
                "> Scale before exporting.",
            )

        return {"FINISHED"}


class TEXTGEN_OT_about(bpy.types.Operator):
    bl_idname = "object.textgen_about"
    bl_label = "About Text Generator"
    bl_description = "Show information about the Text Generator add-on"
    bl_options = {"REGISTER"}

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=420)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Text Generator", icon="FILE_FONT")
        col.label(text="Generates blocky Minecraft-style text as 3D mesh objects.")
        col.separator()
        col.label(text="Worth noting:")
        col.label(text="- Fonts are a replica, not from official Minecraft font files.")
        col.label(text="- To make a new line, type a backslash: \\")
        col.separator()
        col.label(text="How to use:")
        col.label(text="Add > Mesh > Blocky Text, or the Text Gen sidebar tab.")
        col.separator()
        col.label(text="Ported from the Blockbench 'Text Generator' plugin by SirJain.")
        col.label(text="Original plugin has no declared license; see porting-notes.md.")
        col.separator()
        row = col.row(align=True)
        op = row.operator("wm.url_open", text="Original Author's Website", icon="URL")
        op.url = WEBSITE_URL
        row = col.row(align=True)
        op = row.operator("wm.url_open", text="Original Author's Twitter", icon="URL")
        op.url = TWITTER_URL
        row = col.row(align=True)
        op = row.operator("wm.url_open", text="Original Author's Discord", icon="URL")
        op.url = DISCORD_URL


CLASSES = (TEXTGEN_OT_generate_text, TEXTGEN_OT_about)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)

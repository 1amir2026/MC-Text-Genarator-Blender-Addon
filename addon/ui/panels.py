import bpy


class TEXTGEN_PT_sidebar(bpy.types.Panel):
    bl_idname = "TEXTGEN_PT_sidebar"
    bl_label = "Text Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Text Gen"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.text_generator_settings

        col = layout.column(align=True)
        col.prop(settings, "input_text")
        col.separator()
        col.prop(settings, "letter_space")
        col.prop(settings, "word_space")
        col.prop(settings, "depth")
        col.prop(settings, "rotation", slider=True)
        if settings.depth == 0.0:
            col.prop(settings, "generate_layer")
        col.separator()
        col.prop(settings, "show_java_warning")
        col.prop(settings, "show_bedrock_warning")

        layout.separator()
        op = layout.operator(
            "object.textgen_generate_text", text="Generate", icon="FILE_FONT"
        )
        op.input_text = settings.input_text
        op.letter_space = settings.letter_space
        op.word_space = settings.word_space
        op.depth = settings.depth
        op.rotation = settings.rotation
        op.generate_layer = settings.generate_layer
        op.show_java_warning = settings.show_java_warning
        op.show_bedrock_warning = settings.show_bedrock_warning

        layout.operator("object.textgen_about", text="About", icon="INFO")


def draw_add_mesh_menu(self, context):
    self.layout.operator(
        "object.textgen_generate_text", text="Blocky Text", icon="FILE_FONT"
    )


def draw_help_menu(self, context):
    self.layout.operator("object.textgen_about", text="About Text Generator")


CLASSES = (TEXTGEN_PT_sidebar,)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.append(draw_add_mesh_menu)
    bpy.types.TOPBAR_MT_help.append(draw_help_menu)


def unregister():
    bpy.types.TOPBAR_MT_help.remove(draw_help_menu)
    bpy.types.VIEW3D_MT_mesh_add.remove(draw_add_mesh_menu)
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)

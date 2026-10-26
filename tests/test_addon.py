import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ADDON_DIR = ROOT / "addon"

FAILURES = []
PASSED = 0


def check(label, condition):
    global PASSED
    if condition:
        PASSED += 1
        print("PASS:", label)
    else:
        FAILURES.append(label)
        print("FAIL:", label)


def load_addon():
    spec = importlib.util.spec_from_file_location(
        "blocky_text_generator",
        str(ADDON_DIR / "__init__.py"),
        submodule_search_locations=[str(ADDON_DIR)],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["blocky_text_generator"] = module
    spec.loader.exec_module(module)
    return module


def collect_objects(collection):
    objs = list(collection.objects)
    for child in collection.children:
        objs.extend(collect_objects(child))
    return objs


def run():
    import bpy
    import mathutils

    addon = load_addon()
    addon.register()
    check("register() completes without error", True)

    check(
        "scene property group is attached",
        hasattr(bpy.context.scene, "text_generator_settings"),
    )
    check(
        "generate operator is registered",
        hasattr(bpy.ops.object, "textgen_generate_text"),
    )
    check("about operator is registered", hasattr(bpy.ops.object, "textgen_about"))

    try:
        bpy.ops.object.textgen_generate_text("EXEC_DEFAULT", input_text="")
        check("empty input is rejected", False)
    except RuntimeError as exc:
        check("empty input is rejected", "blank" in str(exc))

    before = set(bpy.data.collections.keys())
    bpy.ops.object.textgen_generate_text("EXEC_DEFAULT", input_text="###")
    after = set(bpy.data.collections.keys())
    check("all-invalid input leaves no orphan collections", before == after)

    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.textgen_generate_text(
        "EXEC_DEFAULT",
        input_text="Hi!",
        letter_space=0.3,
        word_space=1.0,
        depth=4.0,
        rotation=0.0,
        generate_layer=False,
    )
    root = bpy.data.collections.get("text_Hi!")
    check("root collection created for 'Hi!'", root is not None)
    if root is not None:
        objs = collect_objects(root)
        check("'Hi!' produces 6 cube objects (3+1+2 rects)", len(objs) == 6)

        min_c = mathutils.Vector((1e9, 1e9, 1e9))
        max_c = mathutils.Vector((-1e9, -1e9, -1e9))
        for obj in objs:
            for v in obj.data.vertices:
                w = obj.matrix_world @ v.co
                min_c.x, min_c.y, min_c.z = min(min_c.x, w.x), min(min_c.y, w.y), min(min_c.z, w.z)
                max_c.x, max_c.y, max_c.z = max(max_c.x, w.x), max(max_c.y, w.y), max(max_c.z, w.z)
        center = (min_c + max_c) * 0.5
        check(
            "generated text is centered on the origin",
            all(abs(c) < 1e-5 for c in center),
        )
        check(
            "overall width matches width+letter_space accumulation (9.6 units)",
            abs((max_c.x - min_c.x) - 9.6) < 1e-5,
        )
        check("depth maps to the Y axis (4 units)", abs((max_c.y - min_c.y) - 4.0) < 1e-5)
        check("character height maps to the Z axis (8 units)", abs((max_c.z - min_c.z) - 8.0) < 1e-5)

    bpy.ops.object.textgen_generate_text(
        "EXEC_DEFAULT", input_text="ab\\cd", depth=4.0,
    )
    nl_root = bpy.data.collections.get("text_ab\\cd")
    check(
        "backslash triggers a newline instead of being treated as a glyph",
        nl_root is not None and len(nl_root.children) == 4,
    )

    bpy.ops.object.textgen_generate_text(
        "EXEC_DEFAULT", input_text="L", depth=0.0, generate_layer=True,
    )
    layer_root = bpy.data.collections.get("text_L")
    has_layer_base = layer_root is not None and any(
        c.name.startswith("layer_base") for c in layer_root.children
    )
    check("generate_layer with depth=0 creates a layer_base group", has_layer_base)

    before_x = set(bpy.data.collections.keys())
    bpy.ops.object.textgen_generate_text(
        "EXEC_DEFAULT", input_text="X", depth=4.0, generate_layer=True,
    )
    x_root = bpy.data.collections.get("text_X")
    has_layer_base_x = x_root is not None and any(
        c.name.startswith("layer_base") for c in x_root.children
    )
    check(
        "generate_layer is ignored when depth != 0 (matches original condition)",
        not has_layer_base_x,
    )

    try:
        result = bpy.ops.object.textgen_generate_text(
            "EXEC_DEFAULT", input_text="abcdefghijklmnop", depth=4.0,
        )
        check("long text still finishes (warnings are non-blocking)", result == {"FINISHED"})
    except RuntimeError:
        check("long text still finishes (warnings are non-blocking)", False)

    addon.unregister()
    check(
        "unregister() removes the scene property group",
        not hasattr(bpy.context.scene, "text_generator_settings"),
    )

    addon.register()
    addon.unregister()
    check("a second register/unregister cycle succeeds without duplicate-class errors", True)

    print()
    print("%d passed, %d failed" % (PASSED, len(FAILURES)))
    if FAILURES:
        print("Failures:")
        for f in FAILURES:
            print(" -", f)
        sys.exit(1)


if __name__ == "__main__":
    run()

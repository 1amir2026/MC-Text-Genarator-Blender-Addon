import math
import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import bmesh
import bpy
from mathutils import Matrix, Vector

from .char_map import (
    CHAR_DATA,
    FORMAT_LINE_UNIT,
    LINE_HEIGHT,
    NEWLINE_CHAR,
    char_width,
    is_known_char,
)
from .compat import supports_collection_color_tag

COLOR_TAGS = (
    "COLOR_01", "COLOR_02", "COLOR_03", "COLOR_04",
    "COLOR_05", "COLOR_06", "COLOR_07", "COLOR_08",
)

LAYER_NUDGE = 0.2


@dataclass
class GenerationSettings:
    text: str
    letter_space: float
    word_space: float
    depth: float
    rotation_degrees: float
    generate_layer: bool


@dataclass
class GenerationResult:
    root_collection: Optional[bpy.types.Collection] = None
    created_objects: List[bpy.types.Object] = field(default_factory=list)
    invalid_char_count: int = 0
    text_length: float = 0.0
    num_lines: int = 1
    empty_input: bool = False


def _unique_collection(name: str, parent: bpy.types.Collection) -> bpy.types.Collection:
    coll = bpy.data.collections.new(name)
    parent.children.link(coll)
    return coll


def _rect_to_world_corners(
    rect: Tuple[float, float, float, float],
    depth: float,
    offset_x: float,
    offset_y_line: float,
    extra_nudge: float,
    rotation_matrix: Optional[Matrix],
) -> List[Vector]:
    x0, h0, x1, h1 = rect
    z0, z1 = 0.0, depth

    corners_bb = [
        (x0, h0, z0), (x1, h0, z0), (x1, h1, z0), (x0, h1, z0),
        (x0, h0, z1), (x1, h0, z1), (x1, h1, z1), (x0, h1, z1),
    ]

    world_corners = []
    for bx, by_height, bz_depth in corners_bb:
        world_x = bx + offset_x + extra_nudge
        world_z = by_height - offset_y_line - extra_nudge
        world_y = bz_depth + extra_nudge
        vec = Vector((world_x, world_y, world_z))
        if rotation_matrix is not None:
            vec = rotation_matrix @ vec
        world_corners.append(vec)

    return world_corners


_BOX_FACES = (
    (0, 1, 2, 3),
    (4, 7, 6, 5),
    (0, 4, 5, 1),
    (1, 5, 6, 2),
    (2, 6, 7, 3),
    (3, 7, 4, 0),
)


def _build_box_object(name: str, corners: List[Vector]) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()

    verts = [bm.verts.new(c) for c in corners]
    bm.verts.ensure_lookup_table()

    uv_layer = bm.loops.layers.uv.new("UVMap")

    for face_indices in _BOX_FACES:
        face_verts = [verts[i] for i in face_indices]
        try:
            face = bm.faces.new(face_verts)
        except ValueError:
            continue
        uv_coords = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))
        for loop, uv in zip(face.loops, uv_coords):
            loop[uv_layer].uv = uv

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.normal_update()
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    return obj


def _random_color_tag(rng: random.Random) -> str:
    return COLOR_TAGS[rng.randrange(0, 8)]


def generate_text(context: bpy.types.Context, settings: GenerationSettings) -> GenerationResult:
    result = GenerationResult()

    if settings.text == "":
        result.empty_input = True
        return result

    lowered = settings.text.lower()

    rotation_matrix: Optional[Matrix] = None
    if settings.rotation_degrees != 0.0:
        rotation_matrix = Matrix.Rotation(math.radians(settings.rotation_degrees), 4, "X")

    active_collection = context.collection or context.scene.collection

    root_name = "text_" + settings.text
    root_collection = _unique_collection(root_name, active_collection)
    result.root_collection = root_collection

    layer_base_collection: Optional[bpy.types.Collection] = None

    rng = random.Random()

    offset_x = 0.0
    offset_y_line = 0.0
    num_lines = 1
    text_length = 0.0
    invalid_char_count = 0

    created_objects: List[bpy.types.Object] = []

    for char in lowered:
        if char == NEWLINE_CHAR:
            offset_y_line += LINE_HEIGHT
            offset_x = 0.0
            num_lines += 1
            continue

        if not is_known_char(char):
            invalid_char_count += 1
            continue

        char_collection = _unique_collection("character_" + char, root_collection)
        color_tag = _random_color_tag(rng)
        if supports_collection_color_tag():
            char_collection.color_tag = color_tag

        definition = CHAR_DATA[char]

        layer_char_collection: Optional[bpy.types.Collection] = None
        want_layer = settings.generate_layer and settings.depth == 0.0

        for rect in definition.rects:
            corners = _rect_to_world_corners(
                rect, settings.depth, offset_x, offset_y_line, 0.0, rotation_matrix,
            )
            obj = _build_box_object(root_name, corners)
            char_collection.objects.link(obj)
            created_objects.append(obj)

            if want_layer:
                if layer_base_collection is None:
                    layer_base_collection = _unique_collection("layer_base", root_collection)
                if layer_char_collection is None:
                    layer_char_collection = _unique_collection(
                        "layer_character_" + char, layer_base_collection,
                    )
                    if supports_collection_color_tag():
                        layer_char_collection.color_tag = color_tag

                layer_corners = _rect_to_world_corners(
                    rect, settings.depth, offset_x, offset_y_line, LAYER_NUDGE, rotation_matrix,
                )
                layer_obj = _build_box_object(root_name + "_layer", layer_corners)
                layer_char_collection.objects.link(layer_obj)
                created_objects.append(layer_obj)

        advance = char_width(char, settings.word_space) + settings.letter_space
        offset_x += advance
        text_length += advance

    if not created_objects:
        if root_collection.name in bpy.data.collections:
            for child in list(root_collection.children):
                bpy.data.collections.remove(child)
            active_collection.children.unlink(root_collection)
            bpy.data.collections.remove(root_collection)
        result.root_collection = None
        result.invalid_char_count = invalid_char_count
        result.text_length = text_length
        result.num_lines = num_lines
        return result

    min_corner = Vector((math.inf, math.inf, math.inf))
    max_corner = Vector((-math.inf, -math.inf, -math.inf))
    for obj in created_objects:
        for v in obj.data.vertices:
            min_corner.x = min(min_corner.x, v.co.x)
            min_corner.y = min(min_corner.y, v.co.y)
            min_corner.z = min(min_corner.z, v.co.z)
            max_corner.x = max(max_corner.x, v.co.x)
            max_corner.y = max(max_corner.y, v.co.y)
            max_corner.z = max(max_corner.z, v.co.z)

    center = (min_corner + max_corner) * 0.5

    for obj in created_objects:
        obj.location = -center

    for obj in reversed(created_objects):
        context.view_layer.objects.active = obj
    for obj in created_objects:
        obj.select_set(True)

    result.created_objects = created_objects
    result.invalid_char_count = invalid_char_count
    result.text_length = text_length
    result.num_lines = num_lines
    return result


def exceeds_java_limit(result: GenerationResult, letter_space: float) -> bool:
    effective_length = result.text_length - letter_space
    return effective_length >= 48 or FORMAT_LINE_UNIT * result.num_lines >= 48


def exceeds_bedrock_limit(result: GenerationResult, letter_space: float) -> bool:
    effective_length = result.text_length - letter_space
    return effective_length >= 30 or FORMAT_LINE_UNIT * result.num_lines >= 30

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "addon"))

from modules.char_map import CHAR_DATA

ORIGINAL_SOURCE = ROOT / "original_source" / "mc_text_generator.js"

CHAR_PATTERN = re.compile(
    r'(?P<key>"[^"]"|\$|\w):\s*\{\s*width:\s*(?P<width>formData\.wordSpace|[\d.]+),'
    r'\s*cubes:\s*\[(?P<cubes>.*?)\]\s*\},?',
    re.S,
)


def extract_js_char_map():
    source = ORIGINAL_SOURCE.read_text(encoding="utf-8")
    start = source.index("const charMap = {")
    end = source.index("\n                        }\n", start) + len(
        "\n                        }"
    )
    block = source[start:end]

    data = {}
    for match in CHAR_PATTERN.finditer(block):
        key = match.group("key")
        if key.startswith('"') and key.endswith('"'):
            key = key[1:-1]
        width_raw = match.group("width")
        rects = []
        for cube_match in re.finditer(r"\[([^\]]*)\]", match.group("cubes").strip()):
            nums = [part.strip() for part in cube_match.group(1).split(",") if part.strip()]
            assert len(nums) == 6, (key, nums)
            assert nums[2] == "0" and nums[5] == "formData.depth", (key, nums)
            rects.append((float(nums[0]), float(nums[1]), float(nums[3]), float(nums[4])))
        width = None if width_raw == "formData.wordSpace" else float(width_raw)
        data[key] = (width, tuple(rects))
    return data


def run():
    js_data = extract_js_char_map()
    failures = []

    if set(js_data) != set(CHAR_DATA):
        failures.append(
            "key set mismatch: only in JS=%r only in Python=%r"
            % (set(js_data) - set(CHAR_DATA), set(CHAR_DATA) - set(js_data))
        )

    for key, (width, rects) in js_data.items():
        py_def = CHAR_DATA.get(key)
        if py_def is None:
            continue
        if py_def.width != width:
            failures.append("width mismatch for %r: js=%r py=%r" % (key, width, py_def.width))
        if tuple(py_def.rects) != rects:
            failures.append("rects mismatch for %r" % key)

    if failures:
        print("FAIL: char_map does not match original_source/mc_text_generator.js")
        for f in failures:
            print(" -", f)
        sys.exit(1)

    print("PASS: all %d character entries match the original source exactly" % len(js_data))


if __name__ == "__main__":
    run()

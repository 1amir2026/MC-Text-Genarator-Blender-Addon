import pathlib
import shutil
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ADDON_SRC = ROOT / "addon"
TEMPLATES = ROOT / "scripts" / "templates"
BUILD_DIR = ROOT / "build"
DIST_DIR = ROOT / "dist"
PACKAGE_NAME = "blocky_text_generator"
VERSION = "1.0.0"

IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "blender_manifest.toml")


def clean():
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    DIST_DIR.mkdir(exist_ok=True)


def zip_dir(src_dir: pathlib.Path, zip_path: pathlib.Path, arc_root: str) -> None:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(src_dir.rglob("*")):
            if path.is_dir():
                continue
            arcname = pathlib.Path(arc_root) / path.relative_to(src_dir)
            zf.write(path, arcname.as_posix())


def build_legacy() -> pathlib.Path:
    staging = BUILD_DIR / "legacy" / PACKAGE_NAME
    shutil.copytree(ADDON_SRC, staging, ignore=IGNORE)
    shutil.copy(TEMPLATES / "legacy_init.py", staging / "__init__.py")
    zip_path = DIST_DIR / f"{PACKAGE_NAME}-legacy-v{VERSION}.zip"
    zip_dir(staging.parent, zip_path, "")
    return zip_path


def build_extension() -> pathlib.Path:
    staging = BUILD_DIR / "extension" / PACKAGE_NAME
    shutil.copytree(
        ADDON_SRC, staging, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
    )
    zip_path = DIST_DIR / f"{PACKAGE_NAME}-extension-v{VERSION}.zip"
    zip_dir(staging, zip_path, "")
    return zip_path


def main() -> None:
    clean()
    legacy_zip = build_legacy()
    extension_zip = build_extension()
    print("Legacy package:", legacy_zip)
    print("Extension package:", extension_zip)


if __name__ == "__main__":
    main()

from pathlib import Path
import mkdocs_gen_files

PACKAGE_NAME = "core"
SRC_DIR = Path(PACKAGE_NAME)
API_DOCS_PATH = Path("API")

nav = mkdocs_gen_files.Nav()

for path in sorted(SRC_DIR.rglob("*.py")):
    module_path = path.relative_to(SRC_DIR).with_suffix("")
    doc_path = API_DOCS_PATH / path.relative_to(SRC_DIR).with_suffix(".md")
    module_name = ".".join(module_path.parts)

    # skip __init__.py modules
    if module_name.endswith("__init__"):
        continue

    # Store nav paths relative to API/ (not docs root)
    nav[module_path.parts] = doc_path.relative_to(API_DOCS_PATH).as_posix()

    with mkdocs_gen_files.open(doc_path, "w") as f:
        print(f"::: {PACKAGE_NAME}.{module_name}", file=f)

    mkdocs_gen_files.set_edit_path(doc_path, path)

# Write navigation structure correctly
with mkdocs_gen_files.open(API_DOCS_PATH / "SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())

# Landing page
with mkdocs_gen_files.open(API_DOCS_PATH / "index.md", "w") as f:
    f.write(
        f"# API Reference\n\n"
        f"This section contains the **automatically generated reference documentation** "
        f"for the `{PACKAGE_NAME}` package.\n\n"
        f"Browse the modules below:\n\n"
        f"{{{{ nav('API/SUMMARY.md') }}}}\n"
    )

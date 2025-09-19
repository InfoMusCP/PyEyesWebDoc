# gen_pages.py
"""
Auto-generate API documentation pages with mkdocs-gen-files + mkdocstrings.
"""

from pathlib import Path
import mkdocs_gen_files

# -------- SETTINGS --------
PACKAGE_NAME = "core"
SRC_DIR = Path("PyEyesWeb") / PACKAGE_NAME  # adjust for CI vs local
API_DOCS_PATH = Path("API")
# --------------------------

nav = mkdocs_gen_files.Nav()

# Generate individual module pages and build nav
for path in sorted(SRC_DIR.rglob("*.py")):
    module_path = path.relative_to(SRC_DIR).with_suffix("")
    doc_path = API_DOCS_PATH / path.relative_to(SRC_DIR).with_suffix(".md")

    # Create the full module name including the package
    if module_path.parts:
        module_name = ".".join(module_path.parts)
        full_module_name = f"{PACKAGE_NAME}.{module_name}"
    else:
        continue  # Skip if no module path

    # Skip __init__.py modules
    if module_name.endswith("__init__"):
        continue

    # Add to literate-nav
    nav[module_path.parts] = doc_path.relative_to(API_DOCS_PATH).as_posix()

    # Generate module page with correct syntax
    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(f"# {module_name}\n\n")
        f.write(f"::: {full_module_name}\n")

    mkdocs_gen_files.set_edit_path(doc_path, path)

# Write SUMMARY.md for sidebar navigation
with mkdocs_gen_files.open(API_DOCS_PATH / "SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())

# Generate API landing page
with mkdocs_gen_files.open(API_DOCS_PATH / "index.md", "w") as f:
    f.write(
        f"# API Reference\n\n"
        f"This section contains the automatically generated reference documentation for the `{PACKAGE_NAME}` package.\n\n"
        f"Browse the modules using the sidebar navigation.\n"
    )
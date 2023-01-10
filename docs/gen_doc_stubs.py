"""Mkdocs Code Reference Generator."""

import json
import os
from pathlib import Path

import mkdocs_gen_files

with open("workspace.json", "r") as workspace_file:
    workspace = json.loads(workspace_file.read())

src_root = Path(".")

for project_name, project_path in workspace["projects"].items():
    try:
        with open(os.path.join(project_path, "project.json"), "r") as project_file:
            project = json.loads(project_file.read())
            custom_patterns = [
                # # OpenAPI Specs
                # (f"{project_path}/docs/openapi/*.json", False),
                # (f"{project_path}/docs/openapi/*.yml", False),

                # Markdowns
                (f"{project_path}/*.md", True),

                # # API Config
                # (f"{project_path}/docs/source/*.md", True),

                # # TypeScript Typedoc
                # (f"{project_path}/typedoc/**/*.md", False),

                # # Images
                # (f"{project_path}/docs/**/*.jpg", False),
                # (f"{project_path}/docs/**/*.png", False)
            ]

            for pattern, edit_path in custom_patterns:
                for path in src_root.glob(pattern):
                    doc_path = Path("reference", path.relative_to(src_root))
                    with mkdocs_gen_files.open(doc_path, "wb") as f:
                        f.write(path.read_bytes())

                    if edit_path:
                        mkdocs_gen_files.set_edit_path(doc_path, f"../{path}")

            # for path in src_root.glob(f"{project['sourceRoot']}/**/*[!__init__].py"):
            #     doc_path = Path("reference", path.relative_to(src_root)).with_suffix(".md")
            #     doc_normalized_path = str(doc_path).replace(project_path, f"{project_path}/code_reference")
            #     with mkdocs_gen_files.open(doc_normalized_path, "w") as f:
            #         ident = ".".join(path.with_suffix("").parts)
            #         f.write(f"::: {ident}")

            #     mkdocs_gen_files.set_edit_path(doc_normalized_path, f"../{path}")
    except Exception:
        pass

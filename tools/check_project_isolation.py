"""Validate that projects in this repository remain isolated.

This script enforces lightweight repository boundaries:
- No root-level shared Python dependency/config files.
- Each project owns its own README and requirements file.
- Python source files do not reference sibling project folder names.
"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
PROJECTS = [
    "recommendationsystem_ibmcommunity_project",
    "crisp_dm_breast_cancer_project",
    "data_science_pipeline_project",
    "data_science_dashboard_project",
]

FORBIDDEN_ROOT_FILES = [
    "requirements.txt",
    "pyproject.toml",
    "setup.py",
]


def check_root_files(errors: list[str]) -> None:
    for file_name in FORBIDDEN_ROOT_FILES:
        file_path = ROOT / file_name
        if file_path.exists():
            errors.append(
                f"Root-level {file_name} found. Keep dependencies/config project-scoped."
            )


def check_project_basics(errors: list[str]) -> None:
    for project in PROJECTS:
        project_dir = ROOT / project
        if not project_dir.is_dir():
            errors.append(f"Missing project directory: {project}")
            continue

        required_files = ["README.md", "requirements.txt"]
        for req in required_files:
            req_path = project_dir / req
            if not req_path.exists():
                errors.append(f"Missing {req} in {project}")


def check_cross_project_references(errors: list[str]) -> None:
    for project in PROJECTS:
        project_dir = ROOT / project
        if not project_dir.exists():
            continue

        sibling_names = [name for name in PROJECTS if name != project]

        for py_file in project_dir.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                content = py_file.read_text(encoding="latin-1")

            for sibling in sibling_names:
                if sibling in content:
                    rel_path = py_file.relative_to(ROOT)
                    errors.append(
                        f"Cross-project reference in {rel_path}: contains '{sibling}'"
                    )


def main() -> int:
    errors: list[str] = []
    check_root_files(errors)
    check_project_basics(errors)
    check_cross_project_references(errors)

    if errors:
        print("Project isolation check failed:\n")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Project isolation check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
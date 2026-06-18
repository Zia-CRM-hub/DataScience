# DataScience

AI and data science projects covering recommendation systems, healthcare analytics, retail modeling, and dashboard development.

## Repository Overview

This repository contains independent, portfolio-style projects. Each project has its own `README.md`, code/notebook assets, and `requirements.txt` file.

| Project | Focus Area | Main Entry Point |
|---|---|---|
| `data_science_recommendation_system_project` | Recommender systems (rank-based, collaborative, content-based, SVD) | `recommendationsystem_ibmcommunity_analysis.ipynb` |
| `crisp_dm_breast_cancer_project` | CRISP-DM classification workflow for breast cancer diagnosis | `crisp_dm_breast_cancer_analysis.ipynb` |
| `data_science_pipeline_project` | End-to-end ML pipeline for product recommendation prediction | `train.py` |
| `data_science_dashboard_project` | SQLite + Python package + FastHTML dashboard | `report/dashboard.py` |

## Prerequisites

- Python 3.9+
- `pip` for dependency installation
- Jupyter (for notebook-based projects)

## Quick Start

Clone and enter the repository:

```bash
git clone https://github.com/Zia-CRM-hub/DataScience.git
cd DataScience
```

Install dependencies per project:

```bash
cd <project_folder>
python -m pip install -r requirements.txt
```

## Running Projects

Notebook projects:

```bash
cd data_science_recommendation_system_project
jupyter notebook recommendationsystem_ibmcommunity_analysis.ipynb
```

```bash
cd crisp_dm_breast_cancer_project
jupyter notebook crisp_dm_breast_cancer_analysis.ipynb
```

Script-based ML project:

```bash
cd data_science_pipeline_project
python train.py
python -m pytest test.py -q
```

Dashboard project:

```bash
cd data_science_dashboard_project
python -m pip install -r requirements.txt
cd python-package
python -m pip install -e .
cd ..
python report/dashboard.py
```

## Notes

- Each project is intentionally self-contained.
- Use a virtual environment (`venv`/conda) per project to avoid dependency conflicts.
- See each project's `README.md` for implementation details and assumptions.

## Project Isolation Policy

To keep all four projects separate and avoid configuration/dependency mixing:

- Do not create root-level shared Python dependency/config files such as `requirements.txt`, `pyproject.toml`, or `setup.py`.
- Install dependencies only from the target project's `requirements.txt`.
- Create and use a dedicated virtual environment inside each project folder.
- Keep project-specific scripts, datasets, and configuration within that project directory.

Example isolated setup workflow:

```bash
cd <project_folder>
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
```

Automated guardrail:

- CI runs `python tools/check_project_isolation.py` on pushes/PRs to ensure these boundaries remain intact.

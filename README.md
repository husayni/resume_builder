# YAML Resume Builder

A Python package that generates professional PDF resumes from YAML files using Jake's LaTeX template. Define your resume content in simple YAML format and convert it to a polished, ATS-friendly PDF with a single command.

[![CI](https://github.com/husayni/resume_builder/actions/workflows/ci.yml/badge.svg)](https://github.com/husayni/resume_builder/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/husayni/resume_builder/branch/main/graph/badge.svg)](https://codecov.io/gh/husayni/resume_builder)
[![PyPI version](https://badge.fury.io/py/yaml-resume-builder.svg)](https://badge.fury.io/py/yaml-resume-builder)

## Prerequisites

- Python 3.8 or higher
- LaTeX installation with `latexmk` command available in your PATH:

### LaTeX Installation

#### Linux (Debian/Ubuntu)
```bash
sudo apt update && sudo apt install texlive-full latexmk
```

#### macOS
Install MacTeX (includes latexmk):
```bash
brew install --cask mactex
```

#### Windows
Install MiKTeX (includes latexmk):
1. Download the MiKTeX Net Installer from https://miktex.org/download
2. Choose "Complete" installation to ensure all required packages are installed
3. MiKTeX will add pdflatex and latexmk to your PATH automatically

## Installation

### From PyPI or GitHub

```bash
# Install from PyPI
pip install yaml-resume-builder

# Or install directly from GitHub
pip install git+https://github.com/husayni/resume_builder.git
```

### For Development

```bash
# Clone the repository
git clone https://github.com/husayni/resume_builder.git
cd resume_builder

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the package in development mode with dev dependencies
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

```bash
# Create a sample YAML resume file
yaml-resume-builder init --output my_resume.yml

# Build a resume from a YAML file
yaml-resume-builder build --input my_resume.yml --output resume.pdf
```

### Python API

```python
from yaml_resume_builder import build_resume

# Build a resume from a YAML file
build_resume(
    input_path="my_resume.yml",
    output_path="resume.pdf"
)
```

## YAML Format

The YAML file should have the following structure. Any unknown fields will be ignored with a warning message:

The template includes sections for Education, Experience, Projects, Skills, and Achievements & Publications. All sections are optional - if you don't provide data for a section, it will be empty in the generated resume.

```yaml
name: Your Name
title: Your Title
contact:
  email: your.email@example.com
  phone: "+1 123 456 7890"
  github: yourusername
  linkedin: yourusername
education:
  - school: University Name
    degree: Degree Name
    dates: "2020 - 2024"
    location: City, Country
experience:
  - company: Company Name
    role: Your Role
    dates: "Jan 2023 - Present"
    location: City, Country
    bullets:
      - Accomplishment 1
      - Accomplishment 2
projects:
  - name: Project Name
    technologies: Python, Flask, React, PostgreSQL, Docker
    date: "June 2020 - Present"
    link: https://github.com/yourusername/project
    bullets:
      - Description 1
      - Description 2
skills:
  - category: Languages
    list: [Python, JavaScript, Java]
  - category: Frameworks
    list: [Django, React, Spring]
achievements:
  - title: "Award Name"
    issuer: "Awarding Organization"
    date: "2023"
  - title: "Seminar speaker on 'Topic Name'"
    issuer: "Event Name"
    date: "2022"
publications:
  - title: "Publication Title"
    journal: "Journal or Conference Name"
    date: "January 2023"
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=yaml_resume_builder

# Run linting checks
ruff check .
isort --check --diff .
```

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. To set up pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses the LaTeX resume template created by [Jake Gutierrez](https://github.com/jakegut/resume), which is also licensed under the MIT License.

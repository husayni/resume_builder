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

# Build a resume optimized to fit on one page
yaml-resume-builder build --input my_resume.yml --output resume.pdf --one-page

# Build with debug mode to save the intermediate LaTeX file
yaml-resume-builder build --input my_resume.yml --output resume.pdf --debug
```

### Python API

```python
from yaml_resume_builder import build_resume

# Build a resume from a YAML file
build_resume(
    input_path="my_resume.yml",
    output_path="resume.pdf"
)

# Build a resume optimized to fit on one page
build_resume(
    input_path="my_resume.yml",
    output_path="resume.pdf",
    one_page=True
)

# Build with debug mode enabled
build_resume(
    input_path="my_resume.yml",
    output_path="resume.pdf",
    debug=True
)

# Build with both one-page optimization and debug mode
build_resume(
    input_path="my_resume.yml",
    output_path="resume.pdf",
    debug=True,
    one_page=True
)
```

## One-Page Optimization

The `--one-page` flag (or `one_page=True` in the Python API) automatically optimizes your resume to fit on a single page. This feature uses progressive optimization techniques:

### How It Works

1. **PDF Analysis**: After generating the initial PDF, the tool counts the number of pages
2. **Progressive Optimization**: If the resume exceeds one page, it applies optimization levels in order:
   - **Level 1**: Apply improved spacing optimizations (better section spacing, consistent margins)
   - **Level 2**: Add CormorantGaramond font for more compact text
   - **Level 3**: Reduce font size from 11pt to 10pt with additional spacing adjustments
   - **Level 4**: Reduce margins slightly with more aggressive spacing
   - **Level 5**: Apply maximum spacing reductions and margin adjustments
3. **Automatic Fallback**: If optimization fails, it falls back to the regular build

### Usage Examples

```bash
# CLI usage
yaml-resume-builder build -i resume.yml -o resume.pdf --one-page

# Python API usage
from yaml_resume_builder import build_resume
build_resume("resume.yml", "resume.pdf", one_page=True)
```

### Professional Standards

The optimization maintains professional standards by:
- Keeping font sizes within readable ranges (10pt-11pt)
- Maintaining appropriate margins (minimum 0.35in)
- Preserving content hierarchy and readability
- Only applying changes that improve space efficiency


## YAML Format

The YAML file should have the following structure. Any unknown fields will be ignored with a warning message:

The template includes sections for Education, Experience, Projects, Skills, Achievements, Publications, and Certifications. All sections are optional - if you don't provide data for a section, it will be empty in the generated resume.

```yaml
name: Your Full Name
contact:
  phone: "+1 (123) 456-7890"
  email: your.email@example.com
  linkedin: your-linkedin-username
  github: your-github-username

education:
  - school: University Name
    location: City, State
    degree: Degree Name (e.g., Bachelor of Science in Computer Science)
    dates: "2020 - 2024"

  - school: Another University (if applicable)
    location: City, State
    degree: Another Degree
    dates: "2016 - 2020"

experience:
  - company: Company Name
    role: Your Job Title
    location: City, State
    dates: "Jan 2023 - Present"
    description:
      - "Accomplished [specific achievement] resulting in [specific measurable outcome]"
      - "Led a team of X people to deliver [project/product] that [specific result]"
      - "Implemented [specific technology/process] that improved [specific metric] by X%"

  - company: Previous Company
    role: Previous Job Title
    location: Remote
    dates: "Jun 2021 - Dec 2022"
    description:
      - "Developed [feature/product] using [technologies] that [specific outcome]"
      - "Collaborated with cross-functional teams to [specific achievement]"
      - "Optimized [process/system] resulting in [specific improvement]"

projects:
  - name: Gitlytics
    technologies: [Python, Flask, React, PostgreSQL, Docker]
    date: June 2020 - Present
    link: https://github.com/yourusername/gitlytics
    description:
      - "Developed a full-stack web application using Flask serving a REST API with React as the frontend"
      - "Implemented GitHub OAuth to get data from user's repositories"
      - "Visualized GitHub data to show collaboration"
      - "Used Celery and Redis for asynchronous tasks"

  - name: Simple Paintball
    technologies: [Spigot API, Java, Maven, TravisCI, Git]
    date: May 2018 - May 2020
    link: https://github.com/yourusername/simple-paintball
    description:
      - "Developed a Minecraft server plugin to entertain kids during free time for a previous job"
      - "Published plugin to websites gaining 2K+ downloads and an average 4.5/5-star review"
      - "Implemented continuous delivery using TravisCI to build the plugin upon new a release"
      - "Collaborated with Minecraft server administrators to suggest features and get feedback"

skills:
  - category: Languages
    list: [Python, JavaScript, Java, SQL]
  - category: Frameworks
    list: [React, Django, Spring Boot, Express.js]

  - category: Tools
    list: [Git, Docker, AWS, CI/CD]

achievements:
  - Won "Best Paper Award" at Conference on Software Engineering (2023)
  - Won "Hackathon Winner" at Tech Innovation Summit (2022)
  - Won "First Prize in Regional Coding Competition" at Tech Association (2020)

publications:
  - Innovative Approaches to Software Testing in Cloud Environments, Journal of Software Engineering, January 2023
  - Machine Learning Applications in DevOps Pipelines, International Conference on DevOps, June 2022

certifications:
  - name: AWS Certified Developer - Associate (2023)
    link: https://www.credly.com/badges/your-badge-id
  - name: Google Cloud Certified - Associate Cloud Engineer (2022)
  - "Microsoft Certified: Azure AI Engineer Associate"
  - name: Kubernetes Certified Application Developer
    link: https://www.cncf.io/certification/ckad/
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

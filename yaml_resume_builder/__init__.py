"""YAML Resume Builder Package.

A package to generate PDF resumes from YAML files using LaTeX templates.
"""

import logging

from yaml_resume_builder.builder import build_resume, build_resume_with_optimization

# Configure logging format for all loggers in the package
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

__version__ = "1.0.5"
__all__ = ["build_resume", "build_resume_with_optimization"]

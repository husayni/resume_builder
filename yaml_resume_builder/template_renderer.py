"""Template renderer module.

This module contains functionality for rendering LaTeX templates.
"""

import logging
from typing import Any, Dict, List, Set

# Configure logging
logger = logging.getLogger(__name__)


def escape_latex(text: Any) -> Any:
    """Escape LaTeX special characters.

    Args:
        text (str): The text to escape.

    Returns:
        str: The escaped text.
    """
    if not isinstance(text, str):
        return text

    # Define LaTeX special characters and their escaped versions
    latex_special_chars = {
        "\\": r"\textbackslash{}",  # Must be first to avoid double escaping
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }

    # Replace special characters
    for char, replacement in latex_special_chars.items():
        text = text.replace(char, replacement)

    return text


# Define known fields for validation
KNOWN_ROOT_FIELDS = {"name", "contact", "education", "experience", "projects", "skills"}
KNOWN_CONTACT_FIELDS = {"phone", "email", "linkedin", "github"}
KNOWN_EDUCATION_FIELDS = {"school", "location", "degree", "dates"}
KNOWN_EXPERIENCE_FIELDS = {"company", "role", "location", "dates", "bullets"}
KNOWN_PROJECT_FIELDS = {"name", "technologies", "date", "link", "bullets"}
KNOWN_SKILLS_FIELDS = {"category", "list"}


def validate_root_fields(data: Dict[str, Any]) -> None:
    """Validate root level fields in the data.

    Args:
        data (dict): The data to validate.
    """
    for field in data:
        if field not in KNOWN_ROOT_FIELDS:
            logger.warning(f"Unknown field '{field}' at root level")


def validate_contact_fields(contact_data: Dict[str, Any]) -> None:
    """Validate contact fields in the data.

    Args:
        contact_data (dict): The contact data to validate.
    """
    for field in contact_data:
        if field not in KNOWN_CONTACT_FIELDS:
            logger.warning(f"Unknown field '{field}' in contact section")


def validate_list_entries(
    entries: List[Dict[str, Any]], known_fields: Set[str], section_name: str
) -> None:
    """Validate fields in list entries.

    Args:
        entries (list): The list of entries to validate.
        known_fields (set): The set of known fields for this entry type.
        section_name (str): The name of the section for warning messages.
    """
    for entry in entries:
        if isinstance(entry, dict):
            for field in entry:
                if field not in known_fields:
                    logger.warning(f"Unknown field '{field}' in {section_name} entry")


def validate_data(data: Dict[str, Any]) -> None:
    """Validate the data structure and warn about unknown fields.

    Args:
        data (dict): The data to validate.
    """
    # Validate root level fields
    validate_root_fields(data)

    # Validate contact fields
    if "contact" in data and isinstance(data["contact"], dict):
        validate_contact_fields(data["contact"])

    # Validate education fields
    if "education" in data and isinstance(data["education"], list):
        validate_list_entries(data["education"], KNOWN_EDUCATION_FIELDS, "education")

    # Validate experience fields
    if "experience" in data and isinstance(data["experience"], list):
        validate_list_entries(data["experience"], KNOWN_EXPERIENCE_FIELDS, "experience")

    # Validate project fields
    if "projects" in data and isinstance(data["projects"], list):
        validate_list_entries(data["projects"], KNOWN_PROJECT_FIELDS, "project")

    # Validate skills fields
    if "skills" in data and isinstance(data["skills"], list):
        validate_list_entries(data["skills"], KNOWN_SKILLS_FIELDS, "skills")


def render_template(template_path: str, data: Dict[str, Any]) -> str:
    """Render a LaTeX template with the given data.

    Args:
        template_path (str): Path to the LaTeX template (not used).
        data (dict): Data to render the template with.

    Returns:
        str: The rendered LaTeX content.
    """
    import os

    # Validate the data structure and warn about unknown fields
    validate_data(data)

    # Use our simple template instead
    simple_template_path = os.path.join(os.path.dirname(__file__), "simple_template.tex")
    with open(simple_template_path, "r") as file:
        template_content = file.read()

    # Replace name
    template_content = template_content.replace("{{name}}", escape_latex(data["name"]))

    # Replace contact information
    template_content = template_content.replace("{{phone}}", escape_latex(data["contact"]["phone"]))
    template_content = template_content.replace("{{email}}", escape_latex(data["contact"]["email"]))
    template_content = template_content.replace(
        "{{linkedin}}", escape_latex(data["contact"]["linkedin"])
    )
    template_content = template_content.replace(
        "{{github}}", escape_latex(data["contact"]["github"])
    )

    # Build education section
    education_section = ""
    for edu in data["education"]:
        education_section += r"\resumeSubheading" + "\n"
        education_section += (
            r"  {"
            + escape_latex(edu["school"])
            + r"}{"
            + escape_latex(edu["location"])
            + r"}"
            + "\n"
        )
        education_section += (
            r"  {" + escape_latex(edu["degree"]) + r"}{" + escape_latex(edu["dates"]) + r"}" + "\n"
        )

    # Replace education section
    template_content = template_content.replace("{{education}}", education_section)

    # Build experience section
    experience_section = ""
    for exp in data["experience"]:
        experience_section += r"\resumeSubheading" + "\n"
        experience_section += (
            r"  {" + escape_latex(exp["role"]) + r"}{" + escape_latex(exp["dates"]) + r"}" + "\n"
        )
        experience_section += (
            r"  {"
            + escape_latex(exp["company"])
            + r"}{"
            + escape_latex(exp["location"])
            + r"}"
            + "\n"
        )
        experience_section += r"  \resumeItemListStart" + "\n"
        for bullet in exp["bullets"]:
            experience_section += r"    \resumeItem{" + escape_latex(bullet) + r"}" + "\n"
        experience_section += r"  \resumeItemListEnd" + "\n"

    # Replace experience section
    template_content = template_content.replace("{{experience}}", experience_section)

    # Build projects section
    projects_section = ""
    for project in data["projects"]:
        projects_section += r"\resumeProjectHeading" + "\n"

        # Build project title with name and technologies
        project_title = r"{\textbf{" + escape_latex(project["name"]) + r"}"

        # Add technologies if available
        if "technologies" in project and project["technologies"]:
            project_title += r" $|$ \emph{" + escape_latex(project["technologies"]) + r"}"
        # Otherwise use link if available (for backward compatibility)
        elif "link" in project and project["link"]:
            project_title += r" $|$ \emph{" + escape_latex(project["link"]) + r"}"

        # Add date if available
        if "date" in project and project["date"]:
            project_title += r"}{" + escape_latex(project["date"]) + r"}"
        else:
            project_title += r"}{}"

        projects_section += r"  " + project_title + "\n"
        projects_section += r"  \resumeItemListStart" + "\n"
        for bullet in project["bullets"]:
            projects_section += r"    \resumeItem{" + escape_latex(bullet) + r"}" + "\n"
        projects_section += r"  \resumeItemListEnd" + "\n"

    # Replace projects section
    template_content = template_content.replace("{{projects}}", projects_section)

    # Build skills section
    skills_section = ""
    for skill in data["skills"]:
        skills_section += (
            r"\textbf{"
            + escape_latex(skill["category"])
            + r"}{: "
            + escape_latex(", ".join(skill["list"]))
            + r"} \\"
            + "\n"
        )

    # Replace skills section
    template_content = template_content.replace("{{skills}}", skills_section)

    return template_content

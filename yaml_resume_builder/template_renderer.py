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
KNOWN_ROOT_FIELDS = {
    "name",
    "contact",
    "education",
    "experience",
    "projects",
    "skills",
    "achievements",
    "publications",
}
KNOWN_CONTACT_FIELDS = {"phone", "email", "linkedin", "github"}
KNOWN_EDUCATION_FIELDS = {"school", "location", "degree", "dates"}
KNOWN_EXPERIENCE_FIELDS = {"company", "role", "location", "dates", "bullets"}
KNOWN_PROJECT_FIELDS = {"name", "technologies", "date", "link", "bullets"}
KNOWN_SKILLS_FIELDS = {"category", "list"}
KNOWN_ACHIEVEMENT_FIELDS = {"title", "issuer", "date", "description", "bullets"}
KNOWN_PUBLICATION_FIELDS = {"title", "authors", "journal", "date", "link", "bullets"}


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

    # Validate achievements fields
    if "achievements" in data and isinstance(data["achievements"], list):
        validate_list_entries(data["achievements"], KNOWN_ACHIEVEMENT_FIELDS, "achievement")

    # Validate publications fields
    if "publications" in data and isinstance(data["publications"], list):
        validate_list_entries(data["publications"], KNOWN_PUBLICATION_FIELDS, "publication")


def _build_education_section(data: Dict[str, Any]) -> str:
    """Build the education section of the resume.

    Args:
        data (dict): The resume data.

    Returns:
        str: The formatted education section.
    """
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
    return education_section


def _build_experience_section(data: Dict[str, Any]) -> str:
    """Build the experience section of the resume.

    Args:
        data (dict): The resume data.

    Returns:
        str: The formatted experience section.
    """
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
    return experience_section


def _build_projects_section(data: Dict[str, Any]) -> str:
    """Build the projects section of the resume.

    Args:
        data (dict): The resume data.

    Returns:
        str: The formatted projects section.
    """
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
    return projects_section


def _build_skills_section(data: Dict[str, Any]) -> str:
    """Build the skills section of the resume.

    Args:
        data (dict): The resume data.

    Returns:
        str: The formatted skills section.
    """
    return "".join(
        (
            r"\textbf{"
            + escape_latex(skill["category"])
            + r"}{: "
            + escape_latex(", ".join(skill["list"]))
            + r"} \\"
            + "\n"
        )
        for skill in data["skills"]
    )


def _format_achievement(achievement: Dict[str, Any]) -> str:
    """Format a single achievement entry.

    Args:
        achievement (dict): The achievement data.

    Returns:
        str: The formatted achievement text.
    """
    # Format: Achievement title at Organization (Year)
    achievement_text = ""
    if "title" in achievement:
        achievement_text += escape_latex(achievement["title"])

    if "issuer" in achievement and achievement["issuer"]:
        achievement_text += " at " + escape_latex(achievement["issuer"])

    if "date" in achievement and achievement["date"]:
        achievement_text += " (" + escape_latex(achievement["date"]) + ")"

    return r"    \resumeItem{" + achievement_text + r"}" + "\n"


def _format_publication(publication: Dict[str, Any]) -> str:
    """Format a single publication entry.

    Args:
        publication (dict): The publication data.

    Returns:
        str: The formatted publication text.
    """
    # Format: "Publication title" in Journal (Year)
    publication_text = ""
    if "title" in publication:
        publication_text += r"``" + escape_latex(publication["title"]) + r"''"

    if "journal" in publication and publication["journal"]:
        publication_text += " in " + escape_latex(publication["journal"])

    if "date" in publication and publication["date"]:
        publication_text += " (" + escape_latex(publication["date"]) + ")"

    return r"    \resumeItem{" + publication_text + r"}" + "\n"


def _build_achievements_publications_section(data: Dict[str, Any]) -> str:
    """Build the achievements and publications section of the resume.

    Args:
        data (dict): The resume data.

    Returns:
        str: The formatted achievements and publications section.
        Returns an empty string if both achievements and publications are empty.
    """
    # Check if both achievements and publications are empty
    has_achievements = "achievements" in data and data["achievements"]
    has_publications = "publications" in data and data["publications"]

    # If both are empty, return an empty string
    if not has_achievements and not has_publications:
        return ""

    section = r"\resumeItemListStart" + "\n"

    # Add achievements if available
    if has_achievements:
        for achievement in data["achievements"]:
            section += _format_achievement(achievement)

    # Add publications if available
    if has_publications:
        for publication in data["publications"]:
            section += _format_publication(publication)

    # End the item list
    section += r"  \resumeItemListEnd" + "\n"

    return section


def render_template(data: Dict[str, Any]) -> str:
    """Render a LaTeX template with the given data.

    Args:
        data (dict): Data to render the template with.

    Returns:
        str: The rendered LaTeX content.
    """
    import os

    # Validate the data structure and warn about unknown fields
    validate_data(data)

    # Use our resume template
    resume_template_path = os.path.join(os.path.dirname(__file__), "resume.tex.template")
    with open(resume_template_path, "r") as file:
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

    # Build and replace sections
    template_content = template_content.replace("{{education}}", _build_education_section(data))
    template_content = template_content.replace("{{experience}}", _build_experience_section(data))
    template_content = template_content.replace("{{projects}}", _build_projects_section(data))
    template_content = template_content.replace("{{skills}}", _build_skills_section(data))

    # Build achievements and publications section
    achievements_publications_content = _build_achievements_publications_section(data)

    # If the section is empty, remove the entire section from the template
    if not achievements_publications_content:
        # Remove the section from the template using string replacement
        # Find the section in the template
        section_start = "%-----------Achievements / Publications / Certifications-----------"
        section_end = "%-------------------------------------------"

        # Find the start and end positions of the section
        start_pos = template_content.find(section_start)
        end_pos = template_content.find(section_end, start_pos) + len(section_end)

        if start_pos != -1 and end_pos != -1:
            # Remove the section
            template_content = template_content[:start_pos] + template_content[end_pos + 1 :]
    else:
        # Otherwise, replace the placeholder with the content
        template_content = template_content.replace(
            "{{achievements_publications}}", achievements_publications_content
        )

    return template_content

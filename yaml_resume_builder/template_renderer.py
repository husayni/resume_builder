"""Template renderer module.

This module contains functionality for rendering LaTeX templates.
"""

import logging
from typing import Any, Dict, List, Optional, Set, Union, cast

# Configure logging
logger = logging.getLogger(__name__)


def escape_latex(text: Any) -> str:
    """Escape LaTeX special characters.

    Args:
        text (str): The text to escape.

    Returns:
        str: The escaped text.
    """
    if not isinstance(text, str):
        return cast(str, str(text))

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
    "certifications",
}
KNOWN_CONTACT_FIELDS = {"phone", "email", "linkedin", "github"}
KNOWN_EDUCATION_FIELDS = {"school", "location", "degree", "dates"}
KNOWN_EXPERIENCE_FIELDS = {
    "company",
    "role",
    "location",
    "dates",
    "description",
    "bullets",
}  # Support both formats
KNOWN_PROJECT_FIELDS = {
    "name",
    "technologies",
    "date",
    "link",
    "description",
    "bullets",
}  # Support both formats
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


def _validate_achievements(data: Dict[str, Any]) -> None:
    """Validate achievements section (support both old and new formats)."""
    if "achievements" in data and isinstance(data["achievements"], list):
        for i, achievement in enumerate(data["achievements"]):
            if isinstance(achievement, dict):
                # Old format: validate known fields
                known_fields = {"title", "issuer", "date", "description", "bullets"}
                for field in achievement:
                    if field not in known_fields:
                        logger.warning(f"Unknown field '{field}' in achievement entry")
            elif not isinstance(achievement, str):
                logger.warning(f"Achievement at index {i} should be a string or dict")


def _validate_publications(data: Dict[str, Any]) -> None:
    """Validate publications section (support both old and new formats)."""
    if "publications" in data and isinstance(data["publications"], list):
        for i, publication in enumerate(data["publications"]):
            if isinstance(publication, dict):
                # Old format: validate known fields
                known_fields = {"title", "authors", "journal", "date", "link", "bullets"}
                for field in publication:
                    if field not in known_fields:
                        logger.warning(f"Unknown field '{field}' in publication entry")
            elif not isinstance(publication, str):
                logger.warning(f"Publication at index {i} should be a string or dict")


def _validate_certifications(data: Dict[str, Any]) -> None:
    """Validate certifications section (support both string and dict formats)."""
    if "certifications" not in data or not isinstance(data["certifications"], list):
        return
    for i, certification in enumerate(data["certifications"]):
        if isinstance(certification, dict):
            # New format: validate known fields
            known_fields = {"name", "link"}
            for field in certification:
                if field not in known_fields:
                    logger.warning(f"Unknown field '{field}' in certification entry")
            # Ensure 'name' field is present
            if "name" not in certification:
                logger.warning(f"Certification at index {i} is missing required 'name' field")
        elif not isinstance(certification, str):
            logger.warning(f"Certification at index {i} should be a string or dict")


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

    # Validate achievements, publications, and certifications
    _validate_achievements(data)
    _validate_publications(data)
    _validate_certifications(data)


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
        # Handle both 'description' (new format) and 'bullets' (old format for backward compatibility)
        descriptions = exp.get("description", exp.get("bullets", []))
        for description in descriptions:
            experience_section += r"    \resumeItem{" + escape_latex(description) + r"}" + "\n"
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
            # Handle both list and string formats for technologies
            if isinstance(project["technologies"], list):
                technologies_str = ", ".join(project["technologies"])
            else:
                technologies_str = str(project["technologies"])
            # Only add technologies if the string is not empty
            if technologies_str.strip():
                project_title += r" $|$ \emph{" + escape_latex(technologies_str) + r"}"
        # Otherwise use link if available (for backward compatibility)
        elif "link" in project and project["link"]:
            project_title += r" $|$ \emph{" + escape_latex(project["link"]) + r"}"

        # Add date if available
        if "date" in project and project["date"]:
            project_title += r"}{" + escape_latex(project["date"]) + r"}"
        else:
            project_title += r"}{}"

        projects_section += f"  {project_title}" + "\n"
        projects_section += r"  \resumeItemListStart" + "\n"
        # Handle both 'description' (new format) and 'bullets' (old format for backward compatibility)
        descriptions = project.get("description", project.get("bullets", []))
        for description in descriptions:
            projects_section += r"    \resumeItem{" + escape_latex(description) + r"}" + "\n"
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


def _format_achievement_item(achievement: Union[str, Dict[str, Any]]) -> str:
    """Format a single achievement item (supports both old and new formats)."""
    if isinstance(achievement, str):
        # New format: simple string
        return r"    \resumeItem{" + escape_latex(achievement) + r"}" + "\n"
    elif isinstance(achievement, dict):
        # Old format: structured object
        achievement_text = ""
        if "title" in achievement:
            achievement_text += escape_latex(str(achievement["title"]))
        if "issuer" in achievement and achievement["issuer"]:
            achievement_text += " at " + escape_latex(str(achievement["issuer"]))
        if "date" in achievement and achievement["date"]:
            achievement_text += " (" + escape_latex(str(achievement["date"])) + ")"
        return r"    \resumeItem{" + achievement_text + r"}" + "\n"
    return ""


def _format_publication_item(publication: Union[str, Dict[str, Any]]) -> str:
    """Format a single publication item (supports both old and new formats)."""
    if isinstance(publication, str):
        # New format: simple string
        return r"    \resumeItem{" + escape_latex(publication) + r"}" + "\n"
    elif isinstance(publication, dict):
        # Old format: structured object
        publication_text = ""
        if "title" in publication:
            publication_text += r"``" + escape_latex(str(publication["title"])) + r"''"
        if "journal" in publication and publication["journal"]:
            publication_text += " in " + escape_latex(str(publication["journal"]))
        if "date" in publication and publication["date"]:
            publication_text += " (" + escape_latex(str(publication["date"])) + ")"
        return r"    \resumeItem{" + publication_text + r"}" + "\n"
    return ""


def _format_certification_item(certification: Union[str, Dict[str, Any]]) -> str:
    """Format a single certification item.

    Args:
        certification: Either a string (old format) or dict with 'name' and optional 'link' (new format)

    Returns:
        str: Formatted LaTeX certification item
    """
    if isinstance(certification, str):
        # Old format: simple string
        return r"    \resumeItem{" + escape_latex(certification) + r"}" + "\n"
    elif isinstance(certification, dict):
        # New format: dict with name and optional link
        name = certification.get("name", "")
        link = certification.get("link", "")

        if not link:
            # Format without hyperlink
            return r"    \resumeItem{" + escape_latex(name) + r"}" + "\n"
        # Format with hyperlink
        escaped_name = escape_latex(name)
        escaped_link = escape_latex(link)
        return (
            r"    \resumeItem{\href{"
            + escaped_link
            + r"}{\underline{"
            + escaped_name
            + r"}}}"
            + "\n"
        )
    else:
        # Fallback for unexpected types
        return r"    \resumeItem{" + escape_latex(str(certification)) + r"}" + "\n"


def _build_publications_section(data: Dict[str, Any]) -> str:
    """Build the publications section of the resume.

    Args:
        data (dict): The resume data.

    Returns:
        str: The formatted publications section.
        Returns an empty string if no publications are available.
    """
    if "publications" not in data or not data["publications"]:
        return ""

    section = r"\resumeItemListStart" + "\n"
    for publication in data["publications"]:
        section += _format_publication_item(publication)
    section += r"  \resumeItemListEnd" + "\n"
    return section


def _build_certifications_section(data: Dict[str, Any]) -> str:
    """Build the certifications section of the resume.

    Args:
        data (dict): The resume data.

    Returns:
        str: The formatted certifications section.
        Returns an empty string if no certifications are available.
    """
    if "certifications" not in data or not data["certifications"]:
        return ""

    section = r"\resumeItemListStart" + "\n"
    for certification in data["certifications"]:
        section += _format_certification_item(certification)
    section += r"  \resumeItemListEnd" + "\n"
    return section


def _build_achievements_section(data: Dict[str, Any]) -> str:
    """Build the achievements section of the resume.

    Args:
        data (dict): The resume data.

    Returns:
        str: The formatted achievements section.
        Returns an empty string if no achievements are available.
    """
    if "achievements" not in data or not data["achievements"]:
        return ""

    section = r"\resumeItemListStart" + "\n"
    for achievement in data["achievements"]:
        section += _format_achievement_item(achievement)
    section += r"  \resumeItemListEnd" + "\n"
    return section


def _apply_optimization_params(template_content: str, optimization_params: Dict[str, Any]) -> str:
    """Apply optimization parameters to the LaTeX template.

    Args:
        template_content (str): The original template content.
        optimization_params (dict): Parameters for optimization.

    Returns:
        str: The optimized template content.
    """
    # Apply font changes
    use_cormorant_font = optimization_params.get("use_cormorant_font", False)
    if use_cormorant_font:
        template_content = template_content.replace(
            "% \\usepackage{CormorantGaramond}",
            "\\usepackage{CormorantGaramond}",
        )

    # Apply font size changes
    font_size = optimization_params.get("font_size", "11pt")
    template_content = template_content.replace(
        r"\documentclass[letterpaper,11pt]{article}",
        f"\\documentclass[letterpaper,{font_size}]{{article}}",
    )

    # Apply margin adjustments
    margin_reduction = optimization_params.get("margin_reduction", 0)
    if margin_reduction > 0:
        # Reduce margins by the specified amount
        base_margin = 0.5
        new_margin = base_margin - margin_reduction
        template_content = template_content.replace(
            r"\addtolength{\oddsidemargin}{-0.5in}",
            f"\\addtolength{{\\oddsidemargin}}{{{-new_margin}in}}",
        )
        template_content = template_content.replace(
            r"\addtolength{\evensidemargin}{-0.5in}",
            f"\\addtolength{{\\evensidemargin}}{{{-new_margin}in}}",
        )
        template_content = template_content.replace(
            r"\addtolength{\topmargin}{-.5in}", f"\\addtolength{{\\topmargin}}{{{-new_margin}in}}"
        )

    # Apply spacing factor adjustments
    spacing_factor = optimization_params.get("spacing_factor", 1.0)
    if spacing_factor < 1.0:
        # Reduce various spacing elements
        # Section spacing
        template_content = template_content.replace(
            r"\vspace{-4pt}", f"\\vspace{{{int(-4 * spacing_factor)}pt}}"
        )
        template_content = template_content.replace(
            r"\vspace{-5pt}", f"\\vspace{{{int(-5 * spacing_factor)}pt}}"
        )
        template_content = template_content.replace(
            r"\vspace{-2pt}", f"\\vspace{{{int(-2 * spacing_factor)}pt}}"
        )
        template_content = template_content.replace(
            r"\vspace{-7pt}", f"\\vspace{{{int(-7 * spacing_factor)}pt}}"
        )

        # Add additional spacing reduction for very aggressive optimization
        if spacing_factor <= 0.7:
            # Add extra spacing reductions
            template_content = template_content.replace(r"\vspace{1pt}", "\\vspace{0pt}")

    return template_content


def render_template(
    data: Dict[str, Any], optimization_params: Optional[Dict[str, Any]] = None
) -> str:
    """Render a LaTeX template with the given data.

    Args:
        data (dict): Data to render the template with.
        optimization_params (dict, optional): Parameters for optimizing the template for one page.
            Expected keys: font_size, margin_reduction, spacing_factor, use_cormorant_font

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

    # Apply optimization parameters if provided
    if optimization_params:
        template_content = _apply_optimization_params(template_content, optimization_params)

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

    # Handle optional sections
    template_content = _handle_optional_sections(template_content, data)

    return template_content


def _handle_optional_sections(template_content: str, data: Dict[str, Any]) -> str:
    """Handle optional sections that may be empty and need to be removed.

    Args:
        template_content (str): The template content.
        data (dict): The resume data.

    Returns:
        str: The template content with optional sections handled.
    """
    # Handle publications section
    publications_content = _build_publications_section(data)
    template_content = _handle_section(
        template_content,
        publications_content,
        "{{publications}}",
        "%-----------Publications-----------",
        "%-------------------------------------------",
    )

    template_content = template_content.replace("{{skills}}", _build_skills_section(data))

    # Handle certifications section
    certifications_content = _build_certifications_section(data)
    template_content = _handle_section(
        template_content,
        certifications_content,
        "{{certifications}}",
        "%-----------Certifications-----------",
        "%-------------------------------------------",
    )

    # Handle achievements section
    achievements_content = _build_achievements_section(data)
    template_content = _handle_section(
        template_content,
        achievements_content,
        "{{achievements}}",
        "%-----------Achievements-----------",
        "%-------------------------------------------",
    )

    return template_content


def _handle_section(
    template_content: str,
    section_content: str,
    placeholder: str,
    section_start: str,
    section_end: str,
) -> str:
    """Handle a section that may be empty and need to be removed.

    Args:
        template_content (str): The template content.
        section_content (str): The content for the section.
        placeholder (str): The placeholder to replace.
        section_start (str): The start marker for the section.
        section_end (str): The end marker for the section.

    Returns:
        str: The template content with the section handled.
    """
    if not section_content:
        # Remove the section from the template
        start_pos = template_content.find(section_start)
        if start_pos != -1:
            end_pos = template_content.find(section_end, start_pos) + len(section_end)
            if end_pos != -1:
                template_content = template_content[:start_pos] + template_content[end_pos + 1 :]
    else:
        template_content = template_content.replace(placeholder, section_content)

    return template_content

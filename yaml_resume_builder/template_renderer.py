"""Template renderer module.

This module contains functionality for rendering LaTeX templates.
"""

from typing import Any, Dict


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


def render_template(template_path: str, data: Dict[str, Any]) -> str:
    """Render a LaTeX template with the given data.

    Args:
        template_path (str): Path to the LaTeX template (not used).
        data (dict): Data to render the template with.

    Returns:
        str: The rendered LaTeX content.
    """
    import os

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
        project_title = r"{\textbf{" + escape_latex(project["name"]) + r"}"
        if project["link"]:
            project_title += r" $|$ \emph{" + escape_latex(project["link"]) + r"}"
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

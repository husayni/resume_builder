"""Tests for the template_renderer module."""

import os
import tempfile

import pytest

from yaml_resume_builder.template_renderer import escape_latex, render_template


def test_escape_latex() -> None:
    """Test escaping LaTeX special characters."""
    # Test with special characters
    text = "This is a test with special characters: & % $ # _ { } ~ ^ \\"
    escaped = escape_latex(text)

    # Check that the function returns a string
    assert isinstance(escaped, str)

    # Check that special characters are escaped correctly
    assert r"\&" in escaped  # & -> \&
    assert r"\%" in escaped  # % -> \%
    assert r"\$" in escaped  # $ -> \$
    assert r"\#" in escaped  # # -> \#
    assert r"\_" in escaped  # _ -> \_
    assert r"\{" in escaped  # { -> \{
    assert r"\}" in escaped  # } -> \}
    assert r"\textasciitilde{}" in escaped  # ~ -> \textasciitilde{}
    assert r"\textasciicircum{}" in escaped  # ^ -> \textasciicircum{}

    # Check that backslash is properly escaped
    assert "textbackslash" in escaped
    # Just check that the original backslash is gone or properly escaped
    assert "\\" not in escaped or "\\textbackslash" in escaped

    # Test with non-string input
    assert escape_latex(123) == 123
    assert escape_latex(None) is None
    assert escape_latex([]) == []
    assert escape_latex({}) == {}


def test_render_template() -> None:
    """Test rendering a LaTeX template with data."""
    # Create a temporary template file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as temp_file:
        temp_file.write(r"""
\documentclass{article}
\begin{document}
\textbf{\Huge \scshape Jake Ryan}

123-456-7890 $|$ \href{mailto:x@x.com}{\underline{jake@su.edu}} $|$
\href{https://linkedin.com/in/...}{\underline{linkedin.com/in/jake}} $|$
\href{https://github.com/...}{\underline{github.com/jake}}

\section{Education}
  \resumeSubHeadingListStart
    \resumeSubheading
      {Southwestern University}{Georgetown, TX}
      {Bachelor of Arts in Computer Science, Minor in Business}{Aug. 2018 -- May 2021}
  \resumeSubHeadingListEnd
\end{document}
""")
        template_path = temp_file.name

    try:
        # Test data
        data = {
            "name": "Test User",
            "contact": {
                "phone": "555-123-4567",
                "email": "test@example.com",
                "linkedin": "testuser",
                "github": "testuser",
            },
            "education": [
                {
                    "school": "Test University",
                    "location": "Test City, TX",
                    "degree": "Bachelor of Science in Computer Science",
                    "dates": "2020 - 2024",
                }
            ],
            "experience": [],
            "projects": [],
            "skills": [],
        }

        # Render the template
        rendered = render_template(template_path, data)

        # Check that the rendered template is a string
        assert isinstance(rendered, str)

        # Check that the data is correctly inserted
        assert "Test User" in rendered
        assert "555-123-4567" in rendered
        assert "test@example.com" in rendered
        assert "testuser" in rendered
        assert "Test University" in rendered
        assert "Test City, TX" in rendered
        assert "Bachelor of Science in Computer Science" in rendered
        assert "2020 - 2024" in rendered
    finally:
        # Clean up the temporary file
        if os.path.exists(template_path):
            os.unlink(template_path)


def test_render_template_with_experience() -> None:
    """Test rendering a template with experience data."""
    # Create a temporary template file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as temp_file:
        temp_file.write(r"\documentclass{article}\begin{document}{{experience}}\end{document}")
        template_path = temp_file.name

    try:
        # Test data with experience
        data = {
            "name": "Test User",
            "contact": {
                "phone": "555-123-4567",
                "email": "test@example.com",
                "linkedin": "testuser",
                "github": "testuser",
            },
            "education": [],
            "experience": [
                {
                    "company": "Test Company",
                    "role": "Software Engineer",
                    "location": "Test City, CA",
                    "dates": "2020 - Present",
                    "bullets": [
                        "Developed feature X",
                        "Implemented system Y",
                        "Improved performance by Z%",
                    ],
                }
            ],
            "projects": [],
            "skills": [],
        }

        # Render the template
        rendered = render_template(template_path, data)

        # Check that the experience data is correctly inserted
        assert "Test Company" in rendered
        assert "Software Engineer" in rendered
        assert "Test City, CA" in rendered
        assert "2020 - Present" in rendered
        assert "Developed feature X" in rendered
        assert "Implemented system Y" in rendered

        # The % character is escaped in LaTeX, so we need to check for Z\%
        assert "Improved performance by Z\\%" in rendered
    finally:
        # Clean up the temporary file
        if os.path.exists(template_path):
            os.unlink(template_path)


def test_render_template_with_projects() -> None:
    """Test rendering a template with projects data."""
    # Create a temporary template file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as temp_file:
        temp_file.write(r"\documentclass{article}\begin{document}{{projects}}\end{document}")
        template_path = temp_file.name

    try:
        # Test data with projects
        data = {
            "name": "Test User",
            "contact": {
                "phone": "555-123-4567",
                "email": "test@example.com",
                "linkedin": "testuser",
                "github": "testuser",
            },
            "education": [],
            "experience": [],
            "projects": [
                {
                    "name": "Test Project",
                    "link": "https://github.com/testuser/test-project",
                    "bullets": [
                        "Built a web application",
                        "Used React and Node.js",
                        "Implemented CI/CD pipeline",
                    ],
                },
                {
                    "name": "Another Project",
                    "link": "",  # Test with empty link
                    "bullets": [
                        "Created a mobile app",
                        "Used Flutter",
                    ],
                },
            ],
            "skills": [],
        }

        # Render the template
        rendered = render_template(template_path, data)

        # Check that the projects data is correctly inserted
        assert "Test Project" in rendered
        assert "https://github.com/testuser/test-project" in rendered
        assert "Built a web application" in rendered
        assert "Used React and Node.js" in rendered
        assert "Implemented CI/CD pipeline" in rendered

        assert "Another Project" in rendered
        assert "Created a mobile app" in rendered
        assert "Used Flutter" in rendered
    finally:
        # Clean up the temporary file
        if os.path.exists(template_path):
            os.unlink(template_path)


def test_render_template_with_skills() -> None:
    """Test rendering a template with skills data."""
    # Create a temporary template file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as temp_file:
        temp_file.write(r"\documentclass{article}\begin{document}{{skills}}\end{document}")
        template_path = temp_file.name

    try:
        # Test data with skills
        data = {
            "name": "Test User",
            "contact": {
                "phone": "555-123-4567",
                "email": "test@example.com",
                "linkedin": "testuser",
                "github": "testuser",
            },
            "education": [],
            "experience": [],
            "projects": [],
            "skills": [
                {
                    "category": "Languages",
                    "list": ["Python", "JavaScript", "Java"],
                },
                {
                    "category": "Frameworks",
                    "list": ["React", "Django", "Spring"],
                },
            ],
        }

        # Render the template
        rendered = render_template(template_path, data)

        # Check that the skills data is correctly inserted
        assert "Languages" in rendered
        assert "Python, JavaScript, Java" in rendered
        assert "Frameworks" in rendered
        assert "React, Django, Spring" in rendered
    finally:
        # Clean up the temporary file
        if os.path.exists(template_path):
            os.unlink(template_path)


def test_render_template_with_missing_fields() -> None:
    """Test rendering a template with missing fields."""
    # Create a temporary template file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as temp_file:
        temp_file.write(r"\documentclass{article}\begin{document}{{name}}\end{document}")
        template_path = temp_file.name

    try:
        # Test data with missing fields
        data: dict = {}  # Empty data

        # Render the template should raise KeyError
        with pytest.raises(KeyError):
            render_template(template_path, data)
    finally:
        # Clean up the temporary file
        if os.path.exists(template_path):
            os.unlink(template_path)


def test_render_template_with_nonexistent_template() -> None:
    """Test rendering with a non-existent template."""
    # Test data
    data = {
        "name": "Test User",
        "contact": {
            "phone": "555-123-4567",
            "email": "test@example.com",
            "linkedin": "testuser",
            "github": "testuser",
        },
        "education": [],
        "experience": [],
        "projects": [],
        "skills": [],
    }

    # Render the template with a nonexistent path
    # This should still work because the function ignores the template_path
    # and uses the built-in simple_template.tex
    rendered = render_template("nonexistent_template.tex", data)

    # Check that the data is correctly inserted
    assert "Test User" in rendered
    assert "555-123-4567" in rendered
    assert "test@example.com" in rendered
    assert "testuser" in rendered

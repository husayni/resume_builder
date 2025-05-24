"""Tests for the template_renderer module."""

import pytest
from pytest import LogCaptureFixture

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

    # Test with non-string input (now converts to string)
    assert escape_latex(123) == "123"
    assert escape_latex(None) == "None"
    assert escape_latex([]) == "[]"
    assert escape_latex({}) == "{}"


def test_render_template() -> None:
    """Test rendering a LaTeX template with data."""
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
    rendered = render_template(data)

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


def test_render_template_with_experience() -> None:
    """Test rendering a template with experience data."""
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
    rendered = render_template(data)

    # Check that the experience data is correctly inserted
    assert "Test Company" in rendered
    assert "Software Engineer" in rendered
    assert "Test City, CA" in rendered
    assert "2020 - Present" in rendered
    assert "Developed feature X" in rendered
    assert "Implemented system Y" in rendered

    # The % character is escaped in LaTeX, so we need to check for Z\%
    assert "Improved performance by Z\\%" in rendered


def test_render_template_with_projects() -> None:
    """Test rendering a template with projects data."""
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
                "description": [
                    "Built a web application",
                    "Used React and Node.js",
                    "Implemented CI/CD pipeline",
                ],
            },
            {
                "name": "Another Project",
                "link": "",  # Test with empty link
                "description": [
                    "Created a mobile app",
                    "Used Flutter",
                ],
            },
        ],
        "skills": [],
    }

    # Render the template
    rendered = render_template(data)

    # Check that the projects data is correctly inserted
    assert "Test Project" in rendered
    assert "https://github.com/testuser/test-project" in rendered
    assert "Built a web application" in rendered
    assert "Used React and Node.js" in rendered
    assert "Implemented CI/CD pipeline" in rendered

    assert "Another Project" in rendered
    assert "Created a mobile app" in rendered
    assert "Used Flutter" in rendered


def test_render_template_with_projects_technologies_and_dates() -> None:
    """Test rendering a template with projects that have technologies and dates."""
    # Test data with projects including technologies and dates
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
                "name": "Gitlytics",
                "technologies": "Python, Flask, React, PostgreSQL, Docker",
                "date": "June 2020 - Present",
                "link": "https://github.com/testuser/gitlytics",
                "description": [
                    "Developed a full-stack web application",
                    "Implemented GitHub OAuth",
                    "Visualized GitHub data to show collaboration",
                ],
            },
            {
                "name": "Simple Paintball",
                "technologies": "Spigot API, Java, Maven, TravisCI, Git",
                "date": "May 2018 - May 2020",
                "link": "",
                "description": [
                    "Developed a Minecraft server plugin",
                    "Published plugin gaining 2K+ downloads",
                ],
            },
            {
                "name": "Legacy Project",  # Test with missing technologies and date
                "link": "https://example.com",
                "description": [
                    "Created a legacy project",
                ],
            },
        ],
        "skills": [],
    }

    # Render the template
    rendered = render_template(data)

    # Check that the projects data is correctly inserted
    assert "Gitlytics" in rendered
    assert "Python, Flask, React, PostgreSQL, Docker" in rendered
    assert "June 2020 - Present" in rendered
    assert "Developed a full-stack web application" in rendered

    assert "Simple Paintball" in rendered
    assert "Spigot API, Java, Maven, TravisCI, Git" in rendered
    assert "May 2018 - May 2020" in rendered
    assert "Developed a Minecraft server plugin" in rendered

    # Check that legacy project without technologies and date still works
    assert "Legacy Project" in rendered
    assert "https://example.com" in rendered
    assert "Created a legacy project" in rendered


def test_render_template_with_extra_fields(caplog: LogCaptureFixture) -> None:
    """Test rendering a template with extra fields in the YAML data."""
    import logging

    caplog.set_level(logging.WARNING)

    # Test data with extra fields at various levels
    data = {
        "name": "Test User",
        "title": "Software Engineer",  # Extra field at root level
        "contact": {
            "phone": "555-123-4567",
            "email": "test@example.com",
            "linkedin": "testuser",
            "github": "testuser",
            "website": "https://example.com",  # Extra field in contact
            "twitter": "@testuser",  # Extra field in contact
        },
        "education": [
            {
                "school": "Test University",
                "location": "Test City, TX",
                "degree": "Bachelor of Science in Computer Science",
                "dates": "2020 - 2024",
                "gpa": "3.9/4.0",  # Extra field in education
                "honors": ["Dean's List", "Scholarship"],  # Extra field in education
            }
        ],
        "experience": [
            {
                "company": "Test Company",
                "role": "Software Engineer",
                "location": "Test City, CA",
                "dates": "2020 - Present",
                "description": ["Developed feature X"],
                "manager": "John Doe",  # Extra field in experience
                "team_size": 5,  # Extra field in experience
            }
        ],
        "projects": [
            {
                "name": "Test Project",
                "technologies": "Python, Django",
                "date": "2023",
                "link": "https://github.com/testuser/test-project",
                "description": ["Built a web application"],
                "status": "Completed",  # Extra field in project
                "collaborators": ["Jane Doe"],  # Extra field in project
            }
        ],
        "skills": [
            {
                "category": "Languages",
                "list": ["Python", "JavaScript"],
                "proficiency": ["Expert", "Intermediate"],  # Extra field in skills
            }
        ],
        "certifications": [  # New section with simple strings
            "AWS Certified Developer - Associate (2023)",
        ],
    }

    # Render the template
    rendered = render_template(data)

    # Check that the template is rendered correctly with the known fields
    assert "Test User" in rendered

    # Check that warnings were logged for extra fields
    assert "Unknown field 'title' at root level" in caplog.text
    # Note: 'certifications' is now a known field, so no warning expected
    assert "Unknown field 'website' in contact section" in caplog.text
    assert "Unknown field 'twitter' in contact section" in caplog.text
    assert "Unknown field 'gpa' in education entry" in caplog.text
    assert "Unknown field 'honors' in education entry" in caplog.text
    assert "Unknown field 'manager' in experience entry" in caplog.text
    assert "Unknown field 'team_size' in experience entry" in caplog.text
    assert "Unknown field 'status' in project entry" in caplog.text
    assert "Unknown field 'collaborators' in project entry" in caplog.text
    assert "Unknown field 'proficiency' in skills entry" in caplog.text

    # Check that certifications are rendered correctly
    assert "AWS Certified Developer - Associate (2023)" in rendered


def test_render_template_with_skills() -> None:
    """Test rendering a template with skills data."""
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
    rendered = render_template(data)

    # Check that the skills data is correctly inserted
    assert "Languages" in rendered
    assert "Python, JavaScript, Java" in rendered
    assert "Frameworks" in rendered
    assert "React, Django, Spring" in rendered


def test_render_template_with_missing_fields() -> None:
    """Test rendering a template with missing fields."""
    # Test data with missing fields
    data: dict = {}  # Empty data

    # Render the template should raise KeyError
    with pytest.raises(KeyError):
        render_template(data)


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

    # Render the template
    # This should work because the function uses the built-in resume.tex.template
    rendered = render_template(data)

    # Check that the data is correctly inserted
    assert "Test User" in rendered
    assert "555-123-4567" in rendered
    assert "test@example.com" in rendered
    assert "testuser" in rendered

"""Minimal tests for the template_renderer module."""

import os
import tempfile

from yaml_resume_builder.template_renderer import render_template


def test_render_template_with_education() -> None:
    """Test rendering a template with education data."""
    # Create a temporary template file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as temp_file:
        temp_file.write(r"\documentclass{article}\begin{document}{{education}}\end{document}")
        template_path = temp_file.name

    try:
        # Test data with education
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

        # Check that the education data is correctly inserted
        assert "Test University" in rendered
        assert "Test City, TX" in rendered
        assert "Bachelor of Science in Computer Science" in rendered
        assert "2020 - 2024" in rendered
    finally:
        # Clean up the temporary file
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
        assert "Improved performance by Z\\%" in rendered  # % is escaped in LaTeX
    finally:
        # Clean up the temporary file
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
                }
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
    finally:
        # Clean up the temporary file
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
                }
            ],
        }

        # Render the template
        rendered = render_template(template_path, data)

        # Check that the skills data is correctly inserted
        assert "Languages" in rendered
        assert "Python" in rendered
        assert "JavaScript" in rendered
        assert "Java" in rendered
    finally:
        # Clean up the temporary file
        os.unlink(template_path)

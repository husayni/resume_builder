"""Tests for the publications and achievements functionality."""

from yaml_resume_builder.template_renderer import render_template


def test_render_template_with_publications_and_achievements() -> None:
    """Test rendering a template with publications and achievements data."""
    # Test data with publications and achievements
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
        "achievements": [
            {
                "title": "Best Paper Award",
                "issuer": "Conference on Testing",
                "date": "2023",
            },
            {
                "title": "Hackathon Winner",
                "issuer": "Tech Conference",
                "date": "2022",
            },
        ],
        "publications": [
            {
                "title": "A Groundbreaking Paper on Testing Methodologies",
                "journal": "Journal of Testing",
                "date": "January 2023",
            },
            {
                "title": "Advanced Testing Techniques in AI",
                "journal": "Conference on Testing",
                "date": "June 2022",
            },
        ],
    }

    # Render the template
    rendered = render_template(data)

    # Check that the achievements data is correctly inserted
    assert "Best Paper Award at Conference on Testing (2023)" in rendered
    assert "Hackathon Winner at Tech Conference (2022)" in rendered

    # Check that the publications data is correctly inserted
    assert (
        "``A Groundbreaking Paper on Testing Methodologies'' in Journal of Testing (January 2023)"
        in rendered
    )
    assert "``Advanced Testing Techniques in AI'' in Conference on Testing (June 2022)" in rendered


def test_render_template_with_empty_sections() -> None:
    """Test rendering a template with empty achievements and publications sections."""
    # Test data with empty achievements and publications
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
        "achievements": [],
        "publications": [],
    }

    # Render the template
    rendered = render_template(data)

    # Check that the template is rendered correctly
    assert "Test User" in rendered
    # The Achievements & Publications section should not be present
    assert "\\section{Achievements \\& Publications}" not in rendered
    # The section markers should not be present
    assert "%-----------Achievements / Publications / Certifications-----------" not in rendered
    assert "%-------------------------------------------" not in rendered


def test_render_template_with_special_characters() -> None:
    """Test rendering a template with special characters in achievements and publications."""
    # Test data with special characters
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
        "achievements": [
            {
                "title": "Award for 100% Test Coverage",
                "issuer": "Company & Partners",
                "date": "2023",
            },
        ],
        "publications": [
            {
                "title": "Testing with LaTeX: A_Guide",
                "journal": "Journal of LaTeX & Testing",
                "date": "2023",
            },
        ],
    }

    # Render the template
    rendered = render_template(data)

    # Check that special characters are properly escaped
    assert "Award for 100\\% Test Coverage at Company \\& Partners (2023)" in rendered
    assert "``Testing with LaTeX: A\\_Guide'' in Journal of LaTeX \\& Testing (2023)" in rendered


def test_render_template_with_only_achievements() -> None:
    """Test rendering a template with only achievements (no publications)."""
    # Test data with only achievements
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
        "achievements": [
            {
                "title": "Achievement Title",
                "issuer": "Organization",
                "date": "2023",
            },
        ],
        "publications": [],
    }

    # Render the template
    rendered = render_template(data)

    # Check that the achievements section is present
    assert "Achievements \\& Publications" in rendered
    assert "Achievement Title at Organization (2023)" in rendered
    assert "\\resumeItemListStart" in rendered
    assert "\\resumeItemListEnd" in rendered


def test_render_template_with_only_publications() -> None:
    """Test rendering a template with only publications (no achievements)."""
    # Test data with only publications
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
        "achievements": [],
        "publications": [
            {
                "title": "Publication Title",
                "journal": "Journal Name",
                "date": "2023",
            },
        ],
    }

    # Render the template
    rendered = render_template(data)

    # Check that the publications section is present
    assert "Achievements \\& Publications" in rendered
    assert "``Publication Title'' in Journal Name (2023)" in rendered
    assert "\\resumeItemListStart" in rendered
    assert "\\resumeItemListEnd" in rendered

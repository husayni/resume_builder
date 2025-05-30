"""Tests for the publications and achievements functionality."""

from yaml_resume_builder.template_renderer import render_template


def test_render_template_with_publications_and_achievements() -> None:
    """Test rendering a template with publications and achievements data."""
    # Test data with publications and achievements (new format)
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
            "Best Paper Award at Conference on Testing (2023)",
            "Hackathon Winner at Tech Conference (2022)",
        ],
        "publications": [
            "A Groundbreaking Paper on Testing Methodologies, Journal of Testing, January 2023",
            "Advanced Testing Techniques in AI, Conference on Testing, June 2022",
        ],
        "certifications": [
            "AWS Certified Developer - Associate (2023)",
        ],
    }

    # Render the template
    rendered = render_template(data)

    # Check that the achievements data is correctly inserted
    assert "Best Paper Award at Conference on Testing (2023)" in rendered
    assert "Hackathon Winner at Tech Conference (2022)" in rendered

    # Check that the publications data is correctly inserted
    assert (
        "A Groundbreaking Paper on Testing Methodologies, Journal of Testing, January 2023"
        in rendered
    )
    assert "Advanced Testing Techniques in AI, Conference on Testing, June 2022" in rendered

    # Check that the certifications data is correctly inserted
    assert "AWS Certified Developer - Associate (2023)" in rendered


def test_render_template_with_empty_sections() -> None:
    """Test rendering a template with empty achievements, publications, and certifications sections."""
    # Test data with empty achievements, publications, and certifications
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
        "certifications": [],
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
    # Test data with special characters (new format)
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
            "Award for 100% Test Coverage at Company & Partners (2023)",
        ],
        "publications": [
            "Testing with LaTeX: A_Guide, Journal of LaTeX & Testing, 2023",
        ],
        "certifications": [
            "Certified in Testing & Quality Assurance (2023)",
        ],
    }

    # Render the template
    rendered = render_template(data)

    # Check that special characters are properly escaped
    assert "Award for 100\\% Test Coverage at Company \\& Partners (2023)" in rendered
    assert "Testing with LaTeX: A\\_Guide, Journal of LaTeX \\& Testing, 2023" in rendered
    assert "Certified in Testing \\& Quality Assurance (2023)" in rendered


def test_render_template_with_only_achievements() -> None:
    """Test rendering a template with only achievements (no publications or certifications)."""
    # Test data with only achievements (new format)
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
            "Achievement Title at Organization (2023)",
        ],
        "publications": [],
        "certifications": [],
    }

    # Render the template
    rendered = render_template(data)

    # Check that the achievements section is present
    assert "\\section{Achievements}" in rendered
    assert "Achievement Title at Organization (2023)" in rendered
    assert "\\resumeItemListStart" in rendered
    assert "\\resumeItemListEnd" in rendered


def test_render_template_with_only_publications() -> None:
    """Test rendering a template with only publications (no achievements or certifications)."""
    # Test data with only publications (new format)
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
            "Publication Title, Journal Name, 2023",
        ],
        "certifications": [],
    }

    # Render the template
    rendered = render_template(data)

    # Check that the publications section is present
    assert "\\section{Publications}" in rendered
    assert "Publication Title, Journal Name, 2023" in rendered
    assert "\\resumeItemListStart" in rendered
    assert "\\resumeItemListEnd" in rendered


def test_render_template_with_only_certifications() -> None:
    """Test rendering a template with only certifications (no achievements or publications)."""
    # Test data with only certifications
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
        "certifications": [
            "AWS Certified Developer - Associate (2023)",
            "Google Cloud Certified - Associate Cloud Engineer (2022)",
        ],
    }

    # Render the template
    rendered = render_template(data)

    # Check that the certifications section is present
    assert "\\section{Certifications}" in rendered
    assert "AWS Certified Developer - Associate (2023)" in rendered
    assert "Google Cloud Certified - Associate Cloud Engineer (2022)" in rendered
    assert "\\resumeItemListStart" in rendered
    assert "\\resumeItemListEnd" in rendered


def test_render_template_with_certification_links() -> None:
    """Test rendering a template with certifications that have optional links."""
    # Test data with certifications in new dict format with links
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
        "certifications": [
            {
                "name": "AWS Certified Developer - Associate (2023)",
                "link": "https://www.credly.com/badges/your-badge-id",
            },
            {"name": "Google Cloud Certified - Associate Cloud Engineer (2022)"},
            "Traditional String Certification (2021)",
        ],
    }

    # Render the template
    rendered = render_template(data)

    # Check that the certifications section is present
    assert "\\section{Certifications}" in rendered

    # Check that certification with link is formatted with href
    assert (
        "\\href{https://www.credly.com/badges/your-badge-id}{\\underline{AWS Certified Developer - Associate (2023)}}"
        in rendered
    )

    # Check that certification without link is formatted normally
    assert "Google Cloud Certified - Associate Cloud Engineer (2022)" in rendered

    # Check that string certification is formatted normally
    assert "Traditional String Certification (2021)" in rendered

    assert "\\resumeItemListStart" in rendered
    assert "\\resumeItemListEnd" in rendered


def test_render_template_with_mixed_certification_formats() -> None:
    """Test rendering a template with mixed certification formats (string and dict)."""
    # Test data with mixed certification formats
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
        "certifications": [
            "AWS Certified Developer - Associate (2023)",
            {
                "name": "Microsoft Certified: Azure AI Engineer Associate",
                "link": "https://learn.microsoft.com/api/credentials/share/en-gb/SyedHussainAI/B02B98E733ECDA68?sharingId=B39A7C3D2A0738EB",
            },
            {"name": "Google Cloud Certified - Associate Cloud Engineer (2022)"},
        ],
    }

    # Render the template
    rendered = render_template(data)

    # Check that the certifications section is present
    assert "\\section{Certifications}" in rendered

    # Check string format
    assert "AWS Certified Developer - Associate (2023)" in rendered

    # Check dict format with link
    assert (
        "\\href{https://learn.microsoft.com/api/credentials/share/en-gb/SyedHussainAI/B02B98E733ECDA68?sharingId=B39A7C3D2A0738EB}{\\underline{Microsoft Certified: Azure AI Engineer Associate}}"
        in rendered
    )

    # Check dict format without link
    assert "Google Cloud Certified - Associate Cloud Engineer (2022)" in rendered

    assert "\\resumeItemListStart" in rendered
    assert "\\resumeItemListEnd" in rendered


def test_render_template_with_certification_special_characters() -> None:
    """Test rendering certifications with special LaTeX characters."""
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
        "certifications": [
            {
                "name": "AWS Certified & Professional Developer (2023)",
                "link": "https://example.com/cert?id=123&type=aws",
            },
            "Microsoft Certified: Azure AI Engineer & Data Scientist (2022)",
            {"name": "Google Cloud Professional - Machine Learning Engineer (100% Score)"},
        ],
    }

    rendered = render_template(data)

    # Check that special characters are properly escaped
    assert "\\section{Certifications}" in rendered
    assert "AWS Certified \\& Professional Developer (2023)" in rendered
    assert "Microsoft Certified: Azure AI Engineer \\& Data Scientist (2022)" in rendered
    assert "Google Cloud Professional - Machine Learning Engineer (100\\% Score)" in rendered
    assert "https://example.com/cert?id=123\\&type=aws" in rendered


def test_render_template_with_empty_certification_fields() -> None:
    """Test rendering certifications with empty or missing fields."""
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
        "certifications": [
            {"name": "Valid Certification", "link": "https://example.com/cert"},
            {"name": "Certification Without Link"},
            {"name": "", "link": "https://example.com/empty-name"},
            {"name": "Certification With Empty Link", "link": ""},
        ],
    }

    rendered = render_template(data)

    # Check that the certifications section is present
    assert "\\section{Certifications}" in rendered

    # Check valid certification with link
    assert "\\href{https://example.com/cert}{\\underline{Valid Certification}}" in rendered

    # Check certification without link
    assert "Certification Without Link" in rendered

    # Check certification with empty name (should still render)
    assert "\\href{https://example.com/empty-name}{\\underline{}}" in rendered

    # Check certification with empty link (should render without href)
    assert "Certification With Empty Link" in rendered


def test_render_template_with_invalid_certification_types() -> None:
    """Test rendering with invalid certification types (should handle gracefully)."""
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
        "certifications": [
            "Valid String Certification",
            {"name": "Valid Dict Certification"},
            123,  # Invalid type - number
            None,  # Invalid type - None
            [],  # Invalid type - list
        ],
    }

    rendered = render_template(data)

    # Check that the certifications section is present
    assert "\\section{Certifications}" in rendered

    # Check valid certifications
    assert "Valid String Certification" in rendered
    assert "Valid Dict Certification" in rendered

    # Check that invalid types are converted to strings (fallback behavior)
    assert "123" in rendered
    assert "None" in rendered


def test_render_template_with_certification_unknown_fields() -> None:
    """Test rendering certifications with unknown fields (should warn but still work)."""
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
        "certifications": [
            {
                "name": "AWS Certification",
                "link": "https://aws.com/cert",
                "unknown_field": "should be ignored",
                "another_unknown": 123,
            },
            {
                "name": "Google Certification",
                "issuer": "Google",  # Unknown field
                "date": "2023",  # Unknown field
            },
        ],
    }

    rendered = render_template(data)

    # Check that the certifications section is present and renders correctly
    assert "\\section{Certifications}" in rendered
    assert "\\href{https://aws.com/cert}{\\underline{AWS Certification}}" in rendered
    assert "Google Certification" in rendered


def test_render_template_with_only_certification_links() -> None:
    """Test rendering with only certifications that have links."""
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
        "certifications": [
            {
                "name": "AWS Certified Solutions Architect",
                "link": "https://www.credly.com/badges/aws-sa",
            },
            {
                "name": "Microsoft Azure Fundamentals",
                "link": "https://docs.microsoft.com/learn/certifications/azure-fundamentals",
            },
        ],
    }

    rendered = render_template(data)

    # Check that all certifications have links
    assert "\\section{Certifications}" in rendered
    assert (
        "\\href{https://www.credly.com/badges/aws-sa}{\\underline{AWS Certified Solutions Architect}}"
        in rendered
    )
    assert (
        "\\href{https://docs.microsoft.com/learn/certifications/azure-fundamentals}{\\underline{Microsoft Azure Fundamentals}}"
        in rendered
    )
    assert "\\resumeItemListStart" in rendered
    assert "\\resumeItemListEnd" in rendered


def test_render_template_with_long_certification_urls() -> None:
    """Test rendering with very long certification URLs."""
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
        "certifications": [
            {
                "name": "Very Long URL Certification",
                "link": "https://learn.microsoft.com/api/credentials/share/en-gb/SyedHussainAI/B02B98E733ECDA68?sharingId=B39A7C3D2A0738EB&utm_source=linkedin&utm_medium=social&utm_campaign=certification",
            }
        ],
    }

    rendered = render_template(data)

    # Check that long URLs are handled correctly
    assert "\\section{Certifications}" in rendered
    assert "Very Long URL Certification" in rendered
    assert "\\href{" in rendered
    assert "learn.microsoft.com" in rendered


def test_render_template_with_old_format_achievements_publications() -> None:
    """Test rendering a template with old format achievements and publications for backward compatibility."""
    # Test data with old format achievements and publications
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

    # Check that the old format achievements data is correctly converted
    assert "Best Paper Award at Conference on Testing (2023)" in rendered
    assert "Hackathon Winner at Tech Conference (2022)" in rendered

    # Check that the old format publications data is correctly converted
    assert (
        "``A Groundbreaking Paper on Testing Methodologies'' in Journal of Testing (January 2023)"
        in rendered
    )
    assert "``Advanced Testing Techniques in AI'' in Conference on Testing (June 2022)" in rendered

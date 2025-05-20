"""Minimal tests for the resume builder."""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest
import yaml

from yaml_resume_builder.builder import build_resume, compile_latex, load_yaml
from yaml_resume_builder.template_renderer import escape_latex, render_template


def test_load_yaml_minimal() -> None:
    """Test minimal YAML loading functionality."""
    # Create a temporary YAML file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as temp_file:
        temp_file.write("name: Test User\nage: 30")
        temp_path = temp_file.name

    try:
        # Test loading the YAML file
        data = load_yaml(temp_path)
        assert data == {"name": "Test User", "age": 30}
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)


def test_load_yaml_empty() -> None:
    """Test loading an empty YAML file."""
    # Create a temporary empty YAML file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as temp_file:
        temp_file.write("")
        temp_path = temp_file.name

    try:
        # Test loading the empty YAML file
        data = load_yaml(temp_path)
        assert data == {}
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)


def test_load_yaml_not_found() -> None:
    """Test loading YAML from a non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_yaml("non_existent_file.yml")


def test_load_yaml_invalid() -> None:
    """Test loading invalid YAML data."""
    # Create a temporary file with invalid YAML
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as temp_file:
        temp_file.write(
            "name: Test User\nage: 30\n  invalid_indent: :"
        )  # This is invalid YAML syntax
        temp_path = temp_file.name

    try:
        # Test loading the invalid YAML file
        with pytest.raises(yaml.YAMLError):
            load_yaml(temp_path)
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)


def test_escape_latex_minimal() -> None:
    """Test minimal LaTeX escaping functionality."""
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


def test_escape_latex_non_string() -> None:
    """Test escaping non-string values."""
    # Test with non-string input
    assert escape_latex(123) == 123
    assert escape_latex(None) is None
    assert escape_latex([]) == []
    assert escape_latex({}) == {}


@patch("subprocess.run")
def test_compile_latex_minimal(mock_run: MagicMock) -> None:
    """Test minimal LaTeX compilation functionality."""
    # Mock the subprocess.run function
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_run.return_value = mock_process

    # Test compiling a LaTeX file
    with tempfile.TemporaryDirectory() as temp_dir:
        tex_path = os.path.join(temp_dir, "test.tex")
        with open(tex_path, "w") as file:
            file.write("\\documentclass{article}\\begin{document}Test\\end{document}")

        pdf_path = compile_latex(tex_path, temp_dir)

        # Check that subprocess.run was called
        assert mock_run.call_count >= 1

        # Check that the returned PDF path is correct
        assert pdf_path == os.path.join(temp_dir, "test.pdf")


def test_render_template_minimal() -> None:
    """Test minimal template rendering functionality."""
    # Create a temporary template file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as temp_file:
        temp_file.write(r"\documentclass{article}\begin{document}{{name}}\end{document}")
        template_path = temp_file.name

    try:
        # Test data with all required fields
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
        rendered = render_template(template_path, data)

        # Check that the rendered template is a string
        assert isinstance(rendered, str)

        # Check that the data is correctly inserted
        assert "Test User" in rendered
        assert "555-123-4567" in rendered
        assert "test@example.com" in rendered
        assert "testuser" in rendered
    finally:
        # Clean up the temporary file
        os.unlink(template_path)


@patch("yaml_resume_builder.builder.compile_latex")
@patch("yaml_resume_builder.builder.render_template")
@patch("os.path.exists")
def test_build_resume_minimal(
    mock_exists: MagicMock, mock_render_template: MagicMock, mock_compile_latex: MagicMock
) -> None:
    """Test minimal resume building functionality."""
    # Mock the render_template function
    mock_render_template.return_value = (
        "\\documentclass{article}\\begin{document}Test\\end{document}"
    )

    # Mock the compile_latex function
    mock_compile_latex.return_value = "output.pdf"

    # Mock os.path.exists to return True for all paths
    mock_exists.return_value = True

    # Create temporary files for testing
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as yaml_file:
        yaml_file.write("""
name: Test User
contact:
  phone: 555-123-4567
  email: test@example.com
  linkedin: testuser
  github: testuser
education: []
experience: []
projects: []
skills: []
""")
        yaml_path = yaml_file.name

    try:
        # Test building the resume
        output_path = "output.pdf"
        result = build_resume(yaml_path, output_path)

        # Check that the functions were called
        mock_render_template.assert_called_once()
        mock_compile_latex.assert_called_once()

        # Check that the returned path is correct
        assert result == output_path
    finally:
        # Clean up the temporary file
        os.unlink(yaml_path)

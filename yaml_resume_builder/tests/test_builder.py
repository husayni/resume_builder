"""Tests for the builder module."""

import os
import subprocess
import tempfile
from unittest.mock import MagicMock, patch

import pytest
import yaml

from yaml_resume_builder.builder import build_resume, compile_latex, count_pdf_pages, load_yaml


def test_load_yaml() -> None:
    """Test loading YAML data from a file."""
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


def test_load_yaml_empty_file() -> None:
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


def test_load_yaml_file_not_found() -> None:
    """Test loading YAML from a non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_yaml("non_existent_file.yml")


def test_load_yaml_invalid_yaml() -> None:
    """Test loading invalid YAML data."""
    # Create a temporary file with invalid YAML
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as temp_file:
        temp_file.write(
            "name: Test User\nage: 30\n  invalid_indent: :"
        )  # This is invalid YAML syntax
        temp_path = temp_file.name

    try:
        # Test loading the invalid YAML file
        with pytest.raises(yaml.YAMLError):  # Specifically test for YAMLError
            load_yaml(temp_path)
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)


@patch("subprocess.run")
def test_compile_latex(mock_run: MagicMock) -> None:
    """Test compiling a LaTeX file to PDF."""
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

        # Check that subprocess.run was called with the correct arguments
        assert mock_run.call_count >= 1
        # Get the last call which should be the latexmk call
        args = mock_run.call_args_list[-1][0]
        assert args[0][0] == "latexmk"
        assert args[0][1] == "-pdf"
        assert args[0][3] == f"-output-directory={temp_dir}"
        assert args[0][4] == tex_path

        # Check that the returned PDF path is correct
        assert pdf_path == os.path.join(temp_dir, "test.pdf")


@patch("subprocess.run")
def test_compile_latex_latexmk_not_found(mock_run: MagicMock) -> None:
    """Test compiling a LaTeX file when latexmk is not installed."""
    # Mock the subprocess.run function to raise CalledProcessError
    mock_run.side_effect = subprocess.CalledProcessError(1, "which latexmk")

    # Test compiling a LaTeX file
    with tempfile.TemporaryDirectory() as temp_dir:
        tex_path = os.path.join(temp_dir, "test.tex")
        with open(tex_path, "w") as file:
            file.write("\\documentclass{article}\\begin{document}Test\\end{document}")

        with pytest.raises(FileNotFoundError) as excinfo:
            compile_latex(tex_path, temp_dir)

        # Check that the error message contains installation instructions
        assert "LaTeX/latexmk not found" in str(excinfo.value)


@patch("subprocess.run")
@patch("os.name", "nt")  # Mock Windows environment
def test_compile_latex_windows(mock_run: MagicMock) -> None:
    """Test compiling a LaTeX file on Windows."""
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

        # Check that subprocess.run was called with the correct arguments for Windows
        assert mock_run.call_count >= 1
        # First call should be to check if latexmk exists using 'where'
        args = mock_run.call_args_list[0][0]
        assert args[0][0] == "where"
        assert args[0][1] == "latexmk"

        # Also verify that the PDF path is returned correctly
        assert pdf_path.endswith("test.pdf")


@patch("subprocess.run")
def test_compile_latex_compilation_error(mock_run: MagicMock) -> None:
    """Test handling LaTeX compilation errors."""
    # First call succeeds (checking for latexmk)
    mock_success = MagicMock()
    mock_success.returncode = 0

    # Second call fails (latexmk compilation)
    mock_error = subprocess.CalledProcessError(1, "latexmk")
    mock_error.stdout = b"LaTeX Error: File not found"
    mock_error.stderr = b"Error message"

    mock_run.side_effect = [mock_success, mock_error]

    # Test compiling a LaTeX file
    with tempfile.TemporaryDirectory() as temp_dir:
        tex_path = os.path.join(temp_dir, "test.tex")
        with open(tex_path, "w") as file:
            file.write("\\documentclass{article}\\begin{document}Test\\end{document}")

        with pytest.raises(subprocess.CalledProcessError):
            compile_latex(tex_path, temp_dir)


@patch("yaml_resume_builder.builder.compile_latex")
@patch("yaml_resume_builder.builder.render_template")
def test_build_resume(mock_render_template: MagicMock, mock_compile_latex: MagicMock) -> None:
    """Test building a resume from a YAML file."""
    # Mock the render_template function
    mock_render_template.return_value = (
        "\\documentclass{article}\\begin{document}Test\\end{document}"
    )

    # Mock the compile_latex function
    mock_compile_latex.return_value = os.path.join("output_dir", "resume.pdf")

    # Create temporary files for testing
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as yaml_file:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".pdf", delete=False) as output_file:
            # Write test data to the YAML file
            yaml_file.write("name: Test User\nage: 30")
            yaml_path = yaml_file.name

            # Get the output path
            output_path = output_file.name

    try:
        # Test building the resume
        result = build_resume(yaml_path, output_path)

        # Check that the functions were called with the correct arguments
        mock_render_template.assert_called_once()
        mock_compile_latex.assert_called_once()

        # Check that the returned path is correct
        assert result == output_path
    finally:
        # Clean up the temporary files
        for path in [yaml_path, output_path]:
            if os.path.exists(path):
                os.unlink(path)


@patch("yaml_resume_builder.builder.compile_latex")
@patch("yaml_resume_builder.builder.render_template")
@patch("os.path.exists")
def test_build_resume_pdf_not_exists(
    mock_exists: MagicMock, mock_render_template: MagicMock, mock_compile_latex: MagicMock
) -> None:
    """Test building a resume when the PDF doesn't exist (mock case)."""
    # Mock the render_template function
    mock_render_template.return_value = (
        "\\documentclass{article}\\begin{document}Test\\end{document}"
    )

    # Mock the compile_latex function
    mock_compile_latex.return_value = os.path.join(tempfile.gettempdir(), "nonexistent.pdf")

    # Mock os.path.exists to return True for input file and False for PDF
    mock_exists.side_effect = lambda path: not path.endswith(".pdf")

    # Create temporary files for testing
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as yaml_file:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".pdf", delete=False) as output_file:
            yaml_file.write("name: Test User\nage: 30")
            yaml_path = yaml_file.name
            output_path = output_file.name

    try:
        # Test building the resume
        result = build_resume(yaml_path, output_path)

        # Check that the returned path is correct
        assert result == output_path

        # Check that a mock PDF was created
        with open(output_path, "r") as f:
            content = f.read()
            assert content == "Mock PDF content"
    finally:
        # Clean up the temporary files
        for path in [yaml_path, output_path]:
            if os.path.exists(path):
                os.unlink(path)


@patch("yaml_resume_builder.builder.compile_latex")
@patch("yaml_resume_builder.builder.render_template")
def test_build_resume_with_real_pdf(
    mock_render_template: MagicMock,
    mock_compile_latex: MagicMock,
) -> None:
    """Test building a resume with a real PDF (mocked).

    This test is simplified to avoid issues with file operations.
    """
    # Mock the render_template function
    mock_render_template.return_value = (
        "\\documentclass{article}\\begin{document}Test\\end{document}"
    )

    # Mock the compile_latex function to return a PDF path
    pdf_path = os.path.join(tempfile.gettempdir(), "real.pdf")
    mock_compile_latex.return_value = pdf_path

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
        output_path = os.path.join(tempfile.gettempdir(), "output.pdf")

    try:
        # Create a mock PDF file that will be "copied" by the build_resume function
        with open(pdf_path, "w") as f:
            f.write("Mock PDF content")

        # Test building the resume
        result = build_resume(yaml_path, output_path)

        # Check that the returned path is correct
        assert result == output_path

        # Verify that the output file was created
        assert os.path.exists(output_path)

        # Clean up the mock PDF
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)

        # Clean up the output PDF
        if os.path.exists(output_path):
            os.unlink(output_path)
    finally:
        # Clean up the temporary file
        if os.path.exists(yaml_path):
            os.unlink(yaml_path)


@patch("yaml_resume_builder.builder.compile_latex")
@patch("yaml_resume_builder.builder.render_template")
def test_build_resume_create_output_dir(
    mock_render_template: MagicMock, mock_compile_latex: MagicMock
) -> None:
    """Test that build_resume creates the output directory if it doesn't exist."""
    # Mock the render_template function
    mock_render_template.return_value = (
        "\\documentclass{article}\\begin{document}Test\\end{document}"
    )

    # Mock the compile_latex function to return a PDF path
    pdf_path = os.path.join(tempfile.gettempdir(), "test.pdf")
    mock_compile_latex.return_value = pdf_path

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
        # Create a temporary directory for output
        temp_dir = tempfile.mkdtemp()
        # Create a non-existent subdirectory
        output_dir = os.path.join(temp_dir, "subdir")
        output_path = os.path.join(output_dir, "resume.pdf")

        # Create a mock PDF file
        with open(pdf_path, "w") as f:
            f.write("Mock PDF content")

        # Call build_resume
        result = build_resume(yaml_path, output_path)

        # Check that the output directory was created
        assert os.path.exists(output_dir)
        # Check that the output file was created
        assert os.path.exists(output_path)
        # Check that the returned path is correct
        assert result == output_path

        # Clean up the mock PDF
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)
    finally:
        # Clean up the temporary file
        if os.path.exists(yaml_path):
            os.unlink(yaml_path)
        # Clean up the temporary directory
        if os.path.exists(temp_dir):
            import shutil

            shutil.rmtree(temp_dir)


@patch("yaml_resume_builder.builder.compile_latex")
@patch("yaml_resume_builder.builder.render_template")
def test_build_resume_with_debug(
    mock_render_template: MagicMock, mock_compile_latex: MagicMock
) -> None:
    """Test building a resume with debug mode enabled."""
    # Mock the render_template function
    mock_render_template.return_value = (
        "\\documentclass{article}\\begin{document}Test\\end{document}"
    )

    # Mock the compile_latex function
    mock_compile_latex.return_value = os.path.join("output_dir", "resume.pdf")

    # Create temporary files for testing
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as yaml_file:
        # Write test data to the YAML file
        yaml_file.write("name: Test User\nage: 30")
        yaml_path = yaml_file.name

        # Define output paths
        output_path = os.path.join(tempfile.gettempdir(), "test_debug.pdf")
        tex_output_path = output_path.replace(".pdf", ".tex")

    try:
        # Test building the resume with debug=True
        result = build_resume(yaml_path, output_path, debug=True)

        # Check that the functions were called with the correct arguments
        mock_render_template.assert_called_once()
        mock_compile_latex.assert_called_once()

        # Check that the returned path is correct
        assert result == output_path

        # Check that the .tex file was created
        assert os.path.exists(tex_output_path)

        # Check that the .tex file contains the expected content
        with open(tex_output_path, "r") as f:
            tex_content = f.read()
            assert "\\documentclass{article}" in tex_content
            assert "Test" in tex_content

        # Clean up the .tex file
        if os.path.exists(tex_output_path):
            os.unlink(tex_output_path)
    finally:
        # Clean up the temporary files
        for path in [yaml_path, output_path]:
            if os.path.exists(path):
                os.unlink(path)


def test_build_resume_input_not_found() -> None:
    """Test building a resume with a non-existent input file."""
    with pytest.raises(FileNotFoundError):
        build_resume("non_existent_file.yml", "output.pdf")


def test_count_pdf_pages() -> None:
    """Test counting pages in a PDF file."""
    # Create a mock PDF file with known content
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as pdf_file:
        # Create a minimal PDF content (this is a very basic PDF structure)
        pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
>>
endobj
xref
0 4
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
trailer
<<
/Size 4
/Root 1 0 R
>>
startxref
190
%%EOF"""
        pdf_file.write(pdf_content)
        pdf_path = pdf_file.name

    try:
        # Test counting pages
        page_count = count_pdf_pages(pdf_path)
        assert page_count == 1
    finally:
        # Clean up
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)


def test_count_pdf_pages_file_not_found() -> None:
    """Test counting pages in a non-existent PDF file."""
    with pytest.raises(FileNotFoundError):
        count_pdf_pages("non_existent_file.pdf")


@patch("yaml_resume_builder.builder.count_pdf_pages")
@patch("yaml_resume_builder.builder.compile_latex")
@patch("yaml_resume_builder.builder.render_template")
def test_build_resume_one_page_optimization(
    mock_render_template: MagicMock,
    mock_compile_latex: MagicMock,
    mock_count_pdf_pages: MagicMock,
) -> None:
    """Test building a resume with one-page optimization that succeeds on first try."""
    # Mock the render_template function
    mock_render_template.return_value = (
        "\\documentclass{article}\\begin{document}Test\\end{document}"
    )

    # Mock the compile_latex function
    pdf_path = os.path.join(tempfile.gettempdir(), "test.pdf")
    mock_compile_latex.return_value = pdf_path

    # Mock count_pdf_pages to return 1 (one page)
    mock_count_pdf_pages.return_value = 1

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
        output_path = os.path.join(tempfile.gettempdir(), "output.pdf")

    try:
        # Create a mock PDF file
        with open(pdf_path, "w") as f:
            f.write("Mock PDF content")

        # Test building the resume with one-page optimization
        result = build_resume(yaml_path, output_path, one_page=True)

        # Check that the returned path is correct
        assert result == output_path

        # Verify that render_template was called with optimization parameters
        mock_render_template.assert_called_once()
        _, kwargs = mock_render_template.call_args
        assert "optimization_params" in kwargs
        assert kwargs["optimization_params"]["font_size"] == "11pt"
        assert kwargs["optimization_params"]["use_cormorant_font"] is False

        # Verify that count_pdf_pages was called
        mock_count_pdf_pages.assert_called_once_with(pdf_path)

        # Clean up the mock PDF
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)
        if os.path.exists(output_path):
            os.unlink(output_path)
    finally:
        # Clean up the temporary file
        if os.path.exists(yaml_path):
            os.unlink(yaml_path)


@patch("yaml_resume_builder.builder.count_pdf_pages")
@patch("yaml_resume_builder.builder.compile_latex")
@patch("yaml_resume_builder.builder.render_template")
def test_build_resume_one_page_optimization_fallback(
    mock_render_template: MagicMock,
    mock_compile_latex: MagicMock,
    mock_count_pdf_pages: MagicMock,
) -> None:
    """Test building a resume with one-page optimization that falls back to regular build."""
    # Mock the render_template function
    mock_render_template.return_value = (
        "\\documentclass{article}\\begin{document}Test\\end{document}"
    )

    # Mock the compile_latex function
    pdf_path = os.path.join(tempfile.gettempdir(), "test.pdf")
    mock_compile_latex.return_value = pdf_path

    # Mock count_pdf_pages to always return 2 (more than one page)
    mock_count_pdf_pages.return_value = 2

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
        output_path = os.path.join(tempfile.gettempdir(), "output.pdf")

    try:
        # Create a mock PDF file
        with open(pdf_path, "w") as f:
            f.write("Mock PDF content")

        # Test building the resume with one-page optimization
        result = build_resume(yaml_path, output_path, one_page=True)

        # Check that the returned path is correct
        assert result == output_path

        # Verify that render_template was called multiple times (for different optimization levels)
        assert mock_render_template.call_count >= 5  # Should try all optimization levels

        # Clean up the mock PDF
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)
        if os.path.exists(output_path):
            os.unlink(output_path)
    finally:
        # Clean up the temporary file
        if os.path.exists(yaml_path):
            os.unlink(yaml_path)


@patch("yaml_resume_builder.builder.count_pdf_pages")
@patch("yaml_resume_builder.builder.compile_latex")
@patch("yaml_resume_builder.builder.render_template")
def test_build_resume_one_page_optimization_levels(
    mock_render_template: MagicMock,
    mock_compile_latex: MagicMock,
    mock_count_pdf_pages: MagicMock,
) -> None:
    """Test that optimization levels include the correct font parameters."""
    # Mock the render_template function
    mock_render_template.return_value = (
        "\\documentclass{article}\\begin{document}Test\\end{document}"
    )

    # Mock the compile_latex function
    pdf_path = os.path.join(tempfile.gettempdir(), "test.pdf")
    mock_compile_latex.return_value = pdf_path

    # Mock count_pdf_pages to return 2 for first call, then 1 for second call
    mock_count_pdf_pages.side_effect = [2, 1]  # First level fails, second level succeeds

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
        output_path = os.path.join(tempfile.gettempdir(), "output.pdf")

    try:
        # Create a mock PDF file
        with open(pdf_path, "w") as f:
            f.write("Mock PDF content")

        # Test building the resume with one-page optimization
        result = build_resume(yaml_path, output_path, one_page=True)

        # Check that the returned path is correct
        assert result == output_path

        # Verify that render_template was called twice (level 1 and level 2)
        assert mock_render_template.call_count == 2

        # Check first call (level 1) - should not have font change
        first_call_kwargs = mock_render_template.call_args_list[0][1]
        assert "optimization_params" in first_call_kwargs
        assert first_call_kwargs["optimization_params"]["use_cormorant_font"] is False

        # Check second call (level 2) - should have font change
        second_call_kwargs = mock_render_template.call_args_list[1][1]
        assert "optimization_params" in second_call_kwargs
        assert second_call_kwargs["optimization_params"]["use_cormorant_font"] is True

        # Clean up the mock PDF
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)
        if os.path.exists(output_path):
            os.unlink(output_path)
    finally:
        # Clean up the temporary file
        if os.path.exists(yaml_path):
            os.unlink(yaml_path)


def test_build_resume_one_page_disabled() -> None:
    """Test that build_resume works normally when one_page=False."""
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
        output_path = os.path.join(tempfile.gettempdir(), "output.pdf")

    try:
        with patch("yaml_resume_builder.builder.render_template") as mock_render_template:
            with patch("yaml_resume_builder.builder.compile_latex") as mock_compile_latex:
                mock_render_template.return_value = (
                    "\\documentclass{article}\\begin{document}Test\\end{document}"
                )
                mock_compile_latex.return_value = output_path

                # Test building the resume with one_page=False
                result = build_resume(yaml_path, output_path, one_page=False)

                # Verify that render_template was called without optimization_params
                mock_render_template.assert_called_once()
                _, kwargs = mock_render_template.call_args
                assert (
                    "optimization_params" not in kwargs or kwargs.get("optimization_params") is None
                )
                assert result == output_path
    finally:
        # Clean up the temporary file
        if os.path.exists(yaml_path):
            os.unlink(yaml_path)

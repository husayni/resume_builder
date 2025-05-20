"""Minimal tests for the builder module."""

import os
import subprocess
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from yaml_resume_builder.builder import build_resume, compile_latex


@patch("subprocess.run")
def test_compile_latex_windows(mock_run: MagicMock) -> None:
    """Test compiling a LaTeX file on Windows."""
    # Mock os.name to be 'nt' (Windows)
    with patch("os.name", "nt"):
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
@patch("os.path.exists")
@patch("builtins.open")
def test_build_resume_with_real_pdf(
    mock_open: MagicMock,
    mock_exists: MagicMock,
    mock_render_template: MagicMock,
    mock_compile_latex: MagicMock,
) -> None:
    """Test building a resume with a real PDF (mocked)."""
    # Mock the render_template function
    mock_render_template.return_value = (
        "\\documentclass{article}\\begin{document}Test\\end{document}"
    )

    # Mock the compile_latex function to return a PDF path
    pdf_path = os.path.join(tempfile.gettempdir(), "real.pdf")
    mock_compile_latex.return_value = pdf_path

    # Mock os.path.exists to return True for all paths
    mock_exists.return_value = True

    # Set up mock file handles for reading and writing
    mock_src = MagicMock()
    mock_dst = MagicMock()
    mock_src.__enter__.return_value.read.return_value = b"PDF content"

    # Configure the open mock to return different file handles
    def side_effect(path: str, mode: str = "r") -> MagicMock:
        return mock_src if path == pdf_path and mode == "rb" else mock_dst

    mock_open.side_effect = side_effect

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
        # Test building the resume
        result = build_resume(yaml_path, output_path)

        # Check that the returned path is correct
        assert result == output_path

        # Verify that the PDF content was copied
        mock_dst.__enter__.return_value.write.assert_called_once_with(b"PDF content")
    finally:
        # Clean up the temporary file
        os.unlink(yaml_path)


@patch("yaml_resume_builder.builder.compile_latex")
@patch("yaml_resume_builder.builder.render_template")
@patch("os.path.exists")
@patch("os.makedirs")
def test_build_resume_create_output_dir(
    mock_makedirs: MagicMock,
    mock_exists: MagicMock,
    mock_render_template: MagicMock,
    mock_compile_latex: MagicMock,
) -> None:
    """Test creating output directory if it doesn't exist."""
    # Mock the render_template function
    mock_render_template.return_value = (
        "\\documentclass{article}\\begin{document}Test\\end{document}"
    )

    # Mock the compile_latex function
    mock_compile_latex.return_value = os.path.join(tempfile.gettempdir(), "resume.pdf")

    # Mock os.path.exists to return True for input file and PDF, but False for output dir
    mock_exists.side_effect = lambda path: "nonexistent_dir" not in path

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
        # Use a nested output path that doesn't exist
        output_path = os.path.join(tempfile.gettempdir(), "nonexistent_dir", "resume.pdf")

        # Test building the resume
        result = build_resume(yaml_path, output_path)

        # Check that os.makedirs was called with the correct directory
        mock_makedirs.assert_called_once_with(os.path.dirname(output_path))

        # Check that the returned path is correct
        assert result == output_path
    finally:
        # Clean up the temporary file
        os.unlink(yaml_path)

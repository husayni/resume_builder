"""Minimal tests for the CLI module."""

import os
import tempfile
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from yaml_resume_builder.cli import cli


@patch("yaml_resume_builder.cli.build_resume")
def test_build_command_minimal(mock_build_resume: MagicMock) -> None:
    """Test the build command with minimal arguments."""
    # Mock the build_resume function
    mock_build_resume.return_value = "output.pdf"

    # Create temporary files for testing
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as yaml_file:
        yaml_file.write("name: Test User\nage: 30")
        yaml_path = yaml_file.name

    try:
        # Create a CLI runner
        runner = CliRunner()

        # Run the build command
        result = runner.invoke(
            cli,
            ["build", "--input", yaml_path, "--output", "output.pdf"],
        )

        # Check that the command succeeded
        assert result.exit_code == 0

        # Check that the build_resume function was called with the correct arguments
        mock_build_resume.assert_called_once_with(yaml_path, "output.pdf", None)

        # Check that the success message is in the output
        assert "Resume successfully built and saved to: output.pdf" in result.output
    finally:
        # Clean up the temporary file
        os.unlink(yaml_path)


@patch("yaml_resume_builder.cli.build_resume")
def test_build_command_with_template(mock_build_resume: MagicMock) -> None:
    """Test the build command with a template argument."""
    # Mock the build_resume function
    mock_build_resume.return_value = "output.pdf"

    # Create temporary files for testing
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as yaml_file:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as template_file:
            yaml_file.write("name: Test User\nage: 30")
            template_file.write(r"\documentclass{article}\begin{document}{{name}}\end{document}")
            yaml_path = yaml_file.name
            template_path = template_file.name

    try:
        # Create a CLI runner
        runner = CliRunner()

        # Run the build command with template
        result = runner.invoke(
            cli,
            ["build", "--input", yaml_path, "--output", "output.pdf", "--template", template_path],
        )

        # Check that the command succeeded
        assert result.exit_code == 0

        # Check that the build_resume function was called with the correct arguments
        mock_build_resume.assert_called_once_with(yaml_path, "output.pdf", template_path)

        # Check that the success message is in the output
        assert "Resume successfully built and saved to: output.pdf" in result.output
    finally:
        # Clean up the temporary files
        os.unlink(yaml_path)
        os.unlink(template_path)


@patch("yaml_resume_builder.cli.build_resume")
def test_build_command_error(mock_build_resume: MagicMock) -> None:
    """Test the build command with an error."""
    # Mock the build_resume function to raise an exception
    mock_build_resume.side_effect = Exception("Test error")

    # Create a temporary YAML file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as yaml_file:
        yaml_file.write("name: Test User\nage: 30")
        yaml_path = yaml_file.name

    try:
        # Create a CLI runner
        runner = CliRunner()

        # Run the build command
        result = runner.invoke(
            cli,
            ["build", "--input", yaml_path, "--output", "output.pdf"],
        )

        # Check that the command failed
        assert result.exit_code == 1

        # Check that the error message is in the output
        assert "Error building resume: Test error" in result.output
    finally:
        # Clean up the temporary file
        os.unlink(yaml_path)


@patch("yaml_resume_builder.cli.shutil.copy")
@patch("yaml_resume_builder.cli.os.path.dirname")
def test_init_command_minimal(mock_dirname: MagicMock, mock_copy: MagicMock) -> None:
    """Test the init command with minimal arguments."""
    # Mock the dirname function to return a fixed path
    mock_dirname.return_value = "/fake/path"

    # Create a CLI runner
    runner = CliRunner()

    # Run the init command
    result = runner.invoke(cli, ["init"])

    # Check that the command succeeded
    assert result.exit_code == 0

    # Check that the copy function was called with the correct arguments
    mock_copy.assert_called_once_with("/fake/path/sample_resume.yml", "sample_resume.yml")

    # Check that the success message is in the output
    assert "Sample resume file created at: sample_resume.yml" in result.output


@patch("yaml_resume_builder.cli.shutil.copy")
@patch("yaml_resume_builder.cli.os.path.dirname")
def test_init_command_with_output(mock_dirname: MagicMock, mock_copy: MagicMock) -> None:
    """Test the init command with an output argument."""
    # Mock the dirname function to return a fixed path
    mock_dirname.return_value = "/fake/path"

    # Create a CLI runner
    runner = CliRunner()

    # Run the init command with output
    result = runner.invoke(cli, ["init", "--output", "custom_resume.yml"])

    # Check that the command succeeded
    assert result.exit_code == 0

    # Check that the copy function was called with the correct arguments
    mock_copy.assert_called_once_with("/fake/path/sample_resume.yml", "custom_resume.yml")

    # Check that the success message is in the output
    assert "Sample resume file created at: custom_resume.yml" in result.output

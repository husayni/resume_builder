"""Tests for the CLI module."""

import os
import tempfile
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from yaml_resume_builder.cli import cli, main


@patch("yaml_resume_builder.cli.build_resume")
def test_build_command(mock_build_resume: MagicMock) -> None:
    """Test the build command."""
    # Mock the build_resume function
    mock_build_resume.return_value = "output.pdf"

    # Create temporary files for testing
    # Using nested context managers for Python 3.8 compatibility
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as yaml_file:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as template_file:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".pdf", delete=False) as output_file:
                # Write test data to the files
                yaml_file.write("name: Test User\nage: 30")
                template_file.write(
                    "\\documentclass{article}\\begin{document}{{name}}\\end{document}"
                )

                # Get the file paths
                yaml_path = yaml_file.name
                template_path = template_file.name
                output_path = output_file.name

    try:
        # Create a CLI runner
        runner = CliRunner()

        # Run the build command
        result = runner.invoke(
            cli,
            ["build", "--input", yaml_path, "--output", output_path, "--template", template_path],
        )

        # Check that the command succeeded
        assert result.exit_code == 0

        # Check that the build_resume function was called with the correct arguments
        mock_build_resume.assert_called_once_with(yaml_path, output_path, template_path)

        # Check that the success message is in the output
        assert "Resume successfully built and saved to: output.pdf" in result.output
    finally:
        # Clean up the temporary files
        for path in [yaml_path, template_path, output_path]:
            if os.path.exists(path):
                os.unlink(path)


@patch("yaml_resume_builder.cli.build_resume")
def test_build_command_without_template(mock_build_resume: MagicMock) -> None:
    """Test the build command without specifying a template."""
    # Mock the build_resume function
    mock_build_resume.return_value = "output.pdf"

    # Create temporary files for testing
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as yaml_file:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".pdf", delete=False) as output_file:
            yaml_file.write("name: Test User\nage: 30")
            yaml_path = yaml_file.name
            output_path = output_file.name

    try:
        # Create a CLI runner
        runner = CliRunner()

        # Run the build command without template
        result = runner.invoke(
            cli,
            ["build", "--input", yaml_path, "--output", output_path],
        )

        # Check that the command succeeded
        assert result.exit_code == 0

        # Check that the build_resume function was called with the correct arguments
        mock_build_resume.assert_called_once_with(yaml_path, output_path, None)

        # Check that the success message is in the output
        assert "Resume successfully built and saved to: output.pdf" in result.output
    finally:
        # Clean up the temporary files
        for path in [yaml_path, output_path]:
            if os.path.exists(path):
                os.unlink(path)


@patch("yaml_resume_builder.cli.build_resume")
def test_build_command_error(mock_build_resume: MagicMock) -> None:
    """Test the build command with an error."""
    # Mock the build_resume function to raise an exception
    mock_build_resume.side_effect = Exception("Test error")

    # Create temporary files for testing
    # Using nested context managers for Python 3.8 compatibility
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as yaml_file:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as template_file:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".pdf", delete=False) as output_file:
                # Write test data to the files
                yaml_file.write("name: Test User\nage: 30")
                template_file.write(
                    "\\documentclass{article}\\begin{document}{{name}}\\end{document}"
                )

                # Get the file paths
                yaml_path = yaml_file.name
                template_path = template_file.name
                output_path = output_file.name

    try:
        # Create a CLI runner
        runner = CliRunner()

        # Run the build command
        result = runner.invoke(
            cli,
            ["build", "--input", yaml_path, "--output", output_path, "--template", template_path],
        )

        # Check that the command failed
        assert result.exit_code == 1

        # Check that the error message is in the output
        assert "Error building resume: Test error" in result.output
    finally:
        # Clean up the temporary files
        for path in [yaml_path, template_path, output_path]:
            if os.path.exists(path):
                os.unlink(path)


def test_build_command_invalid_input() -> None:
    """Test the build command with invalid input arguments."""
    # Create a CLI runner
    runner = CliRunner()

    # Run the build command without required arguments
    result = runner.invoke(cli, ["build"])

    # Check that the command failed
    assert result.exit_code != 0

    # Check that the error message mentions the missing options
    assert "Missing option" in result.output
    assert "--input" in result.output or "-i" in result.output


@patch("yaml_resume_builder.cli.shutil.copy")
@patch("yaml_resume_builder.cli.os.path.dirname")
def test_init_command(mock_dirname: MagicMock, mock_copy: MagicMock) -> None:
    """Test the init command."""
    # Mock the dirname function to return a fixed path
    mock_dirname.return_value = "/fake/path"

    # Create a CLI runner
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Run the init command
        result = runner.invoke(cli, ["init", "--output", "test_sample.yml"])

        # Check that the command succeeded
        assert result.exit_code == 0

        # Check that the copy function was called with the correct arguments
        mock_copy.assert_called_once_with("/fake/path/sample_resume.yml", "test_sample.yml")

        # Check that the success message is in the output
        assert "Sample resume file created at: test_sample.yml" in result.output


@patch("yaml_resume_builder.cli.shutil.copy")
@patch("yaml_resume_builder.cli.os.path.dirname")
def test_init_command_default_output(mock_dirname: MagicMock, mock_copy: MagicMock) -> None:
    """Test the init command with default output path."""
    # Mock the dirname function to return a fixed path
    mock_dirname.return_value = "/fake/path"

    # Create a CLI runner
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Run the init command without specifying output
        result = runner.invoke(cli, ["init"])

        # Check that the command succeeded
        assert result.exit_code == 0

        # Check that the copy function was called with the correct arguments
        mock_copy.assert_called_once_with("/fake/path/sample_resume.yml", "sample_resume.yml")

        # Check that the success message is in the output
        assert "Sample resume file created at: sample_resume.yml" in result.output


@patch("yaml_resume_builder.cli.shutil.copy")
def test_init_command_error(mock_copy: MagicMock) -> None:
    """Test the init command with an error."""
    # Mock the copy function to raise an exception
    mock_copy.side_effect = Exception("Test error")

    # Create a CLI runner
    runner = CliRunner()

    # Run the init command
    result = runner.invoke(cli, ["init"])

    # Check that the command failed
    assert result.exit_code == 1

    # Check that the error message is in the output
    assert "Error creating sample resume file: Test error" in result.output


@patch("yaml_resume_builder.cli.cli")
def test_main_function(mock_cli: MagicMock) -> None:
    """Test the main entry point function."""
    # Call the main function
    main()

    # Check that the cli function was called
    mock_cli.assert_called_once()


def test_cli_help() -> None:
    """Test the CLI help command."""
    # Create a CLI runner
    runner = CliRunner()

    # Run the help command
    result = runner.invoke(cli, ["--help"])

    # Check that the command succeeded
    assert result.exit_code == 0

    # Check that the help text contains expected information
    assert "Resume Builder CLI" in result.output
    assert "build" in result.output
    assert "init" in result.output


def test_build_help() -> None:
    """Test the build command help."""
    # Create a CLI runner
    runner = CliRunner()

    # Run the build help command
    result = runner.invoke(cli, ["build", "--help"])

    # Check that the command succeeded
    assert result.exit_code == 0

    # Check that the help text contains expected information
    assert "Build a resume from a YAML file" in result.output
    assert "--input" in result.output
    assert "--output" in result.output
    assert "--template" in result.output


def test_init_help() -> None:
    """Test the init command help."""
    # Create a CLI runner
    runner = CliRunner()

    # Run the init help command
    result = runner.invoke(cli, ["init", "--help"])

    # Check that the command succeeded
    assert result.exit_code == 0

    # Check that the help text contains expected information
    assert "Create a sample YAML resume file" in result.output
    assert "--output" in result.output

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2025-05-21

### Added
- Added Achievements & Publications section to resume template

## [1.0.2] - 2025-05-21

### Added
- Added support for project technologies and dates in resume templates
- Updated project format to match Jake Gutierrez's resume template style
- Added backward compatibility for projects without technologies or dates
- Added validation for YAML data structure with warnings for unknown fields

## [1.0.1] - 2025-05-21

### Fixed
- Fixed missing PDF copy functionality in `build_resume` by using `shutil.copy` instead of manual file operations
- Fixed inconsistent error handling in `compile_latex` by removing redundant print statements
- Improved error messages by including stdout and stderr in exception messages

### Changed
- Consolidated duplicate test suites by merging minimal test files into main test files
- Improved test reliability by properly mocking `compile_latex` in tests
- Enhanced test coverage to 100% across all modules
- Simplified LaTeX escape logic test for better clarity

## [1.0.0] - 2025-05-21

### Added
- Initial release of yaml-resume-builder
- Support for generating PDF resumes from YAML files using LaTeX templates
- Command-line interface with build and init commands
- Comprehensive test suite with high coverage

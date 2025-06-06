# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.2] - 2025-06-01

### Changed
- Improved one-page optimization strategy with progressive font and spacing adjustments
- Level 1: Enhanced spacing optimizations without font changes
- Level 2: CormorantGaramond font for more compact text
- Updated LaTeX template with better spacing consistency and margin alignment

## [1.1.1] - 2025-05-30

### Added
- **Certification Links Feature**: Certifications now support optional clickable links
  - Backward compatible with existing string format
  - Generates LaTeX `\href{url}{\underline{name}}` for linked certifications
  - Mixed format support (string and dict in same YAML file)
- Enhanced LaTeX special character escaping for URLs and certification names

### Changed
- Updated sample YAML file to demonstrate new certification link format

## [1.1.0.1] - 2025-05-26

### Fixed
- Updated CLI tests to match new unified build_resume function signature
- Fixed test expectations to include one_page parameter in function calls
- Resolved test failures after API refactoring

### Technical
- All 48 tests now passing with 96% overall coverage
- Improved test reliability and maintainability

## [1.1.0] - 2025-05-26

### Added
- One-page resume optimization feature with `--one-page` CLI flag
- Progressive optimization with 5 levels (spacing, font size, margins)
- PDF page counting functionality using pypdf library
- `one_page` parameter to existing `build_resume()` function for Python API
- Comprehensive documentation for optimization feature
- 19 new tests covering optimization scenarios with 96% overall coverage

### Changed
- Enhanced CLI with new `--one-page` / `-1` flag for automatic optimization
- Updated README with detailed optimization documentation and usage examples
- Improved template renderer to support optimization parameters
- Refactored template rendering for better maintainability
- Simplified API by adding `one_page` parameter to `build_resume()` instead of separate function

### Technical
- Added pypdf>=4.0.0 dependency for PDF analysis
- Maintains professional formatting standards with graceful fallback
- Automatic optimization attempts with clear progress feedback

## [1.0.5] - 2025-05-21

### Fixed
- Fixed package distribution to include the renamed template file
- Updated package data configuration to explicitly include .tex.template files

## [1.0.4] - 2025-05-21

### Added
- Hide Achievements & Publications section when both are empty

### Changed
- Renamed template file from `simple_template.tex` to `resume.tex.template` for better clarity
- Improved cleanup of temporary LaTeX files

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

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- v0.1.10 Add a class-based view that derives from `SpectacularApiView`
- v0.1.9 Add app settings to override openapi url, etc.

## [0.1.8] - 2025-04-29

- Added test suite for views, `get_filter_parameters`, and URLs
- Added end-to-end tests that verify HTML contains the expected context data
- Added end-to-end tests that verify the overall structure and integrity of the HTML document
- Add [pre-commit](https://pre-commit.org) configuration for consistent development

### Changed

 - Changed project maintainer dependencies to use dependency-groups (installed with `--group` flag)
  instead of optional-dependencies (installed with `--extra` flag).
 - Change `scalar_viewer` to return a `TemplateResponse` instead of `HttpResponse`
 - Update QA (linting) to using pre-commit, including: ruff, mypy, djlint, etc.

## [0.1.7] - 2025-04-25

### Added

- v0.1.7 (#7) Split HTML/CSS into templates and static files.
- v0.1.7 Default to the most recent Python versions: 3.10, 3.11, 3.12, and 3.13

### Fixed

- v0.1.7 Fix bad indentation in the return statement in `get_filter_parameters.py` (#5).
- v0.1.7 Fix import error in urls.py (importing scalar_viewer from .scalar instead of .views).

## [0.1.6] - 2025-04-24

## Added
 - v0.1.6 (#4) Add ruff linting to CI pipelines
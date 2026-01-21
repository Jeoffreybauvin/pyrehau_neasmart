# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Refactored project structure: moved `RehauNeaSmartHeatarea` to `pyrehau_neasmart/heatarea.py`.
- Extracted constants to `const.py`, exceptions to `exceptions.py`, and utils to `utils.py`.

## [0.0.7] - 2026-01-21

### Changed
- Bump version for CI/CD testing.

## [0.0.6] - 2026-01-21

### Added

- Docker development environment (`Dockerfile` and `docker-compose.dev.yml`) using `python:3.14-slim`.


## [0.0.5] - 2020-04-24

### Added

- Some docstrings (generate doc with pdoc)
- Ability to change target temperature 	and heat area mode (POST requests)
- Handle errors

### Changed

- Nothing

## [0.0.4] - 2020-01-26

### Added

- Changelog :)
- Set the target (T_TARGET) temperature (POST request). Still WIP
- Heatarea's names

### Changed

- Use /data/static.xml instead of /data/cyclic.xml
- Cast temperatures to float instead of str


## [0.0.3] - 2020-01-24

### Added

- Initial version

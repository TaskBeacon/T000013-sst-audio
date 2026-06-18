# CHANGELOG

All notable development changes for `T000013-sst-audio` are documented here.

## [Unreleased]

### Changed
- Added explicit trial context metadata for the go-trial `no_response_feedback` phase.

## [1.1.2] - 2026-03-02

### Added
- Added required reference artifacts under `references/`:
  - `references.yaml`
  - `references.md`
  - `parameter_mapping.md`
  - `stimulus_mapping.md`
  - `task_logic_audit.md`

### Changed
- Rewrote all `config/*.yaml` files in UTF-8 clean format and aligned trigger naming (`stop_onset`).
- Refactored `src/run_trial.py` to add full trial context on fixation/go/stop phases and consistent SSD logging (`ssd_s`, `stop_failed`).
- Updated `main.py` to emit `exp_onset`/`exp_end` and use explicit shutdown after goodbye.
- Replaced sampler with task-specific `TaskSamplerResponder` behavior aligned to go/stop phase logic.
- Updated `README.md` and `taskbeacon.yaml` metadata to current contract style.

### Fixed
- Removed mojibake/corrupted participant-facing text in task configs and documentation.
- Fixed mismatch between runtime trigger usage and trigger-map naming in stop-signal phases.
- Fixed scripted simulation responder key to produce valid response events in go windows.

## [1.1.1] - 2026-02-18

### Changed
- Refactored responder context phase naming in `src/run_trial.py` for auditability.
- Updated stage comments and README runtime phase notes.

### Fixed
- Removed legacy MID-style stage comment patterns from trial runtime code.

## [1.1.0] - 2026-02-17

### Added
- Added mode-aware runtime flow in `main.py` (`human|qa|sim`).
- Added split runtime configs:
  - `config/config.yaml`
  - `config/config_qa.yaml`
  - `config/config_scripted_sim.yaml`
  - `config/config_sampler_sim.yaml`
- Added `responders/task_sampler.py` scaffold and standardized outputs folder structure.

### Changed
- Migrated trigger schema to structured `triggers.map/driver/policy/timing`.
- Added trial-context wiring in `src/run_trial.py` via `set_trial_context(...)`.
- Adopted `contracts.psyflow_taps: v0.1.0` in `taskbeacon.yaml`.
- Updated `.gitignore` for standardized output handling.

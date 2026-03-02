# Task Logic Audit

## 1. Paradigm Intent

- Task: Stop-Signal Task, auditory stop-cue variant (SST-Audio)
- Primary construct: Response inhibition under a go-vs-stop race process
- Manipulated factors:
  - Trial type (go vs stop)
  - Response side (left vs right)
  - Adaptive stop-signal delay (SSD)
- Dependent measures:
  - Go hit/miss rate
  - Stop success/failure rate
  - SSD adaptation trajectory
- Key citations:
  - `LOGAN1984`
  - `BAND2003`
  - `VERBRUGGEN2019`
  - `KOK2004`

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: 3 (human), 1 (qa/sim)
- Trials per block: 70 (human), 24 (qa/sim)
- Randomization/counterbalancing:
  - Custom generator enforces stop ratio and anti-clustering constraints.
- Condition generation method:
  - Custom `generate_sst_conditions(...)` in `src/utils.py`.
  - Why custom: requires constrained sequence rules (minimum leading go trials and stop-run cap) beyond flat independent label sampling.
  - Generated shape: list of condition tokens (`go_left`, `go_right`, `stop_left`, `stop_right`).
- Runtime-generated trial values:
  - SSD is retrieved per stop trial from adaptive controller and updated online from stop outcome.

### Trial State Machine

1. State name: fixation
   - Onset trigger: `fixation_onset`
   - Stimuli shown: central fixation cross
   - Valid keys: `task.key_list`
   - Timeout behavior: auto-advance after sampled fixation interval
   - Next state: go_response_window or pre_stop_go_window

2. State name: go_response_window (go trials)
   - Onset trigger: `go_onset`
   - Stimuli shown: white directional arrow
   - Valid keys: `task.key_list`
   - Timeout behavior: mark go miss and show no-response feedback
   - Next state: trial end

3. State name: pre_stop_go_window (stop trials)
   - Onset trigger: `go_onset`
   - Stimuli shown: white directional arrow
   - Valid keys: `task.key_list`
   - Timeout behavior: runs for current SSD interval
   - Next state: stop_signal_window

4. State name: stop_signal_window (stop trials)
   - Onset trigger: `stop_onset`
   - Stimuli shown: go arrow + auditory beep stop signal
   - Valid keys: `task.key_list`
   - Timeout behavior: stop success if no response during remaining go window
   - Next state: trial end

## 3. Condition Semantics

- Condition ID: `go_left`
  - Participant-facing meaning: left response to left-pointing arrow.
  - Concrete stimulus realization: white left arrow (`go_left`).
  - Outcome rules: hit when correct key in go window; else miss/error.

- Condition ID: `go_right`
  - Participant-facing meaning: right response to right-pointing arrow.
  - Concrete stimulus realization: white right arrow (`go_right`).
  - Outcome rules: hit when correct key in go window; else miss/error.

- Condition ID: `stop_left`
  - Participant-facing meaning: prepare left response but withhold after auditory stop cue.
  - Concrete stimulus realization: `go_left` plus `stop_signal` beep after SSD.
  - Outcome rules: stop failure if any keypress in pre-stop or stop windows.

- Condition ID: `stop_right`
  - Participant-facing meaning: prepare right response but withhold after auditory stop cue.
  - Concrete stimulus realization: `go_right` plus `stop_signal` beep after SSD.
  - Outcome rules: stop failure if any keypress in pre-stop or stop windows.

Participant-facing text/stimuli source:

- Participant-facing text source: `config/*.yaml` `stimuli` (`instruction_text`, `block_break`, `no_response_feedback`, `good_bye`).
- Why this source is appropriate: keeps localization changes in config without modifying trial runtime logic.
- Localization strategy: swap language strings in config while keeping `run_trial.py` unchanged.

## 4. Response and Scoring Rules

- Response mapping:
  - Left arrow -> `task.left_key`
  - Right arrow -> `task.right_key`
- Response key source: config (`task.key_list`, `task.left_key`, `task.right_key`).
- Missing-response policy:
  - Go trials: timeout -> go miss + miss feedback.
  - Stop trials: no response in both windows -> stop success.
- Correctness logic:
  - Go correctness uses StimUnit `correct_keys` matching.
  - Stop failure is `resp_pre_stop or resp_stop_window`.
- Reward/penalty updates:
  - No explicit monetary scoring in this baseline task.
- Running metrics:
  - Block-level go accuracy and stop success rate displayed in break screen.
  - SSD updated each stop trial through staircase controller.

## 5. Stimulus Layout Plan

- Screen name: fixation
  - Stimulus IDs shown together: `fixation`
  - Layout anchors (`pos`): centered default origin
  - Size/spacing: single text item
  - Readability/overlap checks: no overlap risk
  - Rationale: neutral preparatory baseline

- Screen name: go / stop trial display
  - Stimulus IDs shown together: `go_*` arrow alone, or `go_*` + `stop_signal` in stop window
  - Layout anchors (`pos`): centered for visual arrow; auditory cue is non-positional
  - Size/spacing: `size: 8` for arrows; one visual object at a time
  - Readability/overlap checks: single-arrow display avoids visual clutter
  - Rationale: isolate motor selection from stop cue timing

- Screen name: instruction / block break / goodbye
  - Stimulus IDs shown together: one `textbox`/`text` at a time
  - Layout anchors (`pos`): centered; `size: [20, 5]` where textbox is used
  - Size/spacing: `letterHeight: 0.78`
  - Readability/overlap checks: no multi-layer text overlap
  - Rationale: clear participant guidance and transition control

## 6. Trigger Plan

- `exp_onset` / `exp_end`: session start/end markers
- `block_onset` / `block_end`: block boundaries
- `fixation_onset`: fixation onset
- `go_onset`: go stimulus onset
- `go_response`: go response event
- `go_miss`: go timeout event
- `stop_onset`: auditory stop-signal onset
- `pre_stop_response`: response during SSD window
- `on_stop_response`: response after stop-signal onset
- `no_response_feedback_onset`: miss-feedback onset

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style: single mode-aware flow with shared setup and explicit output handling.
- `utils.py` used: yes.
- `utils.py` purpose:
  - adaptive SSD staircase controller
  - constrained stop/go condition generation
- Custom controller used: yes.
- Why PsyFlow-native path is insufficient:
  - online SSD adaptation requires stateful trial-by-trial updates.
- Legacy/backward-compatibility fallback logic required: no.

## 8. Inference Log

- Decision: auditory stop cue (`assets/beep.mp3`) used instead of visual red signal.
  - Why inference was required: selected papers define modality-general stop-signal rules, not one mandatory cue modality for this repo variant.
  - Citation-supported rationale: `VERBRUGGEN2019` permits stop-signal implementations that preserve timing and inhibition rule semantics.

- Decision: stop ratio fixed at 25% in generator defaults.
  - Why inference was required: literature provides guidance but no single universally fixed ratio.
  - Citation-supported rationale: `BAND2003` horse-race simulations and practical SST implementations.

- Decision: QA/sim shortened profiles.
  - Why inference was required: validation workflows require mechanism-complete but short smoke runs.
  - Citation-supported rationale: human-study trial volume recommendations (`VERBRUGGEN2019`) are not required for non-human gate execution.

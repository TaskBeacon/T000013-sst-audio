# Stop-Signal Task (SST-Audio)

![Maturity: smoke_tested](https://img.shields.io/badge/Maturity-smoke_tested-d97706?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Stop-Signal Task (SST-Audio) |
| Version | v1.1.2 |
| URL / Repository | https://github.com/TaskBeacon/T000013-sst-audio |
| Short Description | Auditory stop-signal variant of SST with adaptive stop-signal delay (SSD). |
| Created By | Zhipeng Cao (zhipeng30@foxmail.com) |
| Date Updated | 2026-03-02 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior / EEG |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural |

## Run Modes

- Human (default): `python main.py`
- QA: `python main.py qa --config config/config_qa.yaml`
- Scripted Sim: `python main.py sim --config config/config_scripted_sim.yaml`
- Sampler Sim: `python main.py sim --config config/config_sampler_sim.yaml`

## 1. Task Overview

This auditory SST measures response inhibition. Participants respond to directional arrows on go trials. On stop trials, an auditory beep appears after a stop-signal delay (SSD), and participants should withhold the response. SSD is updated online with a staircase controller targeting approximately 50% stop success.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| Setup | Load config, initialize runtime context (`human/qa/sim`), open window, load stimuli/audio, initialize triggers and SSD controller. |
| Instruction | Show instructions (voice optional in human mode). |
| Block Loop | Generate constrained go/stop conditions and run trial loop. |
| Block Summary | Compute go hit rate and stop success rate, then show break screen. |
| Finalize | Show goodbye screen, send `exp_end`, save CSV, close trigger runtime, quit PsychoPy. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Fixation | Present fixation cross for sampled duration (`0.8` to `1.0` s). |
| Go Trial | Show white arrow, collect response up to `go_duration`; timeout logs go miss and shows miss feedback. |
| Stop Trial (Phase 1) | Show white arrow during SSD (`pre_stop_go_window`) and capture early responses. |
| Stop Trial (Phase 2) | Continue go arrow while presenting auditory stop signal (`stop_signal_window`); capture failed-stop responses. |
| Update | Mark stop success/failure and update SSD staircase. |

### Controller Logic

| Component | Description |
|---|---|
| Controller | 1-up/1-down SSD staircase in `src/utils.py`. |
| Target | `target_success = 0.5` stop success convergence. |
| Bounds | SSD constrained to `0.05` to `0.5` seconds. |
| Step | SSD step size `0.05` seconds. |
| Pooling | Shared SSD by default (`condition_specific = false`). |

## 3. Configuration Summary

All runtime settings are in `config/config.yaml` (with `config_qa.yaml` and sim variants for non-human modes).

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | Participant ID (3-digit constrained form entry). |
| `subname` | Participant name (pinyin). |
| `age` | Age (5 to 60). |
| `gender` | Gender (`Male`/`Female`). |

### b. Window Settings

| Parameter | Value |
|---|---|
| `window.size` | `[1920, 1080]` |
| `window.units` | `deg` |
| `window.fullscreen` | `true` |
| `window.bg_color` | `gray` |
| `window.monitor_width_cm` | `60` |
| `window.monitor_distance_cm` | `72` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `fixation` | `text` | Central fixation cross. |
| `go_left` / `go_right` | `shape` | White directional arrows for go responses. |
| `stop_signal` | `sound` | Auditory beep stop signal (`assets/beep.mp3`). |
| `no_response_feedback` | `text` | Message shown after go timeout. |
| `block_break` | `text` | Inter-block summary with go/stop metrics. |
| `instruction_text` | `textbox` | Chinese instructions for auditory stop rule. |
| `good_bye` | `textbox` | End-of-task message. |

### d. Timing

| Phase | Duration |
|---|---|
| `fixation_duration` | Random in `[0.8, 1.0]` s |
| `go_duration` | `1.0` s |
| `no_response_feedback_duration` | `0.8` s |
| `ssd` | Adaptive (`0.05` to `0.5` s) |

### e. Triggers

| Event | Code |
|---|---:|
| `exp_onset` | 98 |
| `exp_end` | 99 |
| `block_onset` | 100 |
| `block_end` | 101 |
| `fixation_onset` | 1 |
| `go_onset` | 10 |
| `go_response` | 11 |
| `go_miss` | 12 |
| `stop_onset` | 22 |
| `pre_stop_response` | 23 |
| `on_stop_response` | 24 |
| `no_response_feedback_onset` | 30 |

### f. Adaptive Controller

| Parameter | Value |
|---|---|
| `initial_ssd` | `0.25` |
| `step` | `0.05` |
| `min_ssd` | `0.05` |
| `max_ssd` | `0.5` |
| `target_success` | `0.5` |

## 4. Methods (for academic publication)

Participants completed an auditory stop-signal task with directional go responses and infrequent stop-signal inhibition trials. Each trial began with fixation, then a directional arrow requiring a left/right button response. On stop trials, a brief auditory beep was presented after a variable stop-signal delay (SSD), and participants were instructed to withhold responding.

SSD was updated online using a staircase rule (increase after successful inhibition, decrease after failed inhibition), targeting approximately 50% stop success. Go/stop onset and response events were trigger-marked to support synchronized behavioral and EEG analyses.

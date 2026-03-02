# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `go_left` | `go_response_window` | `go_left` | White left-pointing arrow; press left key (`F`). | `LOGAN1984` | Go process is a speeded directional response to imperative stimulus. | `psychopy_builtin` | `n/a` | `shape` stimulus with left-pointing vertices. |
| `go_right` | `go_response_window` | `go_right` | White right-pointing arrow; press right key (`J`). | `LOGAN1984` | Go process is a speeded directional response to imperative stimulus. | `psychopy_builtin` | `n/a` | Symmetric response mapping with left condition. |
| `stop_left` | `pre_stop_go_window` + `stop_signal_window` | `go_left` + `stop_signal` | Left go arrow followed by auditory beep stop cue; participant should withhold response. | `BAND2003` | Stop process interrupts ongoing go process after SSD. | `licensed_external_asset` | `assets/beep.mp3` | Auditory stop modality variant; timing remains horse-race compatible. |
| `stop_right` | `pre_stop_go_window` + `stop_signal_window` | `go_right` + `stop_signal` | Right go arrow followed by auditory beep stop cue; participant should withhold response. | `BAND2003` | Stop process interrupts ongoing go process after SSD. | `licensed_external_asset` | `assets/beep.mp3` | Failed stop if response occurs in either stop-trial response window. |
| `all_conditions` | `fixation` | `fixation` | Central fixation cross before go onset. | `KOK2004` | Pre-stimulus fixation supports baseline alignment for event analyses. | `psychopy_builtin` | `n/a` | Duration sampled from `[0.8, 1.0]` seconds. |
| `go_miss_feedback` | `no_response_feedback` | `no_response_feedback` | Reminder message shown when participant misses go response window. | `VERBRUGGEN2019` | Task quality requires explicit response-window and miss handling policy. | `psychopy_builtin` | `n/a` | Text is config-defined for localization portability. |
| `block_transition` | `block` | `block_break` | Break screen displaying go hit-rate and stop success-rate. | `VERBRUGGEN2019` | Monitoring go and stop performance is recommended for SST quality control. | `psychopy_builtin` | `n/a` | Metrics derived from trial-level output. |
| `task_start_end` | `instruction_text` / `goodbye` | `instruction_text`, `good_bye` | Chinese instruction and ending screens with key guidance. | `VERBRUGGEN2019` | Clear participant instruction is mandatory for valid SST behavior. | `psychopy_builtin` | `assets/instruction_text_voice.mp3` | Human mode can add synthesized instruction voice. |

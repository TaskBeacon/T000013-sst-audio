# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `conditions` | `task.conditions` | `['go_left', 'go_right', 'stop_left', 'stop_right']` | `LOGAN1984` | SST requires a speeded go process and a competing stop process over shared response mapping. | `adapted` | Directional conditions encode left/right response factors. |
| `stop_ratio` | `src/utils.generate_sst_conditions(stop_ratio)` | `0.25` | `BAND2003` | Stop trials are sampled as a minority class in horse-race simulation design. | `inferred` | Implemented with sequence constraints in custom generator. |
| `total_blocks` | `task.total_blocks` | `3` (human), `1` (qa/sim) | `VERBRUGGEN2019` | Reliable SST estimates require repeated exposure; reduced non-human profiles are acceptable for smoke tests. | `adapted` | QA/sim intentionally reduced for gate runtime. |
| `trial_per_block` | `task.trial_per_block` | `70` (human), `24` (qa/sim) | `VERBRUGGEN2019` | Sufficient trial count is necessary for stable stop metrics. | `inferred` | Human profile aligns with standard SST scale. |
| `fixation_duration` | `timing.fixation_duration` | `[0.8, 1.0]` s | `KOK2004` | Pre-stimulus fixation supports event alignment and baseline control. | `adapted` | Sampled uniformly per trial. |
| `go_duration` | `timing.go_duration` | `1.0` s | `BAND2003` | Go response window is bounded for hit/miss classification and SSRT estimation. | `adapted` | Applied in go and stop phases. |
| `stop_signal_modality` | `stimuli.stop_signal` | `sound` (`assets/beep.mp3`) | `VERBRUGGEN2019` | Consensus guidance allows modality variants when stop cue timing and response rules remain equivalent. | `adapted` | Auditory cue is explicit in this task variant. |
| `ssd_initial` | `controller.initial_ssd` | `0.25` s | `BAND2003` | Staircase starts from intermediate delay. | `adapted` | Updated online by 1-up/1-down controller. |
| `ssd_bounds` | `controller.min_ssd`, `controller.max_ssd` | `0.05` to `0.5` s | `VERBRUGGEN2019` | Practical bounds prevent floor/ceiling stop-signal behavior. | `inferred` | Enforced in controller update logic. |
| `ssd_step` | `controller.step` | `0.05` s | `BAND2003` | Fixed-step staircase drives convergence near 50% stop success. | `direct` | Shared SSD pool by default. |
| `trigger_go_onset` | `triggers.map.go_onset` | `10` | `KOK2004` | Go-locked marker required for event-aligned EEG analysis. | `direct` | Sent on both go-only and stop trials. |
| `trigger_stop_onset` | `triggers.map.stop_onset` | `22` | `KOK2004` | Stop-signal onset marker required for successful vs failed inhibition contrasts. | `direct` | Emitted when auditory stop signal starts. |
| `trigger_pre_stop_response` | `triggers.map.pre_stop_response` | `23` | `BAND2003` | Responses before stop cue onset distinguish pre-stop failures. | `adapted` | Captured in pre-stop go window. |
| `trigger_on_stop_response` | `triggers.map.on_stop_response` | `24` | `KOK2004` | Response after stop onset marks failed inhibition outcome. | `direct` | Captured in stop-signal window. |

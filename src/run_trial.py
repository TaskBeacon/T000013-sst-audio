from functools import partial

from psyflow import StimUnit, set_trial_context
from .utils import Controller

# trial stages use task-specific phase labels via set_trial_context(...)


def _deadline_s(value) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return None
    return None


def _next_trial_id(controller) -> int:
    histories = getattr(controller, "histories", {}) or {}
    done = 0
    for items in histories.values():
        try:
            done += len(items)
        except Exception:
            continue
    return int(done) + 1


def run_trial(
    win,
    kb,
    settings,
    condition: str,
    stim_bank: dict,
    controller: Controller,
    trigger_runtime=None,
    block_id=None,
    block_idx=None,
):
    """Single SST-Audio trial."""
    trial_id = _next_trial_id(controller)
    trial_data = {"condition": condition}
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    # phase: go_response_window
    _condition = condition.split("_")[0]
    _stim = condition.split("_")[1]
    correct_key = settings.left_key if _stim == "left" else settings.right_key

    # phase: go_response_window
    fix_stim = stim_bank.get("fixation")
    make_unit(unit_label="fixation").add_stim(fix_stim).show(
        duration=settings.fixation_duration,
        onset_trigger=settings.triggers.get("fixation_onset"),
    ).to_dict(trial_data)

    # phase: go_response_window
    if _condition == "go":
        go_stim = stim_bank.get(condition)
        go_unit = make_unit(unit_label="go").add_stim(go_stim)
        set_trial_context(
            go_unit,
            trial_id=trial_id,
            phase="go_response_window",
            deadline_s=_deadline_s(settings.go_duration),
            valid_keys=list(settings.key_list),
            block_id=block_id,
            condition_id=str(condition),
            task_factors={"condition": str(condition), "stage": "go_response_window", "block_idx": block_idx},
            stim_id=str(condition),
        )
        go_unit.capture_response(
            keys=settings.key_list,
            correct_keys=correct_key,
            duration=settings.go_duration,
            onset_trigger=settings.triggers.get("go_onset"),
            response_trigger=settings.triggers.get("go_response"),
            timeout_trigger=settings.triggers.get("go_miss"),
            terminate_on_response=True,
        )
        go_unit.to_dict(trial_data)

        resp = go_unit.get_state("key_press", False)
        if not resp:
            make_unit(unit_label="no_response_feedback").add_stim(stim_bank.get("no_response_feedback")).show(
                duration=settings.no_response_feedback_duration,
                onset_trigger=settings.triggers.get("no_response_feedback_onset"),
            ).to_dict(trial_data)

    else:
        stop_stim = stim_bank.get("stop_signal")
        go_stim = stim_bank.get(condition.replace("stop", "go"))

        ssd = controller.get_ssd()
        go_unit = make_unit(unit_label="go_ssd").add_stim(go_stim)
        set_trial_context(
            go_unit,
            trial_id=trial_id,
            phase="pre_stop_go_window",
            deadline_s=_deadline_s(ssd),
            valid_keys=list(settings.key_list),
            block_id=block_id,
            condition_id=str(condition),
            task_factors={"condition": str(condition), "stage": "pre_stop_go_window", "block_idx": block_idx, "ssd_s": float(ssd)},
            stim_id=condition.replace("stop", "go"),
        )
        go_unit.capture_response(
            keys=settings.key_list,
            duration=ssd,
            onset_trigger=settings.triggers.get("pre_stop_onset"),
            response_trigger=settings.triggers.get("pre_stop_response"),
            terminate_on_response=False,
        )
        go_unit.to_dict(trial_data)
        resp1 = go_unit.get_state("key_press", False)

        rem = settings.go_duration - ssd
        stop_unit = make_unit(unit_label="stop").add_stim(go_stim).add_stim(stop_stim)
        set_trial_context(
            stop_unit,
            trial_id=trial_id,
            phase="stop_signal_window",
            deadline_s=_deadline_s(rem),
            valid_keys=list(settings.key_list),
            block_id=block_id,
            condition_id=str(condition),
            task_factors={"condition": str(condition), "stage": "stop_signal_window", "block_idx": block_idx, "ssd_s": float(ssd)},
            stim_id=str(condition),
        )
        stop_unit.capture_response(
            keys=settings.key_list,
            duration=rem,
            onset_trigger=settings.triggers.get("on_stop_onset"),
            response_trigger=settings.triggers.get("on_stop_response"),
            terminate_on_response=True,
        )
        stop_unit.to_dict(trial_data)
        resp2 = stop_unit.get_state("key_press", False)

        failed_stop = bool(resp1 or resp2)
        controller.update(success=not failed_stop)

    # outcome display
    return trial_data

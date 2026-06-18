from functools import partial

from psyflow import StimUnit, next_trial_id, set_trial_context

from .utils import Controller


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
    trial_id = next_trial_id()
    trial_data = {"condition": condition}
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    cond_kind, cond_side = str(condition).split("_", 1)
    correct_key = settings.left_key if cond_side == "left" else settings.right_key

    # phase: fixation
    fix_unit = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        fix_unit,
        trial_id=trial_id,
        phase="fixation",
        deadline_s=settings.fixation_duration,
        valid_keys=list(settings.key_list),
        block_id=block_id,
        condition_id=str(condition),
        task_factors={"condition": str(condition), "stage": "fixation", "block_idx": block_idx},
        stim_id="fixation",
    )
    fix_unit.show(
        duration=settings.fixation_duration,
        onset_trigger=settings.triggers.get("fixation_onset"),
    ).to_dict(trial_data)

    # phase: go_response_window
    if cond_kind == "go":
        go_stim = stim_bank.get(condition)
        go_unit = make_unit(unit_label="go").add_stim(go_stim)
        set_trial_context(
            go_unit,
            trial_id=trial_id,
            phase="go_response_window",
            deadline_s=settings.go_duration,
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
            no_response_unit = make_unit(unit_label="no_response_feedback").add_stim(stim_bank.get("no_response_feedback"))
            set_trial_context(
                no_response_unit,
                trial_id=trial_id,
                phase="no_response_feedback",
                deadline_s=settings.no_response_feedback_duration,
                valid_keys=[],
                block_id=block_id,
                condition_id=str(condition),
                task_factors={
                    "condition": str(condition),
                    "stage": "no_response_feedback",
                    "condition_kind": cond_kind,
                    "condition_side": cond_side,
                    "block_idx": block_idx,
                },
                stim_id="no_response_feedback",
            )
            no_response_unit.show(
                duration=settings.no_response_feedback_duration,
                onset_trigger=settings.triggers.get("no_response_feedback_onset"),
            ).to_dict(trial_data)

    # phase: pre_stop_go_window + stop_signal_window
    else:
        go_stim = stim_bank.get(condition.replace("stop", "go"))
        stop_signal = stim_bank.get("stop_signal")

        ssd = controller.get_ssd(stim=cond_side)
        trial_data["ssd_s"] = float(ssd)

        go_unit = make_unit(unit_label="go_ssd").add_stim(go_stim)
        set_trial_context(
            go_unit,
            trial_id=trial_id,
            phase="pre_stop_go_window",
            deadline_s=ssd,
            valid_keys=list(settings.key_list),
            block_id=block_id,
            condition_id=str(condition),
            task_factors={"condition": str(condition), "stage": "pre_stop_go_window", "block_idx": block_idx},
            stim_id=condition.replace("stop", "go"),
        )
        go_unit.capture_response(
            keys=settings.key_list,
            duration=ssd,
            onset_trigger=settings.triggers.get("go_onset"),
            response_trigger=settings.triggers.get("pre_stop_response"),
            terminate_on_response=False,
        )
        go_unit.to_dict(trial_data)
        resp1 = go_unit.get_state("key_press", False)

        rem = max(0.0, float(settings.go_duration) - float(ssd))
        stop_unit = make_unit(unit_label="stop").add_stim(go_stim).add_stim(stop_signal)
        set_trial_context(
            stop_unit,
            trial_id=trial_id,
            phase="stop_signal_window",
            deadline_s=rem,
            valid_keys=list(settings.key_list),
            block_id=block_id,
            condition_id=str(condition),
            task_factors={
                "condition": str(condition),
                "stage": "stop_signal_window",
                "block_idx": block_idx,
                "ssd_s": float(ssd),
            },
            stim_id="stop_signal",
        )
        stop_unit.capture_response(
            keys=settings.key_list,
            duration=rem,
            onset_trigger=settings.triggers.get("stop_onset"),
            response_trigger=settings.triggers.get("on_stop_response"),
            terminate_on_response=True,
        )
        stop_unit.to_dict(trial_data)
        resp2 = stop_unit.get_state("key_press", False)

        failed_stop = bool(resp1 or resp2)
        trial_data["stop_failed"] = failed_stop
        controller.update(success=not failed_stop, stim=cond_side)

    return trial_data

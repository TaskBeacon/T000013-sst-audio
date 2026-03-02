from __future__ import annotations

from typing import Any

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


class TaskSamplerResponder:
    """Task-local sampler responder for SST-Audio simulation."""

    def __init__(
        self,
        *,
        key_left: str = "f",
        key_right: str = "j",
        p_hit_go: float = 0.90,
        p_fail_stop: float = 0.50,
        rt_go_mean_s: float = 0.32,
        rt_go_sd_s: float = 0.05,
        rt_min_s: float = 0.12,
        continue_rt_s: float = 0.25,
    ) -> None:
        self.key_left = str(key_left)
        self.key_right = str(key_right)
        self.p_hit_go = max(0.0, min(1.0, float(p_hit_go)))
        self.p_fail_stop = max(0.0, min(1.0, float(p_fail_stop)))
        self.rt_go_mean_s = float(rt_go_mean_s)
        self.rt_go_sd_s = max(1e-6, float(rt_go_sd_s))
        self.rt_min_s = max(0.0, float(rt_min_s))
        self.continue_rt_s = max(0.01, float(continue_rt_s))

        self._rng: Any = None
        self._failed_stop_trial_ids: set[str] = set()

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng
        self._failed_stop_trial_ids.clear()

    def _pick_key(self, valid_keys: list[str], preferred: str | None = None) -> str | None:
        if not valid_keys:
            return None
        if preferred and preferred in valid_keys:
            return preferred
        return valid_keys[0]

    def _sample_rt(self) -> float:
        if self._rng is None:
            return max(self.rt_min_s, self.rt_go_mean_s)
        return max(self.rt_min_s, float(self._rng.normal(self.rt_go_mean_s, self.rt_go_sd_s)))

    def _deadline(self, obs: Observation) -> float | None:
        if obs.deadline_s is not None:
            return float(obs.deadline_s)
        if obs.response_window_s is not None:
            return float(obs.response_window_s)
        return None

    def act(self, obs: Observation) -> Action:
        if isinstance(obs, dict):
            obs = Observation.from_dict(obs)

        valid_keys = list(obs.valid_keys or [])
        if self._rng is None or not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "sst_audio_sampler", "reason": "unavailable"})

        phase = str(obs.phase or "").strip().lower()
        condition = str(obs.condition_id or "").strip().lower()
        trial_id = str(obs.trial_id or "")

        if phase in {"instruction_text", "block", "goodbye", "block_feedback"}:
            key = self._pick_key(valid_keys)
            if key is None:
                return Action(key=None, rt_s=None, meta={"source": "sst_audio_sampler", "reason": "no_valid_key"})
            return Action(key=key, rt_s=self.continue_rt_s, meta={"source": "sst_audio_sampler", "phase": phase})

        if condition.startswith("go_"):
            if phase not in {"go_response_window", "stimulus", "response"}:
                return Action(key=None, rt_s=None, meta={"source": "sst_audio_sampler", "phase": phase, "outcome": "withhold"})
            if float(self._rng.random()) > self.p_hit_go:
                return Action(key=None, rt_s=None, meta={"source": "sst_audio_sampler", "condition": condition, "outcome": "go_miss"})

            preferred = self.key_left if condition.endswith("left") else self.key_right
            key = self._pick_key(valid_keys, preferred=preferred)
            if key is None:
                return Action(key=None, rt_s=None, meta={"source": "sst_audio_sampler", "condition": condition, "outcome": "go_miss"})

            rt_s = self._sample_rt()
            deadline = self._deadline(obs)
            if deadline is not None and rt_s > deadline:
                return Action(key=None, rt_s=None, meta={"source": "sst_audio_sampler", "condition": condition, "outcome": "late"})

            return Action(key=key, rt_s=rt_s, meta={"source": "sst_audio_sampler", "condition": condition, "outcome": "go_hit"})

        if condition.startswith("stop_"):
            if phase == "pre_stop_go_window":
                if float(self._rng.random()) < self.p_fail_stop:
                    preferred = self.key_left if condition.endswith("left") else self.key_right
                    key = self._pick_key(valid_keys, preferred=preferred)
                    if key is not None:
                        if trial_id:
                            self._failed_stop_trial_ids.add(trial_id)
                        rt_s = self._sample_rt()
                        deadline = self._deadline(obs)
                        if deadline is not None and rt_s > deadline:
                            return Action(key=None, rt_s=None, meta={"source": "sst_audio_sampler", "condition": condition, "outcome": "late"})
                        return Action(key=key, rt_s=rt_s, meta={"source": "sst_audio_sampler", "condition": condition, "outcome": "stop_fail_pre"})
                return Action(key=None, rt_s=None, meta={"source": "sst_audio_sampler", "condition": condition, "outcome": "hold_pre"})

            if phase == "stop_signal_window":
                if trial_id and trial_id in self._failed_stop_trial_ids:
                    return Action(key=None, rt_s=None, meta={"source": "sst_audio_sampler", "condition": condition, "outcome": "already_failed"})
                return Action(key=None, rt_s=None, meta={"source": "sst_audio_sampler", "condition": condition, "outcome": "stop_success"})

            return Action(key=None, rt_s=None, meta={"source": "sst_audio_sampler", "condition": condition, "outcome": "withhold"})

        return Action(key=None, rt_s=None, meta={"source": "sst_audio_sampler", "outcome": "unknown_condition"})

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._failed_stop_trial_ids.clear()

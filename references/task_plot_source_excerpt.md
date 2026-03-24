# 源证据摘录（Stop-Signal Task (SST-Audio)）

## 输入文件
- [README.md](E:/xhmhc/TaskBeacon/benchmark/runs/task_plot_redo/T000013-sst-audio/README.md)
- [config/config.yaml](E:/xhmhc/TaskBeacon/benchmark/runs/task_plot_redo/T000013-sst-audio/config/config.yaml)
- [src/run_trial.py](E:/xhmhc/TaskBeacon/benchmark/runs/task_plot_redo/T000013-sst-audio/src/run_trial.py)

## 选定条件
- `go_left`
- `go_right`
- `stop_left`
- `stop_right`

## 关键试次流程
- `fixation`：`0.8` 到 `1.0` 秒，显示中央 `+`
- `go_response_window`：`1.0` 秒，显示左/右白箭头并收集按键
- `no_response_feedback`：`0.8` 秒，仅在 go 试次无反应时显示“【未按键】请在箭头出现后按键。”
- `pre_stop_go_window`：SSD 可变窗口，先显示 go 箭头并允许提前反应
- `stop_signal_window`：剩余 go 窗口，go 箭头继续显示，同时播放 `stop_signal` beep

## 备注
- `no_response_feedback` 是从 `if not resp:` 分支推断出的参与者可见屏幕，原始 `set_trial_context(...)` 中未单独标注，需要在审计中显式说明。
- stop cue 为音频资源，因此在图中以简短注释和音频资源图块表示。

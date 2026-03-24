# 任务流程审计

- 生成时间：2026-03-23
- 模式：existing
- 任务目录：`E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000013-sst-audio`

## 1. 输入来源

- [README.md](E:/xhmhc/TaskBeacon/benchmark/runs/task_plot_redo/T000013-sst-audio/README.md)
- [config/config.yaml](E:/xhmhc/TaskBeacon/benchmark/runs/task_plot_redo/T000013-sst-audio/config/config.yaml)
- [src/run_trial.py](E:/xhmhc/TaskBeacon/benchmark/runs/task_plot_redo/T000013-sst-audio/src/run_trial.py)

## 2. 从源码提取的证据

- `fixation`：中央 `+`，持续 `0.8` 到 `1.0` 秒。
- `go_response_window`：左/右白箭头，持续 `1.0` 秒，收集 `f/j` 按键。
- `no_response_feedback`：仅在 go 试次未反应时显示，持续 `0.8` 秒。
- `pre_stop_go_window`：stop 试次先显示 go 箭头，窗口长度等于当前 SSD。
- `stop_signal_window`：继续显示 go 箭头，同时播放 `stop_signal` beep，窗口长度为剩余 go 时间。

## 3. 绘图映射

- 采用一条件一时间线。
- 四条时间线分别对应 `go_left`、`go_right`、`stop_left`、`stop_right`。
- go 条件补画了 `no_response_feedback` 分支，因为它是参与者可见且在 `show()` 中发生的屏幕。
- stop 条件的音频提示用简短注释 `Beep` 表示，避免在窄屏中截断。
- 根键：`task_plot_spec`
- 规范版本：`0.2`

## 4. 版式与校验

- 输出文件：`task_flow.png`
- `max_conditions`：`4`
- `screens_per_timeline`：`4`
- `qa_mode`：`local`
- 版式结论：四条时间线均可读，go 反馈分支已补回，stop cue 未再出现长文本截断。

## 5. 说明

- 初始自动生成版本遗漏了 go 试次的 `no_response_feedback`，后续已手工补入规范并重绘。
- 该分支没有单独的 `set_trial_context(...)`，因此在审计中显式标注为推断得到的参与者可见屏幕。

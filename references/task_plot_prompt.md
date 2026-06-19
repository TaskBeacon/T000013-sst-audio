Use case: infographic-diagram
Asset type: TaskBeacon task flow diagram
Primary request: Create a clean, publication-ready task flow diagram as a timeline collection for the behavioral task described below.

Task: Stop-Signal Task (SST-Audio)
Construct: response inhibition / auditory stop signal
Rows/conditions:
- Go trial: white left/right arrow; press F for left or J for right.
- Stop trial: white arrow starts the go response, then an auditory beep stop signal plays after adaptive SSD; withhold response.

Timeline phases:
- Go trial: Fixation (800-1000 ms; no scored response; +) -> Go arrow (1000 ms; press F/J; white left/right arrow; ends on response) -> Timeout feedback (800 ms only if no response; no-response prompt)
- Stop trial: Fixation (800-1000 ms; no scored response; +) -> Pre-stop go (SSD 50-500 ms adaptive; response = stop failure; white arrow) -> Auditory stop signal (remaining go window; withhold response; white arrow remains + beep)

Visual requirements:
- White background, landscape orientation, crisp dark text, restrained condition accent colors.
- One horizontal row per condition or representative trial type.
- Each row contains 3-7 participant-screen snapshots connected by a subtle arrow.
- Each screen snapshot shows the visible stimulus or feedback, not internal variable names.
- Use gray participant-screen boxes, thin black arrows, consistent row spacing, and subtle row separators.
- Place timing labels under each screen in compact text.
- Place condition labels at the left of each row.
- Use short labels only; avoid paragraphs inside the image.
- Make all text legible at normal document preview size.
- Leave a clean blank header band across the top 15-18% of the image. This band is reserved for a fixed title, `Construct: ...` subtitle, and TaskBeacon logo lockup that will be added after generation.

Accuracy constraints:
- Do not invent phases, stimuli, condition names, keys, rewards, or timings.
- Do not add people, lab equipment, decorative scenes, logos, or unrelated icons.
- Do not draw the task title, construct subtitle, any logo, watermark, brand mark, or `TaskBeacon` text inside the generated image.
- Draw only the timeline content below the blank header band.
- If a detail is unknown, omit it rather than guessing.
- Preserve these exact terms where used: Go trial, Stop trial, Fixation, Go arrow, Pre-stop go, Auditory stop signal, Timeout feedback, only if no response, F/J, white arrow, beep, 800-1000 ms, 1000 ms, SSD 50-500 ms adaptive, remaining go window, withhold response, stop failure, 800 ms.
- Do not show a red arrow in the stop row; the stop signal is auditory, so show the white arrow plus a small sound/beep symbol.

Style:
TaskBeacon scientific infographic style: clean vector-like raster image, organized spacing, gray screen boxes, restrained color accents, and a blank header-safe area.

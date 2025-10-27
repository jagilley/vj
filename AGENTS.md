# Repository Guidelines

## Project Structure & Module Organization
- Root contains Blender Python scene scripts: `scene_01_geometric_abstract.py`, `scene_02_lighting_showcase.py`, `scene_03_procedural_materials.py`, and the entrypoint `render_all_scenes.py`.
- Assets: `.blend` files live at the root; transient assets may go in `inputs/` (ignored by Git).
- Generated artifacts: `render_*.png` are written alongside scripts by default; optional scratch outputs can go in `outputs/` (ignored by Git).
- Convenience script: `render.sh` wraps Blender CLI for macOS.

## Build, Test, and Development Commands
- Render one scene: `./render.sh 1` (or `2`, `3`). Uses Blender in background and saves `render_*.png`.
- Render all scenes: `./render.sh all`.
- Direct Blender usage (example): `/Applications/Blender.app/Contents/MacOS/Blender --background --python render_all_scenes.py -- 2`.
- Open a scene interactively: `/Applications/Blender.app/Contents/MacOS/Blender --python scene_01_geometric_abstract.py`.
- Update Blender path: edit `render.sh` if Blender is not installed at the default macOS location.

## Coding Style & Naming Conventions
- Python: follow PEP 8 with 4‑space indentation and `snake_case` for files, functions, and variables.
- Scene files: `scene_XX_short_title.py` where `XX` is zero‑padded order.
- Constants in `UPPER_SNAKE_CASE`; module‑level docstrings required for new files.
- Keep functions small and composable; prefer explicit node/scene setup over hidden side effects.

## Testing Guidelines
- No unit test framework configured. Validate changes by rendering:
  - Quick check: render Scene 1 at lower samples during development, then restore defaults.
  - Verify output file exists and visually sanity‑check materials, lighting, and camera.
- Avoid committing large temporary outputs; use `outputs/` for scratch renders.

## Commit & Pull Request Guidelines
- History is minimal; use imperative present tense (optionally Conventional Commits), e.g., `feat: add crystal shader variant`.
- PRs should include:
  - Summary of changes and reasoning
  - Blender version and platform used
  - Before/after screenshots or the produced `render_*.png`
  - Any changes to default samples or output paths

## Security & Configuration Tips
- Paths: `render.sh` assumes macOS Blender path; adjust for Linux/Windows before running CI or sharing instructions.
- Large files: keep `.blend` and renders out of commits unless essential. Verify `.gitignore` patterns for local assets.

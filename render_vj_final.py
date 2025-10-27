"""
Render the 120 BPM VJ loop to a final MP4 with higher quality.
Usage:
  /Applications/Blender.app/Contents/MacOS/Blender --background --python render_vj_final.py
"""

import bpy  # noqa: F401
import importlib.util
import os


def load_vj_module():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vj_path = os.path.join(script_dir, "scene_03_vj_loop.py")
    spec = importlib.util.spec_from_file_location("scene_03_vj_loop", vj_path)
    vj = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(vj)
    return vj


def main():
    vj = load_vj_module()
    vj.create_scene()
    vj.render_animation(output_path="outputs/vj_loop_120bpm_final.mp4", preview=False)


if __name__ == "__main__":
    main()

"""
AI Scene Assembly Demo - Main Render Script
This script demonstrates AI-driven assembly of Blender scenes by:
1. Programmatically creating complex 3D scenes
2. Setting up materials, lighting, and cameras
3. Rendering the final output

Usage:
    blender --background --python render_all_scenes.py -- [scene_number]

Examples:
    blender --background --python render_all_scenes.py -- 1
    blender --background --python render_all_scenes.py -- all
"""

import bpy
import sys
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Available scenes
SCENES = {
    1: {
        'name': 'Geometric Abstract',
        'script': 'scene_01_geometric_abstract.py',
        'output': 'render_01_geometric_abstract.png',
        'description': 'A vibrant composition of geometric shapes with varied materials'
    },
    2: {
        'name': 'Lighting Showcase',
        'script': 'scene_02_lighting_showcase.py',
        'output': 'render_02_lighting_showcase.png',
        'description': 'Demonstration of glass, reflections, and emissive materials'
    },
    3: {
        'name': 'Procedural Materials',
        'script': 'scene_03_procedural_materials.py',
        'output': 'render_03_procedural_materials.png',
        'description': 'Showcase of procedurally generated materials: marble, lava, crystal, rust'
    }
}

def print_banner():
    """Print a nice banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║          AI-Driven Blender Scene Assembly Demo              ║
    ║                                                              ║
    ║  Demonstrating programmatic creation of complex 3D scenes   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def render_scene(scene_num):
    """Render a specific scene"""
    if scene_num not in SCENES:
        print(f"Error: Scene {scene_num} does not exist!")
        return False

    scene_info = SCENES[scene_num]
    print(f"\n{'='*70}")
    print(f"SCENE {scene_num}: {scene_info['name']}")
    print(f"Description: {scene_info['description']}")
    print(f"{'='*70}\n")

    # Load and execute the scene script
    script_path = os.path.join(SCRIPT_DIR, scene_info['script'])
    if not os.path.exists(script_path):
        print(f"Error: Script not found at {script_path}")
        return False

    print(f"Executing scene script: {scene_info['script']}")
    exec(open(script_path).read(), {'__name__': '__main__', 'bpy': bpy})

    # Set output path
    output_path = os.path.join(SCRIPT_DIR, scene_info['output'])
    bpy.context.scene.render.filepath = output_path

    # Render
    print(f"\nRendering scene to: {scene_info['output']}")
    print("This may take a few minutes depending on your hardware...\n")

    bpy.ops.render.render(write_still=True)

    print(f"\n✓ Scene {scene_num} rendered successfully!")
    print(f"  Output saved to: {output_path}\n")

    return True

def main():
    """Main entry point"""
    print_banner()

    # Parse command line arguments
    # Arguments after '--' are accessible via sys.argv
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []

    # Determine which scene(s) to render
    if not argv:
        print("Usage: blender --background --python render_all_scenes.py -- [scene_number|all]")
        print("\nAvailable scenes:")
        for num, info in SCENES.items():
            print(f"  {num}: {info['name']} - {info['description']}")
        print("\nExamples:")
        print("  blender --background --python render_all_scenes.py -- 1")
        print("  blender --background --python render_all_scenes.py -- all")
        return

    scene_arg = argv[0]

    if scene_arg.lower() == 'all':
        print("Rendering all scenes...\n")
        for scene_num in SCENES.keys():
            render_scene(scene_num)
    else:
        try:
            scene_num = int(scene_arg)
            render_scene(scene_num)
        except ValueError:
            print(f"Error: Invalid scene number '{scene_arg}'")
            print("Use 'all' to render all scenes, or specify a scene number (1-3)")

    print("\n" + "="*70)
    print("All requested renders complete!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()

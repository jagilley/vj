# AI-Driven Blender Scene Assembly Demo

This project demonstrates AI-driven assembly of complex 3D scenes in Blender using Python scripts. Each scene is programmatically created, showcasing different aspects of 3D rendering, materials, and lighting.

## Features

- **Procedural Scene Generation**: All scenes are created entirely through code
- **Advanced Materials**: Showcases glass, metals, procedural textures, and emissive materials
- **Dynamic Lighting**: Demonstrates various lighting techniques
- **Modular Design**: Each scene is self-contained and can be rendered independently

## Scenes

### Scene 1: Geometric Abstract
A vibrant composition featuring:
- Randomized geometric shapes (spheres, cubes, cylinders, torus, cones)
- Varied materials (glossy, matte, metallic, emissive)
- Circular arrangement with floating elements
- Reflective ground plane

### Scene 2: Lighting Showcase
Demonstrates advanced lighting and material interaction:
- Glass spheres with different tints
- Highly reflective chrome sphere
- Emissive cubes acting as colored lights
- Glossy reflective surfaces
- Caustics from glass refraction

### Scene 3: Procedural Materials
Showcases complex procedural shader networks:
- **Marble**: Noise-based procedural marble with veins
- **Lava/Magma**: Emissive material with Voronoi and noise patterns
- **Crystal**: Glass + glossy mix with Voronoi edge detection
- **Rusty Metal**: Weathered metal with rust patterns

## Requirements

- Blender 3.0 or higher (installed at `/Applications/Blender.app` on macOS)
- Python 3.x (comes with Blender)

## Usage

### Render Individual Scenes

```bash
# Render Scene 1
/Applications/Blender.app/Contents/MacOS/Blender --background --python render_all_scenes.py -- 1

# Render Scene 2
/Applications/Blender.app/Contents/MacOS/Blender --background --python render_all_scenes.py -- 2

# Render Scene 3
/Applications/Blender.app/Contents/MacOS/Blender --background --python render_all_scenes.py -- 3
```

### Render All Scenes

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python render_all_scenes.py -- all
```

### Use Individual Scene Scripts

You can also run individual scene scripts directly:

```bash
# Open Blender with Scene 1 loaded
/Applications/Blender.app/Contents/MacOS/Blender --python scene_01_geometric_abstract.py
```

## Output

Rendered images are saved in the project directory:
- `render_01_geometric_abstract.png`
- `render_02_lighting_showcase.png`
- `render_03_procedural_materials.png`

## Render Settings

- **Engine**: Cycles (path tracing)
- **Resolution**: 1920x1080 (Full HD)
- **Samples**:
  - Scene 1: 128 samples
  - Scene 2: 256 samples (higher for glass caustics)
  - Scene 3: 256 samples (higher for procedural details)

## Project Structure

```
Blender/
├── README.md                           # This file
├── render_all_scenes.py                # Main render script
├── scene_01_geometric_abstract.py      # Geometric shapes scene
├── scene_02_lighting_showcase.py       # Lighting and materials scene
├── scene_03_procedural_materials.py    # Procedural shaders scene
└── render_*.png                        # Output renders (generated)
```

## Technical Details

### Scene Assembly Process

Each scene follows this pattern:

1. **Clear Scene**: Remove all default objects
2. **Create Materials**: Set up shader nodes programmatically
3. **Add Objects**: Create and position 3D geometry
4. **Setup Lighting**: Add and configure light sources
5. **Setup Camera**: Position and orient the camera
6. **Configure Rendering**: Set render engine and quality settings

### Material Creation

Materials are created using Blender's node-based shader system:

- **Principled BSDF**: For standard materials (metallic, roughness, etc.)
- **Glass BSDF**: For transparent refractive materials
- **Emission**: For light-emitting surfaces
- **Procedural Textures**: Noise, Voronoi, and other texture nodes
- **Color Ramps**: For controlling color transitions
- **Node Mixing**: Combining multiple shaders and textures

## Customization

You can modify any scene by:

1. Opening the scene script (e.g., `scene_01_geometric_abstract.py`)
2. Adjusting parameters like:
   - Object positions and scales
   - Material colors and properties
   - Light intensity and color
   - Camera position and angle
   - Render samples and resolution
3. Running the modified script

## AI Assembly Concept

This project demonstrates how AI can:

- **Understand 3D Concepts**: Translate high-level descriptions into technical implementations
- **Generate Complex Scenes**: Create intricate shader networks and object arrangements
- **Optimize Rendering**: Balance quality and render time
- **Follow Best Practices**: Use proper scene organization and material workflows

The scenes were designed to showcase that AI can create production-ready 3D content programmatically, useful for:
- Batch scene generation
- Procedural content pipelines
- Automated visualization
- Rapid prototyping

## Tips

- **Faster Previews**: Reduce `cycles.samples` in scene scripts for quicker test renders
- **Higher Quality**: Increase samples for final renders (512+ for production quality)
- **GPU Rendering**: Enable GPU in Blender preferences for faster renders
- **Denoising**: Enable denoising in render settings to reduce noise at lower sample counts

## License

This demo project is provided as-is for educational and demonstration purposes.

---

**Created with AI-driven scene assembly** 🤖

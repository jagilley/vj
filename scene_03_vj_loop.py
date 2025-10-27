"""
Scene 3: VJ Loop (120 BPM)
Animated loop with beat-synced motions, lighting, and materials.
Designed to sync with 120 BPM (house) tracks.
"""

import bpy
import math
from math import pi

# --- Tempo & Timing ---
BPM = 120
FPS = 30
BEATS_PER_BAR = 4
BARS = 8  # 8 bars = 16 seconds at 120 bpm
BEATS_PER_SEC = BPM / 60.0
FRAMES_PER_BEAT = int(round(FPS / BEATS_PER_SEC))  # 15 at 30 fps
TOTAL_BEATS = BEATS_PER_BAR * BARS
FRAME_START = 1
FRAME_END = FRAME_START + (TOTAL_BEATS * FRAMES_PER_BEAT) - 1  # inclusive


def beat_frame(beat_index: int) -> int:
    """Return frame index (1-based) for a given beat index (0-based)."""
    return FRAME_START + beat_index * FRAMES_PER_BEAT


def is_downbeat(beat_index: int) -> bool:
    """Downbeat at the start of each bar (every 4 beats)."""
    return beat_index % BEATS_PER_BAR == 0


def add_pulse_keyframes(id_block, data_path: str, base: float, peak: float, decay: float = 0.4):
    """
    Add quarter-note pulses for the whole loop.
    - id_block: data owner (e.g., light.data for energy, object for scale component)
    - data_path: RNA path (e.g., 'energy', 'Emission Strength', 'scale')
    - base: resting value between pulses
    - peak: value at beat
    - decay: fraction of beat duration to return to base after peak
    """
    decay_frames = max(1, int(FRAMES_PER_BEAT * decay))
    for b in range(TOTAL_BEATS + 1):
        f = beat_frame(b)
        # Peak on beat
        if data_path == 'scale':
            # Expect vector scale; keyframe all components
            id_block.scale = (peak, peak, peak)
            id_block.keyframe_insert(data_path=data_path, frame=f)
            # Return to base after decay
            id_block.scale = (base, base, base)
            id_block.keyframe_insert(data_path=data_path, frame=min(f + decay_frames, FRAME_END))
        else:
            try:
                # Some properties live on inputs, not on id_block directly
                # Here we assume scalar props on the id_block (e.g., Light.energy)
                setattr(id_block, data_path, peak)
                id_block.keyframe_insert(data_path=data_path, frame=f)
                setattr(id_block, data_path, base)
                id_block.keyframe_insert(data_path=data_path, frame=min(f + decay_frames, FRAME_END))
            except Exception:
                # Fallback: ignore if property path is not valid
                pass


def set_linear_interpolation():
    """Set all keyframes to linear interpolation for crisp pulses and smooth loops."""
    for action in bpy.data.actions:
        for fcurve in action.fcurves:
            for kp in fcurve.keyframe_points:
                kp.interpolation = 'LINEAR'

def clear_scene():
    """Remove all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Remove all materials
    for material in list(bpy.data.materials):
        try:
            bpy.data.materials.remove(material)
        except Exception:
            pass

def create_marble_material(name, animate=False):
    """Create a procedural marble material with optional animation"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping = nodes.new(type='ShaderNodeMapping')
    noise_tex1 = nodes.new(type='ShaderNodeTexNoise')
    noise_tex2 = nodes.new(type='ShaderNodeTexNoise')
    mix_rgb = nodes.new(type='ShaderNodeMix')
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    output = nodes.new(type='ShaderNodeOutputMaterial')

    # Configure noise textures
    noise_tex1.inputs['Scale'].default_value = 3.0
    noise_tex1.inputs['Detail'].default_value = 8.0
    noise_tex1.inputs['Roughness'].default_value = 0.5

    noise_tex2.inputs['Scale'].default_value = 6.0
    noise_tex2.inputs['Detail'].default_value = 4.0

    # Configure color ramp for marble veins
    color_ramp.color_ramp.elements[0].color = (0.9, 0.9, 0.95, 1.0)
    color_ramp.color_ramp.elements[1].color = (0.2, 0.2, 0.25, 1.0)

    # Configure BSDF
    bsdf.inputs['Roughness'].default_value = 0.25
    bsdf.inputs['Specular IOR Level'].default_value = 0.6

    # Link nodes
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise_tex1.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise_tex2.inputs['Vector'])
    links.new(noise_tex1.outputs['Fac'], mix_rgb.inputs['A'])
    links.new(noise_tex2.outputs['Fac'], mix_rgb.inputs['B'])
    links.new(mix_rgb.outputs['Result'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Animate mapping rotation for flowing marble effect
    if animate:
        # 1 rotation per bar for subtle flow
        mapping.inputs['Rotation'].default_value[2] = 0
        mapping.inputs['Rotation'].keyframe_insert(data_path="default_value", frame=FRAME_START, index=2)
        mapping.inputs['Rotation'].default_value[2] = math.radians(360 * BARS)
        mapping.inputs['Rotation'].keyframe_insert(data_path="default_value", frame=FRAME_END, index=2)

    return mat, mapping if animate else mat

def create_lava_material(name, animate=False):
    """Create a procedural lava/magma material with optional animation"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping = nodes.new(type='ShaderNodeMapping')
    noise_tex = nodes.new(type='ShaderNodeTexNoise')
    voronoi_tex = nodes.new(type='ShaderNodeTexVoronoi')
    color_ramp1 = nodes.new(type='ShaderNodeValToRGB')
    color_ramp2 = nodes.new(type='ShaderNodeValToRGB')
    mix_rgb = nodes.new(type='ShaderNodeMix')
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    output = nodes.new(type='ShaderNodeOutputMaterial')

    # Configure textures
    noise_tex.inputs['Scale'].default_value = 4.0
    noise_tex.inputs['Detail'].default_value = 10.0
    voronoi_tex.inputs['Scale'].default_value = 3.0

    # Configure color ramps
    color_ramp1.color_ramp.elements[0].color = (0.1, 0.0, 0.0, 1.0)
    color_ramp1.color_ramp.elements[1].color = (1.0, 0.3, 0.0, 1.0)

    color_ramp2.color_ramp.elements[0].position = 0.3
    color_ramp2.color_ramp.elements[1].position = 0.7

    # Configure BSDF for emission
    bsdf.inputs['Roughness'].default_value = 0.7
    bsdf.inputs['Emission Strength'].default_value = 2.5

    # Link nodes
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise_tex.inputs['Vector'])
    links.new(mapping.outputs['Vector'], voronoi_tex.inputs['Vector'])
    links.new(noise_tex.outputs['Fac'], color_ramp1.inputs['Fac'])
    links.new(voronoi_tex.outputs['Distance'], color_ramp2.inputs['Fac'])
    links.new(color_ramp1.outputs['Color'], mix_rgb.inputs['A'])
    links.new(color_ramp2.outputs['Color'], mix_rgb.inputs['B'])
    links.new(mix_rgb.outputs['Result'], bsdf.inputs['Base Color'])
    links.new(mix_rgb.outputs['Result'], bsdf.inputs['Emission Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Animate texture movement for flowing lava
    if animate:
        # Slow upward flow across the whole loop
        mapping.inputs['Location'].default_value[2] = 0
        mapping.inputs['Location'].keyframe_insert(data_path="default_value", frame=FRAME_START, index=2)
        mapping.inputs['Location'].default_value[2] = 5.0
        mapping.inputs['Location'].keyframe_insert(data_path="default_value", frame=FRAME_END, index=2)

        # Emission: add beat-synced keyframes programmatically later (in object setup)

    return mat, bsdf if animate else mat

def create_crystal_material(name):
    """Create a procedural crystal material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    voronoi_tex = nodes.new(type='ShaderNodeTexVoronoi')
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    glass_bsdf = nodes.new(type='ShaderNodeBsdfGlass')
    glossy_bsdf = nodes.new(type='ShaderNodeBsdfGlossy')
    mix_shader = nodes.new(type='ShaderNodeMixShader')
    output = nodes.new(type='ShaderNodeOutputMaterial')

    # Configure voronoi
    voronoi_tex.inputs['Scale'].default_value = 10.0
    voronoi_tex.feature = 'DISTANCE_TO_EDGE'

    # Configure color ramp
    color_ramp.color_ramp.elements[0].color = (0.3, 0.5, 1.0, 1.0)
    color_ramp.color_ramp.elements[1].color = (0.8, 0.9, 1.0, 1.0)

    # Configure shaders
    glass_bsdf.inputs['IOR'].default_value = 1.6
    glossy_bsdf.inputs['Roughness'].default_value = 0.08

    # Link nodes
    links.new(tex_coord.outputs['Generated'], voronoi_tex.inputs['Vector'])
    links.new(voronoi_tex.outputs['Distance'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], glass_bsdf.inputs['Color'])
    links.new(color_ramp.outputs['Color'], glossy_bsdf.inputs['Color'])
    links.new(glass_bsdf.outputs['BSDF'], mix_shader.inputs[1])
    links.new(glossy_bsdf.outputs['BSDF'], mix_shader.inputs[2])
    links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
    mix_shader.inputs['Fac'].default_value = 0.25

    return mat

def create_rusty_metal_material(name):
    """Create a procedural rusty metal material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    noise_tex = nodes.new(type='ShaderNodeTexNoise')
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    output = nodes.new(type='ShaderNodeOutputMaterial')

    # Configure noise
    noise_tex.inputs['Scale'].default_value = 14.0
    noise_tex.inputs['Detail'].default_value = 18.0

    # Configure color ramp for rust
    color_ramp.color_ramp.elements[0].color = (0.6, 0.3, 0.1, 1.0)  # Rust
    color_ramp.color_ramp.elements[1].color = (0.4, 0.4, 0.45, 1.0)  # Metal

    # Configure BSDF
    bsdf.inputs['Metallic'].default_value = 0.9
    bsdf.inputs['Roughness'].default_value = 0.55

    # Link nodes
    links.new(tex_coord.outputs['Generated'], noise_tex.inputs['Vector'])
    links.new(noise_tex.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Roughness'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat

def add_material_showcase_objects():
    """Add objects to showcase different materials with beat-synced animation."""
    # Central marble column
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 2))
    column = bpy.context.active_object
    column.scale = (0.8, 0.8, 2)
    mat, mapping = create_marble_material("Marble", animate=True)
    column.data.materials.append(mat)

    # Lava sphere with pulsating animation
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, location=(-3, -2, 1.2))
    lava_sphere = bpy.context.active_object
    lava_sphere.scale = (1.2, 1.2, 1.2)
    mat, bsdf = create_lava_material("Lava", animate=True)
    lava_sphere.data.materials.append(mat)
    # Beat-synced pulses (downbeat heavier) for scale and emission
    add_pulse_keyframes(lava_sphere, 'scale', base=1.0, peak=1.35, decay=0.35)
    # Emission strength lives on the BSDF input; keyframe via node input default_value
    try:
        bsdf.inputs['Emission Strength'].default_value = 2.0
        for b in range(TOTAL_BEATS + 1):
            f = beat_frame(b)
            strength = 6.0 if is_downbeat(b) else 4.0
            bsdf.inputs['Emission Strength'].default_value = strength
            bsdf.inputs['Emission Strength'].keyframe_insert(data_path="default_value", frame=f)
            # quick falloff
            bsdf.inputs['Emission Strength'].default_value = 2.0
            bsdf.inputs['Emission Strength'].keyframe_insert(data_path="default_value", frame=min(f + int(FRAMES_PER_BEAT * 0.3), FRAME_END))
    except Exception:
        pass

    # Crystal formation with rotation
    crystals = []
    for i in range(5):
        x = 3 + (i * 0.4) - 0.8
        y = -2 + (i % 2) * 0.3
        z = 0.5 + (i * 0.4)
        scale = 0.3 + (i * 0.15)

        bpy.ops.mesh.primitive_cone_add(location=(x, y, z))
        crystal = bpy.context.active_object
        crystal.scale = (scale, scale, scale * 2)
        crystal.rotation_euler = (0, 0, i * 0.5)
        crystal.data.materials.append(create_crystal_material(f"Crystal_{i}"))

        # Slow rotation across the full loop
        crystal.rotation_euler = (0, 0, i * 0.5)
        crystal.keyframe_insert(data_path="rotation_euler", frame=FRAME_START)
        crystal.rotation_euler = (0, 0, i * 0.5 + math.radians(360))
        crystal.keyframe_insert(data_path="rotation_euler", frame=FRAME_END)

        crystals.append(crystal)

    # Rusty metal cubes with rotation
    for i in range(3):
        x = -2 + (i * 2)
        y = 2.5
        z = 0.6

        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        cube = bpy.context.active_object
        cube.scale = (0.6, 0.6, 0.6)
        cube.rotation_euler = (math.radians(45), 0, math.radians(45 * i))
        cube.data.materials.append(create_rusty_metal_material(f"RustyMetal_{i}"))

        # Animate rotation on multiple axes across the loop
        start_rot = (math.radians(45), 0, math.radians(45 * i))
        cube.rotation_euler = start_rot
        cube.keyframe_insert(data_path="rotation_euler", frame=FRAME_START)
        cube.rotation_euler = (
            start_rot[0] + math.radians(360),
            start_rot[1] + math.radians(180),
            start_rot[2] + math.radians(360),
        )
        cube.keyframe_insert(data_path="rotation_euler", frame=FRAME_END)

    # Ground plane with marble
    bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.scale = (8, 8, 1)
    mat, mapping = create_marble_material("GroundMarble", animate=True)
    plane.data.materials.append(mat)

def setup_lighting():
    """Setup three-point lighting with beat-synced animation."""
    # Key light
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    key_light = bpy.context.active_object
    key_light.data.energy = 2.8
    key_light.rotation_euler = (math.radians(45), 0, math.radians(45))

    # Fill light with pulsation
    bpy.ops.object.light_add(type='AREA', location=(-4, -3, 6))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 180
    fill_light.data.size = 4
    # Beat-synced pulses for fill light (accent downbeats)
    add_pulse_keyframes(fill_light.data, 'energy', base=120.0, peak=240.0, decay=0.35)

    # Rim light
    bpy.ops.object.light_add(type='AREA', location=(2, 5, 4))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 140
    rim_light.data.size = 3

def setup_camera():
    """Setup camera with circular rotation animation synced to bars."""
    bpy.ops.object.camera_add(location=(6, -6, 4))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(70), 0, math.radians(45))

    bpy.context.scene.camera = camera

    # Create empty at scene center for camera to track
    bpy.ops.object.empty_add(location=(0, 0, 1.5))
    empty = bpy.context.active_object
    empty.name = "CameraTarget"

    # Add track to constraint
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = empty
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    # Animate camera rotating around the scene over the whole loop
    radius = 8.5
    height = 4
    # Quarter-turn every 2 bars (8 beats), full 360 over 8 bars
    for bar in range(BARS + 1):
        frame = beat_frame(bar * BEATS_PER_BAR)
        angle = (bar / BARS) * 2 * math.pi
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        camera.location = (x, y, height)
        camera.keyframe_insert(data_path="location", frame=frame)

    return camera

def create_scene():
    """Main scene assembly function"""
    print("Assembling Procedural Materials VJ Loop Scene...")

    clear_scene()

    # Add objects with procedural materials
    add_material_showcase_objects()

    # Setup lighting
    setup_lighting()

    # Setup camera
    setup_camera()

    # Configure render settings for animation
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64  # Quick preview; will raise for final
    # Enable denoising at View Layer level for cleaner output
    try:
        bpy.context.view_layer.cycles.use_denoising = True
    except Exception:
        try:
            scene.view_layers[0].cycles.use_denoising = True
        except Exception:
            pass
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.fps = FPS
    scene.frame_start = FRAME_START
    scene.frame_end = FRAME_END

    # Set interpolation to linear for crisp pulses and ensure loops
    set_linear_interpolation()

    # Set world background
    world = bpy.data.worlds['World']
    world.use_nodes = True
    bg_node = world.node_tree.nodes['Background']
    bg_node.inputs['Color'].default_value = (0.04, 0.04, 0.09, 1.0)  # Slightly deeper
    bg_node.inputs['Strength'].default_value = 0.25

    # Beat-synced subtle world brightness pulse for cohesion
    for b in range(TOTAL_BEATS + 1):
        f = beat_frame(b)
        bg_node.inputs['Strength'].default_value = 0.45 if is_downbeat(b) else 0.3
        bg_node.inputs['Strength'].keyframe_insert(data_path="default_value", frame=f)
        bg_node.inputs['Strength'].default_value = 0.25
        bg_node.inputs['Strength'].keyframe_insert(data_path="default_value", frame=min(f + int(FRAMES_PER_BEAT * 0.4), FRAME_END))

    print("VJ Loop Scene assembly complete!")
    print(f"Animation: {scene.frame_end - scene.frame_start + 1} frames ({(TOTAL_BEATS/BEATS_PER_BAR)} bars at {BPM} BPM)")

    # Save the blend file at project root
    try:
        bpy.ops.wm.save_as_mainfile(filepath="scene_03_vj_loop.blend")
        print("Saved to scene_03_vj_loop.blend")
    except Exception:
        pass

    # Compositor: add gentle bloom/glare for emissive hits
    try:
        scene.use_nodes = True
        nt = scene.node_tree
        nt.nodes.clear()
        n_rl = nt.nodes.new(type='CompositorNodeRLayers')
        n_glare = nt.nodes.new(type='CompositorNodeGlare')
        n_glare.glare_type = 'FOG_GLOW'
        n_glare.quality = 'HIGH'
        n_glare.size = 6
        n_glare.mix = 0.2
        n_glare.threshold = 0.6
        n_comp = nt.nodes.new(type='CompositorNodeComposite')
        nt.links.new(n_rl.outputs['Image'], n_glare.inputs['Image'])
        nt.links.new(n_glare.outputs['Image'], n_comp.inputs['Image'])
    except Exception:
        pass

def render_animation(output_path: str, fps: int = FPS, preview: bool = False):
    """Configure output and render animation to a video file.
    - output_path: path without extension or full path depending on format
    - preview: if True, reduce samples for speed
    """
    scene = bpy.context.scene
    if preview:
        if scene.render.engine == 'CYCLES':
            scene.cycles.samples = 16
    else:
        if scene.render.engine == 'CYCLES':
            scene.cycles.samples = max(scene.cycles.samples, 128)
    scene.render.fps = fps
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
    scene.render.ffmpeg.gopsize = fps * 2
    scene.render.ffmpeg.max_b_frames = 2
    scene.render.ffmpeg.audio_codec = 'AAC'
    scene.render.ffmpeg.audio_bitrate = 192
    scene.render.use_file_extension = True
    scene.render.filepath = output_path
    print(f"Rendering animation to: {output_path}")
    bpy.ops.render.render(animation=True)

if __name__ == "__main__":
    create_scene()
    # Default to render a preview file for quick iteration; caller can re-run for final
    render_animation(output_path="outputs/vj_loop_120bpm_preview.mp4", preview=True)

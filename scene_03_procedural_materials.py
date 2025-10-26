"""
Scene 3: Procedural Materials
Demonstrates AI assembly of a scene with complex procedural materials
"""

import bpy
import math

def clear_scene():
    """Remove all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Remove all materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def create_marble_material(name):
    """Create a procedural marble material"""
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
    bsdf.inputs['Roughness'].default_value = 0.3
    bsdf.inputs['Specular IOR Level'].default_value = 0.5

    # Link nodes
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise_tex1.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise_tex2.inputs['Vector'])
    links.new(noise_tex1.outputs['Fac'], mix_rgb.inputs['A'])
    links.new(noise_tex2.outputs['Fac'], mix_rgb.inputs['B'])
    links.new(mix_rgb.outputs['Result'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat

def create_lava_material(name):
    """Create a procedural lava/magma material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
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
    bsdf.inputs['Roughness'].default_value = 0.8
    bsdf.inputs['Emission Strength'].default_value = 3.0

    # Link nodes
    links.new(tex_coord.outputs['Generated'], noise_tex.inputs['Vector'])
    links.new(tex_coord.outputs['Generated'], voronoi_tex.inputs['Vector'])
    links.new(noise_tex.outputs['Fac'], color_ramp1.inputs['Fac'])
    links.new(voronoi_tex.outputs['Distance'], color_ramp2.inputs['Fac'])
    links.new(color_ramp1.outputs['Color'], mix_rgb.inputs['A'])
    links.new(color_ramp2.outputs['Color'], mix_rgb.inputs['B'])
    links.new(mix_rgb.outputs['Result'], bsdf.inputs['Base Color'])
    links.new(mix_rgb.outputs['Result'], bsdf.inputs['Emission Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat

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
    voronoi_tex.inputs['Scale'].default_value = 8.0
    voronoi_tex.feature = 'DISTANCE_TO_EDGE'

    # Configure color ramp
    color_ramp.color_ramp.elements[0].color = (0.3, 0.5, 1.0, 1.0)
    color_ramp.color_ramp.elements[1].color = (0.8, 0.9, 1.0, 1.0)

    # Configure shaders
    glass_bsdf.inputs['IOR'].default_value = 1.6
    glossy_bsdf.inputs['Roughness'].default_value = 0.1

    # Link nodes
    links.new(tex_coord.outputs['Generated'], voronoi_tex.inputs['Vector'])
    links.new(voronoi_tex.outputs['Distance'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], glass_bsdf.inputs['Color'])
    links.new(color_ramp.outputs['Color'], glossy_bsdf.inputs['Color'])
    links.new(glass_bsdf.outputs['BSDF'], mix_shader.inputs[1])
    links.new(glossy_bsdf.outputs['BSDF'], mix_shader.inputs[2])
    links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
    mix_shader.inputs['Fac'].default_value = 0.3

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
    noise_tex.inputs['Scale'].default_value = 12.0
    noise_tex.inputs['Detail'].default_value = 15.0

    # Configure color ramp for rust
    color_ramp.color_ramp.elements[0].color = (0.6, 0.3, 0.1, 1.0)  # Rust
    color_ramp.color_ramp.elements[1].color = (0.4, 0.4, 0.45, 1.0)  # Metal

    # Configure BSDF
    bsdf.inputs['Metallic'].default_value = 0.8
    bsdf.inputs['Roughness'].default_value = 0.6

    # Link nodes
    links.new(tex_coord.outputs['Generated'], noise_tex.inputs['Vector'])
    links.new(noise_tex.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Roughness'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat

def add_material_showcase_objects():
    """Add objects to showcase different materials"""
    # Central marble column
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 2))
    column = bpy.context.active_object
    column.scale = (0.8, 0.8, 2)
    column.data.materials.append(create_marble_material("Marble"))

    # Lava sphere
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, location=(-3, -2, 1.2))
    lava_sphere = bpy.context.active_object
    lava_sphere.scale = (1.2, 1.2, 1.2)
    lava_sphere.data.materials.append(create_lava_material("Lava"))

    # Crystal formation
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

    # Rusty metal cubes
    for i in range(3):
        x = -2 + (i * 2)
        y = 2.5
        z = 0.6

        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        cube = bpy.context.active_object
        cube.scale = (0.6, 0.6, 0.6)
        cube.rotation_euler = (math.radians(45), 0, math.radians(45 * i))
        cube.data.materials.append(create_rusty_metal_material(f"RustyMetal_{i}"))

    # Ground plane with marble
    bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.scale = (8, 8, 1)
    plane.data.materials.append(create_marble_material("GroundMarble"))

def setup_lighting():
    """Setup three-point lighting"""
    # Key light
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    key_light = bpy.context.active_object
    key_light.data.energy = 3.0
    key_light.rotation_euler = (math.radians(45), 0, math.radians(45))

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-4, -3, 6))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 200
    fill_light.data.size = 4

    # Rim light
    bpy.ops.object.light_add(type='AREA', location=(2, 5, 4))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 150
    rim_light.data.size = 3

def setup_camera():
    """Setup camera"""
    bpy.ops.object.camera_add(location=(6, -6, 4))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(70), 0, math.radians(45))

    bpy.context.scene.camera = camera
    return camera

def create_scene():
    """Main scene assembly function"""
    print("Assembling Procedural Materials Scene...")

    clear_scene()

    # Add objects with procedural materials
    add_material_showcase_objects()

    # Setup lighting
    setup_lighting()

    # Setup camera
    setup_camera()

    # Configure render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 256
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    # Set world background with HDRI-like environment
    world = bpy.data.worlds['World']
    world.use_nodes = True
    bg_node = world.node_tree.nodes['Background']
    bg_node.inputs['Color'].default_value = (0.5, 0.6, 0.7, 1.0)
    bg_node.inputs['Strength'].default_value = 1.0

    print("Procedural Materials Scene assembly complete!")

if __name__ == "__main__":
    create_scene()

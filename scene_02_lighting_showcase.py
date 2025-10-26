"""
Scene 2: Lighting Showcase
Demonstrates AI assembly of a scene showcasing various lighting techniques
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

def create_glass_material(name, color, ior=1.45):
    """Create a glass material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()

    # Create nodes
    node_bsdf = nodes.new(type='ShaderNodeBsdfGlass')
    node_output = nodes.new(type='ShaderNodeOutputMaterial')

    # Set properties
    node_bsdf.inputs['Color'].default_value = (*color, 1.0)
    node_bsdf.inputs['IOR'].default_value = ior

    # Link nodes
    mat.node_tree.links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])

    return mat

def create_glossy_material(name, color, roughness=0.1):
    """Create a glossy material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()

    # Create nodes
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_output = nodes.new(type='ShaderNodeOutputMaterial')

    # Set properties
    node_bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    node_bsdf.inputs['Metallic'].default_value = 1.0
    node_bsdf.inputs['Roughness'].default_value = roughness

    # Link nodes
    mat.node_tree.links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])

    return mat

def create_emissive_material(name, color, strength=5.0):
    """Create an emissive material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()

    # Create nodes
    node_emission = nodes.new(type='ShaderNodeEmission')
    node_output = nodes.new(type='ShaderNodeOutputMaterial')

    # Set properties
    node_emission.inputs['Color'].default_value = (*color, 1.0)
    node_emission.inputs['Strength'].default_value = strength

    # Link nodes
    mat.node_tree.links.new(node_emission.outputs['Emission'], node_output.inputs['Surface'])

    return mat

def add_showcase_objects():
    """Add objects to demonstrate lighting effects"""
    # Central reflective sphere
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 1.5))
    sphere = bpy.context.active_object
    sphere.scale = (1.5, 1.5, 1.5)
    sphere.data.materials.append(create_glossy_material("Mirror_Chrome", (0.9, 0.9, 0.95), roughness=0.05))

    # Glass spheres around the central sphere
    glass_positions = [
        (-3, 0, 1),
        (3, 0, 1),
        (0, -3, 1),
        (0, 3, 1),
    ]

    glass_colors = [
        (1.0, 0.3, 0.3),  # Red
        (0.3, 0.3, 1.0),  # Blue
        (0.3, 1.0, 0.3),  # Green
        (1.0, 0.8, 0.3),  # Yellow
    ]

    for i, pos in enumerate(glass_positions):
        bpy.ops.mesh.primitive_uv_sphere_add(location=pos)
        glass_sphere = bpy.context.active_object
        glass_sphere.scale = (0.8, 0.8, 0.8)
        glass_sphere.data.materials.append(create_glass_material(f"Glass_{i}", glass_colors[i]))

    # Emissive cubes (light sources)
    emit_positions = [
        (-2, -2, 3),
        (2, -2, 3),
        (-2, 2, 3),
        (2, 2, 3),
    ]

    emit_colors = [
        (1.0, 0.2, 0.2),  # Red
        (0.2, 0.2, 1.0),  # Blue
        (1.0, 1.0, 0.2),  # Yellow
        (0.2, 1.0, 1.0),  # Cyan
    ]

    for i, pos in enumerate(emit_positions):
        bpy.ops.mesh.primitive_cube_add(location=pos)
        emit_cube = bpy.context.active_object
        emit_cube.scale = (0.4, 0.4, 0.4)
        emit_cube.rotation_euler = (math.radians(45), 0, math.radians(45))
        emit_cube.data.materials.append(create_emissive_material(f"Emit_{i}", emit_colors[i], strength=10.0))

    # Ground plane - glossy to show reflections
    bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.scale = (10, 10, 1)
    plane.data.materials.append(create_glossy_material("Glossy_Ground", (0.1, 0.1, 0.15), roughness=0.2))

    # Back wall with interesting material
    bpy.ops.mesh.primitive_plane_add(location=(0, 5, 3))
    wall = bpy.context.active_object
    wall.scale = (12, 1, 6)
    wall.rotation_euler = (math.radians(90), 0, 0)
    wall.data.materials.append(create_glossy_material("Wall", (0.8, 0.8, 0.9), roughness=0.4))

def setup_lights():
    """Setup area lights for the scene"""
    # Main fill light from above
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 8))
    main_light = bpy.context.active_object
    main_light.data.energy = 200
    main_light.data.size = 8
    main_light.data.color = (1.0, 1.0, 1.0)

    # Accent light from side
    bpy.ops.object.light_add(type='AREA', location=(6, -4, 4))
    accent_light = bpy.context.active_object
    accent_light.data.energy = 150
    accent_light.data.size = 3
    accent_light.data.color = (0.8, 0.9, 1.0)

def setup_camera():
    """Setup camera"""
    bpy.ops.object.camera_add(location=(7, -7, 5))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(65), 0, math.radians(45))

    bpy.context.scene.camera = camera
    return camera

def create_scene():
    """Main scene assembly function"""
    print("Assembling Lighting Showcase Scene...")

    clear_scene()

    # Add objects
    add_showcase_objects()

    # Setup lighting
    setup_lights()

    # Setup camera
    setup_camera()

    # Configure render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 256
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    # Enable caustics for glass
    bpy.context.scene.cycles.caustics_reflective = True
    bpy.context.scene.cycles.caustics_refractive = True

    # Set world background to dark
    world = bpy.data.worlds['World']
    world.use_nodes = True
    bg_node = world.node_tree.nodes['Background']
    bg_node.inputs['Color'].default_value = (0.02, 0.02, 0.03, 1.0)
    bg_node.inputs['Strength'].default_value = 0.3

    print("Lighting Showcase Scene assembly complete!")

if __name__ == "__main__":
    create_scene()

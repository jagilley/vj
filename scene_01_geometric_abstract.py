"""
Scene 1: Geometric Abstract
Demonstrates AI assembly of a geometric abstract scene with randomized shapes and materials
"""

import bpy
import random
import math

def clear_scene():
    """Remove all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Remove all materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def create_material(name, color, metallic=0.0, roughness=0.5, emission_strength=0.0):
    """Create a principled BSDF material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    nodes.clear()

    # Create nodes
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_output = nodes.new(type='ShaderNodeOutputMaterial')

    # Set material properties
    node_bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    node_bsdf.inputs['Metallic'].default_value = metallic
    node_bsdf.inputs['Roughness'].default_value = roughness
    node_bsdf.inputs['Emission Strength'].default_value = emission_strength

    # Link nodes
    mat.node_tree.links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])

    return mat

def add_geometric_object(obj_type, location, scale, rotation, material):
    """Add a geometric object to the scene"""
    if obj_type == 'CUBE':
        bpy.ops.mesh.primitive_cube_add(location=location)
    elif obj_type == 'SPHERE':
        bpy.ops.mesh.primitive_uv_sphere_add(location=location)
    elif obj_type == 'CYLINDER':
        bpy.ops.mesh.primitive_cylinder_add(location=location)
    elif obj_type == 'TORUS':
        bpy.ops.mesh.primitive_torus_add(location=location)
    elif obj_type == 'CONE':
        bpy.ops.mesh.primitive_cone_add(location=location)

    obj = bpy.context.active_object
    obj.scale = scale
    obj.rotation_euler = rotation
    obj.data.materials.append(material)

    return obj

def setup_lighting():
    """Setup three-point lighting"""
    # Key light
    bpy.ops.object.light_add(type='AREA', location=(5, -5, 8))
    key_light = bpy.context.active_object
    key_light.data.energy = 500
    key_light.data.size = 5

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-3, -5, 5))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 200
    fill_light.data.size = 4

    # Rim light
    bpy.ops.object.light_add(type='AREA', location=(0, 5, 3))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 300
    rim_light.data.size = 3

def setup_camera():
    """Setup camera with interesting angle"""
    bpy.ops.object.camera_add(location=(8, -8, 6))
    camera = bpy.context.active_object

    # Point camera at origin
    direction = (0, 0, 1)  # Looking at slightly above origin
    camera.rotation_euler = (math.radians(60), 0, math.radians(45))

    bpy.context.scene.camera = camera
    return camera

def create_scene():
    """Main scene assembly function"""
    print("Assembling Geometric Abstract Scene...")

    clear_scene()

    # Create vibrant materials
    materials = [
        create_material("Red_Glossy", (0.8, 0.1, 0.1), metallic=0.8, roughness=0.2),
        create_material("Blue_Matte", (0.1, 0.3, 0.9), metallic=0.0, roughness=0.8),
        create_material("Gold", (1.0, 0.766, 0.336), metallic=1.0, roughness=0.3),
        create_material("Cyan_Emit", (0.0, 0.8, 0.8), metallic=0.0, roughness=0.5, emission_strength=2.0),
        create_material("Purple", (0.6, 0.1, 0.8), metallic=0.5, roughness=0.4),
        create_material("Orange", (1.0, 0.5, 0.0), metallic=0.0, roughness=0.3),
    ]

    # Shape types
    shapes = ['CUBE', 'SPHERE', 'CYLINDER', 'TORUS', 'CONE']

    # Create a composition of geometric objects
    random.seed(42)  # For reproducibility

    # Central piece - large sphere
    add_geometric_object('SPHERE', (0, 0, 1), (1.5, 1.5, 1.5), (0, 0, 0), materials[0])

    # Surrounding objects in a circular pattern
    num_objects = 8
    radius = 4
    for i in range(num_objects):
        angle = (i / num_objects) * 2 * math.pi
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = random.uniform(0.5, 2.5)

        shape = random.choice(shapes)
        scale_factor = random.uniform(0.5, 1.2)
        rotation = (random.uniform(0, math.pi), random.uniform(0, math.pi), random.uniform(0, math.pi))
        material = random.choice(materials)

        add_geometric_object(shape, (x, y, z), (scale_factor, scale_factor, scale_factor), rotation, material)

    # Add some floating elements
    for i in range(5):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        z = random.uniform(3, 5)

        shape = random.choice(['CUBE', 'SPHERE'])
        scale_factor = random.uniform(0.3, 0.6)
        rotation = (random.uniform(0, math.pi), random.uniform(0, math.pi), random.uniform(0, math.pi))
        material = random.choice(materials)

        add_geometric_object(shape, (x, y, z), (scale_factor, scale_factor, scale_factor), rotation, material)

    # Add a ground plane
    bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.scale = (15, 15, 1)
    ground_mat = create_material("Ground", (0.2, 0.2, 0.25), metallic=0.9, roughness=0.1)
    plane.data.materials.append(ground_mat)

    # Setup lighting and camera
    setup_lighting()
    setup_camera()

    # Configure render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.film_transparent = False

    # Set world background
    world = bpy.data.worlds['World']
    world.use_nodes = True
    bg_node = world.node_tree.nodes['Background']
    bg_node.inputs['Color'].default_value = (0.05, 0.05, 0.1, 1.0)
    bg_node.inputs['Strength'].default_value = 0.5

    print("Scene assembly complete!")

if __name__ == "__main__":
    create_scene()

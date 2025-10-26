import bpy
import math

# Clear existing mesh objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Set up render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.film_transparent = False
scene.render.filepath = "/Users/jaspergilley/Blender/output_rainbow.png"

# Create camera
bpy.ops.object.camera_add(location=(0, 0, 5))
camera = bpy.context.object
camera.data.type = 'ORTHO'
camera.data.ortho_scale = 2.0
scene.camera = camera

# Create a plane
bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
plane = bpy.context.object
plane.scale = (0.5625, 1, 1)  # Aspect ratio for 1080x1920

# Create material with nodes
mat = bpy.data.materials.new(name="RainbowMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
nodes.clear()

# Create nodes
output_node = nodes.new(type='ShaderNodeOutputMaterial')
output_node.location = (800, 0)

emission_node = nodes.new(type='ShaderNodeEmission')
emission_node.location = (600, 0)
emission_node.inputs['Strength'].default_value = 1.2  # Slight increase for vibrancy

# Mix node for adding subtle texture variation
mix_color = nodes.new(type='ShaderNodeMixRGB')
mix_color.location = (400, 0)
mix_color.blend_type = 'MIX'
mix_color.inputs['Fac'].default_value = 0.08  # Very subtle texture overlay

# ColorRamp for rainbow stripes
color_ramp = nodes.new(type='ShaderNodeValToRGB')
color_ramp.location = (200, 100)
color_ramp.color_ramp.interpolation = 'LINEAR'  # Soft transitions like the original

# Set up color stops (from left to right in the image) - VIBRANT colors!
stops = color_ramp.color_ramp.elements
stops[0].position = 0.0
stops[0].color = (0.02, 0.02, 0.02, 1)  # Very dark background - almost black

# Dark grey band (wider)
color_ramp.color_ramp.elements.new(0.28)
stops[1].color = (0.05, 0.05, 0.05, 1)  # Dark grey

# Dark teal - more saturated
color_ramp.color_ramp.elements.new(0.38)
stops[2].color = (0.05, 0.35, 0.45, 1)

# Bright teal - MUCH more vibrant
color_ramp.color_ramp.elements.new(0.46)
stops[3].color = (0.08, 0.55, 0.65, 1)

# Bright turquoise - super vibrant!
color_ramp.color_ramp.elements.new(0.54)
stops[4].color = (0.15, 0.85, 0.75, 1)

# Bright yellow - very saturated
color_ramp.color_ramp.elements.new(0.62)
stops[5].color = (0.95, 0.85, 0.15, 1)

# Vibrant orange
color_ramp.color_ramp.elements.new(0.70)
stops[6].color = (1.0, 0.55, 0.15, 1)

# Bright red/coral
color_ramp.color_ramp.elements.new(0.78)
stops[7].color = (0.95, 0.35, 0.25, 1)

# Back to dark
stops[-1].position = 0.86
stops[-1].color = (0.02, 0.02, 0.02, 1)  # Very dark - almost black

# Texture coordinate and mapping for diagonal pattern
tex_coord = nodes.new(type='ShaderNodeTexCoord')
tex_coord.location = (-400, 100)

# Math node to create diagonal gradient (x + y)
separate_xyz = nodes.new(type='ShaderNodeSeparateXYZ')
separate_xyz.location = (-200, 200)

math_add = nodes.new(type='ShaderNodeMath')
math_add.operation = 'ADD'
math_add.location = (0, 150)

# Rotation effect - multiply and adjust
math_multiply = nodes.new(type='ShaderNodeMath')
math_multiply.operation = 'MULTIPLY'
math_multiply.inputs[1].default_value = 0.7  # Adjust angle
math_multiply.location = (0, 100)

# Noise texture for graininess
noise_tex = nodes.new(type='ShaderNodeTexNoise')
noise_tex.location = (200, -100)
noise_tex.inputs['Scale'].default_value = 1000.0
noise_tex.inputs['Detail'].default_value = 15.0
noise_tex.inputs['Roughness'].default_value = 0.8

# Create a color ramp to adjust noise brightness for texture - make texture MORE visible
noise_adjust = nodes.new(type='ShaderNodeValToRGB')
noise_adjust.location = (0, -150)
noise_adjust.color_ramp.elements[0].position = 0.0
noise_adjust.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1)  # Darker to make grain more prominent
noise_adjust.color_ramp.elements[1].position = 1.0
noise_adjust.color_ramp.elements[1].color = (0.95, 0.95, 0.95, 1)  # Not fully white for more contrast

# Multiply color ramp by adjusted noise for texture
color_mult = nodes.new(type='ShaderNodeMixRGB')
color_mult.location = (200, -50)
color_mult.blend_type = 'MULTIPLY'
color_mult.inputs['Fac'].default_value = 1.0  # Full multiply effect

# Connect nodes
links.new(tex_coord.outputs['Object'], separate_xyz.inputs['Vector'])
links.new(separate_xyz.outputs['X'], math_add.inputs[0])
links.new(separate_xyz.outputs['Y'], math_multiply.inputs[0])
links.new(math_multiply.outputs['Value'], math_add.inputs[1])
links.new(math_add.outputs['Value'], color_ramp.inputs['Fac'])

links.new(tex_coord.outputs['Object'], noise_tex.inputs['Vector'])
# Adjust noise brightness, then use as multiplier for texture
links.new(noise_tex.outputs['Fac'], noise_adjust.inputs['Fac'])
links.new(noise_adjust.outputs['Color'], color_mult.inputs['Color1'])
links.new(color_ramp.outputs['Color'], color_mult.inputs['Color2'])

# Connect directly to emission for maximum color fidelity
links.new(color_mult.outputs['Color'], emission_node.inputs['Color'])
links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])

# Assign material to plane
plane.data.materials.append(mat)

# Set background to very dark - almost black
world = bpy.data.worlds['World']
world.use_nodes = True
bg_node = world.node_tree.nodes['Background']
bg_node.inputs['Color'].default_value = (0.02, 0.02, 0.02, 1)

print("Setup complete. Starting render...")
bpy.ops.render.render(write_still=True)
print("Render complete!")

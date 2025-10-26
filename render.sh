#!/bin/bash

# Convenience script for rendering Blender scenes
# Usage: ./render.sh [scene_number|all]

BLENDER_PATH="/Applications/Blender.app/Contents/MacOS/Blender"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RENDER_SCRIPT="$SCRIPT_DIR/render_all_scenes.py"

# Check if Blender exists
if [ ! -f "$BLENDER_PATH" ]; then
    echo "Error: Blender not found at $BLENDER_PATH"
    echo "Please update BLENDER_PATH in this script to point to your Blender installation."
    exit 1
fi

# Check if render script exists
if [ ! -f "$RENDER_SCRIPT" ]; then
    echo "Error: Render script not found at $RENDER_SCRIPT"
    exit 1
fi

# Parse arguments
if [ $# -eq 0 ]; then
    echo "AI-Driven Blender Scene Assembly Demo"
    echo "======================================"
    echo ""
    echo "Usage: ./render.sh [scene_number|all]"
    echo ""
    echo "Available scenes:"
    echo "  1 - Geometric Abstract"
    echo "  2 - Lighting Showcase"
    echo "  3 - Procedural Materials"
    echo "  all - Render all scenes"
    echo ""
    echo "Examples:"
    echo "  ./render.sh 1      # Render only Scene 1"
    echo "  ./render.sh all    # Render all scenes"
    exit 0
fi

# Run Blender with the render script
echo "Starting Blender render..."
echo ""

"$BLENDER_PATH" --background --python "$RENDER_SCRIPT" -- "$1"

echo ""
echo "Render complete! Check the output files in $SCRIPT_DIR"

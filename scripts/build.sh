#!/bin/zsh
# ============================================================================
# RenderNames - Build Script
# ============================================================================
# Creates a distributable .zip file for the extension
#
# Usage: ./scripts/build.sh
# Output: dist/rendernames-X.X.X.zip

set -e

# Get script directory
SCRIPT_DIR="${0:A:h}"
PROJECT_ROOT="${SCRIPT_DIR:h}"

# Read version from manifest
VERSION=$(grep '^version' "$PROJECT_ROOT/rendernames/blender_manifest.toml" | sed 's/version = "\(.*\)"/\1/')

echo "Building RenderNames v$VERSION..."

# Create dist directory
mkdir -p "$PROJECT_ROOT/dist"

# Output file
OUTPUT="$PROJECT_ROOT/dist/rendernames-$VERSION.zip"

# Remove old build
rm -f "$OUTPUT"

# Create zip (from project root, include only the rendernames folder)
cd "$PROJECT_ROOT"
zip -r "$OUTPUT" rendernames \
    -x "*.pyc" \
    -x "*__pycache__*" \
    -x "*.DS_Store" \
    -x "*.git*"

echo ""
echo "✓ Build complete: $OUTPUT"
echo ""
echo "To install in Blender:"
echo "  1. Open Blender"
echo "  2. Edit → Preferences → Get Extensions"
echo "  3. Click dropdown → Install from Disk"
echo "  4. Select: $OUTPUT"

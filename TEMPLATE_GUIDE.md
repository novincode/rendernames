# RenderNames Template Guide

## Critical Info: Frame Handling

**IMPORTANT**: Blender automatically appends frame numbers when rendering animations!

### For Animations (Multiple Frames):
- ❌ **DON'T use** `{{frame}}` - Blender adds frame numbers automatically
- ✅ **DO use**: `{{scene}}` or `{{scene}}_{{camera}}`
- Result: `Shot.006_0001.png`, `Shot.006_0002.png`, etc.

### For Single Frame Renders:
- ✅ Use `{{frame}}` if you want the frame number in the filename
- Example: `{{scene}}_frame_{{frame}}` → `Shot.006_frame_0052.png`

### For Video Files:
- ✅ Use `{{frame_range}}` for frame range in filename
- Example: `{{scene}}_{{frame_range}}` → `Shot.006_0001-0060.mkv`

## Default Template

```
{{scene}}
```

This creates:
- **Animation**: `Shot.006_0001.exr`, `Shot.006_0002.exr`, ...
- **Video**: `Shot.006_0001-0060.mkv` (with frame range)
- **Single frame**: `Shot.006.png`

## Available Variables

### Scene & Project
- `{{scene}}` - Current scene name
- `{{blend_file}}` - .blend filename (without extension)

### Frame Info
- `{{frame}}` - ⚠️ Not recommended for animations (Blender adds this automatically)
- `{{frame_start}}` - First frame number (e.g., 0001)
- `{{frame_end}}` - Last frame number (e.g., 0060)
- `{{frame_range}}` - Frame range (e.g., 0001-0060) - Good for video filenames

### Date & Time
- `{{date}}` - YYYY-MM-DD
- `{{time}}` - HH-MM-SS
- `{{datetime}}` - YYYY-MM-DD_HH-MM-SS
- `{{year}}`, `{{month}}`, `{{day}}`

### Camera & Technical
- `{{camera}}` - Active camera name
- `{{resolution}}` - e.g., 1920x1080
- `{{width}}`, `{{height}}`
- `{{fps}}` - Frame rate
- `{{format}}` - File format (PNG, EXR, etc.)
- `{{engine}}` - Render engine (CYCLES, EEVEE, etc.)
- `{{samples}}` - Sample count

## Common Templates

### Simple (Default)
```
{{scene}}
```
Result: `Shot.006_0001.exr`, `Shot.006_0002.exr`

### Professional
```
{{project}}/{{scene}}/{{camera}}_{{date}}
```
Result: `MyProject/Shot.006/Camera.001_2025-12-15_0001.exr`

### Archival (Videos)
```
{{scene}}_{{frame_range}}_{{engine}}_{{samples}}s
```
Result: `Shot.006_0001-0060_CYCLES_256s.mkv`

### By Camera
```
{{camera}}/{{scene}}_{{date}}
```
Result: `Camera.001/Shot.006_2025-12-15_0001.exr`

## Tips

1. **Don't duplicate frame info** - Blender adds it automatically
2. **Use frame_range for videos** - Shows the full range in one filename
3. **Use date/time for versions** - Helps track render iterations
4. **Keep it simple** - `{{scene}}` works great for most cases

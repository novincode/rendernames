# Changelog

## 1.2.0
Global / Local Settings Added
Preset Bugs Fixed


## 1.1.0
- Updates and improvements


All notable changes to RenderNames will be documented in this file.

## [0.1.0] - 2025-01-15

**Initial Release**

### Features
- Template-based render file naming with `{{variable}}` syntax
- 20+ template variables (scene, camera, date, time, etc.)
- Live preview of render output paths
- Automatic folder organization options
- Preset system (save, load, import, export)
- Built-in presets: simple, professional, archival, by_camera, minimal
- Custom base path support
- Full Blender 4.2+ and 5.0+ support
- Non-destructive enable/disable

### Known Issues
- Blender automatically appends frame numbers to animations (native Blender behavior)
- Recommendation: Use `{{frame_range}}` for video naming

### What Works
✓ Basic template variable substitution
✓ Live preview with base path calculation
✓ Preset save/load functionality
✓ Folder organization by scene/camera/date
✓ File name sanitization
✓ Frame range display in filenames
✓ Render path restoration after completion

### Testing
This is an early release. While the core functionality is stable, we recommend:
1. Testing with non-critical projects first
2. Keeping backups of important render settings
3. Reporting any issues on GitHub

### Next Steps
- User feedback and bug reports welcome
- Performance optimization in progress
- Additional variables planned for v0.2.0


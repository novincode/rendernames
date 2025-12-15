# RenderNames - Smart Render Naming for Blender

A modern Blender extension (4.2+) that gives you complete control over render output file naming and organization using a flexible template system.

## Features

- **Template Variables**: Use `{{scene}}`, `{{camera}}`, `{{date}}`, and many more
- **Live Preview**: See exactly what your output path will be as you type
- **Folder Organization**: Automatic folder creation per scene/camera/date
- **Preset System**: Save, load, import, and export your configurations
- **Blender Native**: Integrates seamlessly with Output Properties
- **Non-Destructive**: Enable/disable without losing your settings

## Installation

See [docs/INSTALL.md](docs/INSTALL.md) for detailed installation instructions.

**Quick:**
1. Download latest `.zip` from [Releases](https://github.com/novincode/rendernames/releases)
2. In Blender 4.2+: Edit → Preferences → Extensions → Install from Disk
3. Select the zip file, enable it

## Documentation

- **[Installation Guide](docs/INSTALL.md)** - How to install the extension
- **[Changelog](docs/CHANGELOG.md)** - Version history and updates
- **[Architecture](docs/architecture.md)** - Technical documentation

## Quick Start

1. Go to **Output Properties** panel (printer icon)
2. Expand the **RenderNames** section
3. Enable with the checkbox
4. Edit the template or use a preset
5. Render!

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{scene}}` | Current scene name | `Scene` |
| `{{blend_file}}` | Blend file name | `my_project` |
| `{{frame_start}}` | First frame | `0001` |
| `{{frame_end}}` | Last frame | `0250` |
| `{{frame_range}}` | Frame range (RECOMMENDED for videos) | `0001-0250` |
| `{{date}}` | Current date | `2025-01-15` |
| `{{time}}` | Current time | `14-30-45` |
| `{{datetime}}` | Date and time | `2025-01-15_14-30-45` |
| `{{camera}}` | Active camera name | `Camera` |
| `{{resolution}}` | Resolution | `1920x1080` |
| `{{fps}}` | Frame rate | `24` |
| `{{format}}` | Output format | `png` |
| `{{engine}}` | Render engine | `cycles` |
| `{{samples}}` | Sample count | `128` |

⚠️ **Important about Frame Numbers:**
- **For Animations**: Blender automatically adds frame numbers (0001, 0002, etc.) to the end of filenames


## Example Templates

**Simple:**
```
{{scene}}_
→ Scene_0001.exr, Scene_0002.exr (frame numbers added by Blender)
```

**Professional:**
```
{{blend_file}}/{{date}}/{{scene}}_{{camera}}
→ my_project/2025-01-15/Scene_Camera_0001.exr
```

**Video with Frame Range:**
```
{{scene}}_{{frame_range}}
→ Scene_0001-0250.mkv
```

## Presets

### Built-in Presets
- **Simple**: Basic naming without folders
- **Professional**: Full organization with folders
- **Archival**: Timestamped for versioning
- **By Camera**: Organized by camera
- **Minimal**: Just scene and frame

### Custom Presets
- Save your current settings with a name
- Load presets instantly from the menu
- Import/Export presets as JSON files
- Share presets between projects or team members

## Settings

### Folder Structure
- **Blend File Root**: Use blend filename as root folder
- **Per Scene**: Create subfolder for each scene
- **Per Camera**: Create subfolder for each camera  
- **Per Date**: Create subfolder for each render date

### Naming Options
- **Sanitize Names**: Replace special characters with underscores
- **Lowercase**: Convert everything to lowercase
- **Frame Padding**: Number of digits for frame numbers (1-8)

## Compatibility

- **Blender 4.2+**: Full support (modern extension system)
- **Blender 5.0+**: Full support
- **Earlier versions**: Not supported (requires extension system)

## License

GPL-3.0-or-later - Same as Blender

## Development

To build the extension:
```bash
python3 scripts/build.py          # Build the plugin
python3 scripts/build.py release  # Build with release checklist
```

See [docs/architecture.md](docs/architecture.md) for technical details.

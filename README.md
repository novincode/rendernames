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

### Blender 4.2+
1. Download the latest release `.zip` file
2. In Blender: Edit → Preferences → Get Extensions
3. Click the dropdown arrow → Install from Disk
4. Select the `.zip` file

### From Source
1. Clone this repository
2. Zip the `rendernames` folder
3. Install as above

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
| `{{frame}}` | Current frame (padded) | `0001` |
| `{{frame_start}}` | First frame | `0001` |
| `{{frame_end}}` | Last frame | `0250` |
| `{{frame_range}}` | Frame range | `1-250` |
| `{{date}}` | Current date | `2025-01-15` |
| `{{time}}` | Current time | `14-30-45` |
| `{{datetime}}` | Date and time | `2025-01-15_14-30-45` |
| `{{camera}}` | Active camera name | `Camera` |
| `{{resolution}}` | Resolution | `1920x1080` |
| `{{fps}}` | Frame rate | `24` |
| `{{format}}` | Output format | `png` |
| `{{engine}}` | Render engine | `cycles` |
| `{{samples}}` | Sample count | `128` |

## Example Templates

**Simple:**
```
{{scene}}_{{frame_start}}-{{frame_end}}
→ Scene_0001-0250
```

**Professional:**
```
{{blend_file}}/{{date}}/{{scene}}_{{camera}}/{{frame}}
→ my_project/2025-01-15/Scene_Camera/0001
```

**Archival:**
```
{{datetime}}/{{blend_file}}_{{scene}}_f{{frame_start}}-{{frame_end}}
→ 2025-01-15_14-30-45/my_project_Scene_f0001-0250
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

## Contributing

Contributions welcome! Please open an issue first to discuss changes.

## Support

- Report bugs via GitHub Issues
- Feature requests welcome

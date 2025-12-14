# RenderNames - Template Variables Reference

Complete reference for all template variables available in RenderNames.

## Syntax

Variables use double curly braces: `{{variable_name}}`

Example: `{{scene}}_{{date}}_{{frame}}`

## Variable Categories

---

## Scene & Project

### `{{scene}}`
**Current scene name**

Returns the name of the active scene.

- Example: `Scene`
- Note: Respects sanitization settings

### `{{blend_file}}`
**Blend file name without extension**

Returns the filename of the current .blend file, without the `.blend` extension.

- Example: `my_project`
- If file is unsaved: `untitled`

---

## Frame Information

### `{{frame}}`
**Current frame number (padded)**

Returns the current frame number with zero-padding based on the Frame Padding setting.

- Example (padding=4): `0001`
- Example (padding=6): `000001`

### `{{frame_start}}`
**First frame of render range**

Returns the start frame of the scene's frame range.

- Example: `0001`

### `{{frame_end}}`
**Last frame of render range**

Returns the end frame of the scene's frame range.

- Example: `0250`

### `{{frame_range}}`
**Frame range as start-end**

Returns the frame range in a compact format.

- Example: `1-250`
- Note: Does not include zero-padding

---

## Date & Time

### `{{date}}`
**Current date (YYYY-MM-DD)**

Returns the current date when the render starts.

- Example: `2025-01-15`

### `{{time}}`
**Current time (HH-MM-SS)**

Returns the current time when the render starts.

- Example: `14-30-45`

### `{{datetime}}`
**Combined date and time**

Returns both date and time with underscore separator.

- Example: `2025-01-15_14-30-45`

### `{{year}}`
**Current year**

- Example: `2025`

### `{{month}}`
**Current month (zero-padded)**

- Example: `01`

### `{{day}}`
**Current day (zero-padded)**

- Example: `15`

---

## Camera

### `{{camera}}`
**Active camera name**

Returns the name of the scene's active camera.

- Example: `Camera`
- If no camera: `no_camera`

---

## Resolution

### `{{resolution}}`
**Full resolution as WxH**

Returns the render resolution.

- Example: `1920x1080`

### `{{width}}`
**Resolution width only**

- Example: `1920`

### `{{height}}`
**Resolution height only**

- Example: `1080`

### `{{percent}}`
**Resolution percentage**

Returns the resolution scale percentage.

- Example: `100`

---

## Render Settings

### `{{fps}}`
**Frames per second**

Returns the scene's frame rate.

- Example: `24`

### `{{format}}`
**Output format (lowercase)**

Returns the file format from Output settings.

- Example: `png`, `jpeg`, `exr`, `mp4`

### `{{engine}}`
**Render engine name (lowercase)**

Returns the active render engine without the "BLENDER_" prefix.

- Examples: `cycles`, `eevee`, `eevee_next`, `workbench`

### `{{samples}}`
**Render sample count**

Returns the sample count for Cycles or EEVEE.

- Example: `128`
- For engines without samples: `n/a`

---

## Naming Options Effect

### Sanitize Names
When enabled:
- Spaces → underscores
- Removes: `< > : " / \ | ? *`
- Removes leading/trailing dots
- Collapses multiple underscores

### Lowercase
When enabled:
- All variable output converted to lowercase

### Frame Padding
- Affects: `{{frame}}`, `{{frame_start}}`, `{{frame_end}}`
- Range: 1-8 digits
- Example (padding=4): `0001`

---

## Template Examples

### Animation Sequence
```
{{blend_file}}/{{scene}}/{{frame}}
→ my_project/Scene/0001.png
```

### Daily Renders
```
{{date}}/{{scene}}_{{time}}
→ 2025-01-15/Scene_14-30-45
```

### Multi-Camera Setup
```
{{blend_file}}/{{camera}}/{{scene}}_{{frame}}
→ my_project/Camera_Front/Scene_0001
```

### Version Control
```
{{datetime}}_{{blend_file}}_{{scene}}_{{engine}}_{{samples}}
→ 2025-01-15_14-30-45_my_project_Scene_cycles_128
```

### Professional Studio
```
{{year}}/{{month}}/{{blend_file}}/{{scene}}_{{camera}}_{{resolution}}/{{frame}}
→ 2025/01/my_project/Scene_Camera_1920x1080/0001
```

---

## Path Separators

Use `/` in templates to create folder structure:

```
{{blend_file}}/{{scene}}/{{date}}/{{frame}}
```

This creates nested folders automatically when rendering.

---

## Tips

1. **For animations**: Always include `{{frame}}` in your template
2. **For stills**: Use `{{datetime}}` to avoid overwriting
3. **For organization**: Put time-based variables (`{{date}}`) early in path
4. **For sharing**: Use `{{blend_file}}` to keep renders with their source

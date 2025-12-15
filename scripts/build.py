#!/usr/bin/env python3
"""
RenderNames Build Script
Simple: Just builds the extension package.

Usage:
    python3 scripts/build.py

Output: dist/rendernames.zip (ready to install in Blender)
        - Always named 'rendernames.zip' for consistent GitHub release URLs
        - Version tracked in blender_manifest.toml
"""

import re
import sys
import shutil
import subprocess
from pathlib import Path


class Build:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.manifest = self.repo_root / "rendernames" / "blender_manifest.toml"
        self.dist_dir = self.repo_root / "dist"
    
    def get_version(self) -> str:
        """Get version from manifest."""
        with open(self.manifest) as f:
            for line in f:
                match = re.match(r'version = "([^"]+)"', line)
                if match:
                    return match.group(1)
        raise ValueError("No version found in manifest")
    
    def check_code(self):
        """Verify Python compiles."""
        print("🔍 Checking code...")
        rendernames_dir = self.repo_root / "rendernames"
        py_files = list(rendernames_dir.glob("*.py"))
        
        for py_file in py_files:
            result = subprocess.run(
                ["python3", "-m", "py_compile", str(py_file)],
                capture_output=True
            )
            if result.returncode != 0:
                print(f"❌ Error in {py_file.name}:")
                print(result.stderr.decode())
                sys.exit(1)
        print(f"   ✓ All {len(py_files)} Python files compile")
    
    def check_structure(self):
        """Verify required files exist."""
        print("📁 Checking structure...")
        required = [
            "rendernames/__init__.py",
            "rendernames/blender_manifest.toml",
            "rendernames/properties.py",
            "rendernames/operators.py",
            "rendernames/panels.py",
            "rendernames/handlers.py",
            "rendernames/template_engine.py",
            "rendernames/presets.py",
        ]
        
        for file in required:
            if not (self.repo_root / file).exists():
                print(f"❌ Missing: {file}")
                sys.exit(1)
        print(f"   ✓ All {len(required)} required files present")
    
    def create_readme(self):
        """Create user-friendly README for the package."""
        version = self.get_version()
        readme = f"""RenderNames for Blender
=======================

VERSION: {version}
LICENSE: GPL-3.0-or-later

INSTALLATION:
1. Extract this folder
2. In Blender 4.2+: Edit → Preferences → Extensions
3. Click "Install from Disk"
4. Select the rendernames folder
5. Enable the extension

QUICK START:
- Go to Output Properties (printer icon on the right)
- Enable RenderNames
- Edit the template or pick a preset
- Render!

TEMPLATE EXAMPLES:
  {{{{scene}}}}_               → Scene_0001.exr
  {{{{blend_file}}}}/{{{{date}}}}/{{{{scene}}}}   → my_project/2025-01-15/Scene_0001.exr
  {{{{scene}}}}_{{{{frame_range}}}}  → Scene_0001-0250.mkv

FEATURES:
- Template-based render naming with variables
- Live preview of render paths
- Folder organization (by scene, camera, date)
- Preset system (save, load, import, export)
- Built-in presets included

DOCUMENTATION:
https://github.com/novincode/rendernames
https://github.com/novincode/rendernames/blob/main/docs/INSTALL.md
https://github.com/novincode/rendernames/blob/main/CHANGELOG.md

IMPORTANT ABOUT ANIMATIONS:
Blender automatically adds frame numbers to animation outputs.

SUPPORT:
Star: https://github.com/novincode/rendernames/
Sponsor: https://github.com/sponsors/novincode
Report issues: https://github.com/novincode/rendernames/issues
"""
        return readme
    
    def build(self):
        """Build the extension package."""
        version = self.get_version()
        print(f"\n{'='*60}")
        print(f"Building RenderNames v{version}")
        print(f"{'='*60}\n")
        
        # Check
        self.check_code()
        self.check_structure()
        
        # Create dist
        self.dist_dir.mkdir(exist_ok=True)
        
        # Create a staging directory with everything to package
        print(f"\n📦 Creating package...")
        staging_dir = self.dist_dir / "rendernames-staging"
        if staging_dir.exists():
            shutil.rmtree(staging_dir)
        staging_dir.mkdir()
        
        # Copy the extension folder (exclude __pycache__)
        src_plugin = self.repo_root / "rendernames"
        dst_plugin = staging_dir / "rendernames"
        ignore = shutil.ignore_patterns('__pycache__', '*.pyc')
        shutil.copytree(src_plugin, dst_plugin, ignore=ignore)
        
        # Copy README.txt into staging
        readme_content = self.create_readme()
        readme_file = staging_dir / "README.txt"
        with open(readme_file, "w") as f:
            f.write(readme_content)
        
        # Copy LICENSE into staging
        license_src = self.repo_root / "LICENSE"
        if license_src.exists():
            license_dst = staging_dir / "LICENSE"
            shutil.copy(license_src, license_dst)
        
        # Create zip from staging directory
        # Always use 'rendernames.zip' for consistent GitHub release URLs
        zip_name = "rendernames"
        zip_path = self.dist_dir / zip_name
        
        try:
            shutil.make_archive(
                str(zip_path),
                'zip',
                staging_dir,
                '.'
            )
            
            # Clean up staging
            shutil.rmtree(staging_dir)
            
            zip_file = f"{zip_path}.zip"
            size_mb = (self.repo_root / zip_file).stat().st_size / 1024 / 1024
            
            print(f"\n{'='*60}")
            print(f"✓ Build Complete!")
            print(f"{'='*60}")
            print(f"\n📦 Package:      {zip_file}")
            print(f"   Size:        {size_mb:.2f} MB")
            print(f"\nContains:")
            print(f"   - rendernames/     (plugin folder)")
            print(f"   - README.txt       (installation guide)")
            print(f"   - LICENSE          (GPL-3.0)")
            print(f"\n✓ Ready to install in Blender!")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"❌ Build failed: {e}")
            if staging_dir.exists():
                shutil.rmtree(staging_dir)
            sys.exit(1)


if __name__ == "__main__":
    Build().build()

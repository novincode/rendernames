#!/usr/bin/env python3
"""
RenderNames Release Script
Handles version bumping, building, and release guidance.

Usage:
    python3 scripts/release.py patch
    python3 scripts/release.py minor
    python3 scripts/release.py major

Actions:
1. Bumps version in manifest
2. Calls build.py to create package
3. Shows release checklist with git commands
"""

import re
import sys
import subprocess
from pathlib import Path


class Release:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.manifest = self.repo_root / "rendernames" / "blender_manifest.toml"
    
    def get_current_version(self) -> str:
        """Get version from manifest."""
        with open(self.manifest) as f:
            for line in f:
                match = re.match(r'version = "([^"]+)"', line)
                if match:
                    return match.group(1)
        raise ValueError("No version found in manifest")
    
    def parse_version(self, version: str) -> tuple:
        """Parse version string into (major, minor, patch)."""
        parts = version.split('.')
        if len(parts) != 3:
            raise ValueError(f"Invalid version: {version}")
        return tuple(int(p) for p in parts)
    
    def bump_version(self, version: str, bump_type: str) -> str:
        """Bump version according to semver."""
        major, minor, patch = self.parse_version(version)
        
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "patch":
            patch += 1
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")
        
        return f"{major}.{minor}.{patch}"
    
    def update_manifest(self, new_version: str):
        """Update version in manifest."""
        with open(self.manifest) as f:
            content = f.read()
        
        old_pattern = r'version = "[^"]+"'
        new_content = re.sub(
            old_pattern,
            f'version = "{new_version}"',
            content
        )
        
        with open(self.manifest, 'w') as f:
            f.write(new_content)
    
    def update_changelog(self, new_version: str):
        """Add entry to CHANGELOG.md if it exists."""
        changelog = self.repo_root / "docs" / "CHANGELOG.md"
        if not changelog.exists():
            return
        
        with open(changelog) as f:
            content = f.read()
        
        # Add new version at the top if not already present
        if f"## {new_version}" not in content:
            entry = f"""## {new_version}
- Initial release features

"""
            new_content = content.replace("# Changelog\n", f"# Changelog\n\n{entry}", 1)
            with open(changelog, 'w') as f:
                f.write(new_content)
    
    def build(self):
        """Call build.py to create package."""
        result = subprocess.run(
            ["python3", "scripts/build.py"],
            cwd=self.repo_root
        )
        if result.returncode != 0:
            print("❌ Build failed!")
            sys.exit(1)
    
    def show_next_steps(self, new_version: str):
        """Show release checklist."""
        print(f"\n{'='*60}")
        print(f"Release Checklist - v{new_version}")
        print(f"{'='*60}\n")
        
        print("✓ Version updated in manifest")
        print("✓ Package built and ready in dist/\n")
        
        print("NEXT STEPS:")
        print(f"1. Test the package in Blender:")
        print(f"   - Open Blender")
        print(f"   - Preferences → Extensions → Install from Disk")
        print(f"   - Select: dist/rendernames-{new_version}.zip")
        print(f"   - Test features thoroughly\n")
        
        print(f"2. Commit changes:")
        print(f"   git add rendernames/blender_manifest.toml docs/CHANGELOG.md")
        print(f"   git commit -m \"Release v{new_version}\"\n")
        
        print(f"3. Create and push tag:")
        print(f"   git tag v{new_version}")
        print(f"   git push origin main")
        print(f"   git push origin v{new_version}\n")
        
        print(f"4. GitHub will automatically create a release")
        print(f"   - Find it in: https://github.com/novincode/rendernames/releases")
        print(f"   - Download dist/rendernames-{new_version}.zip from there\n")
        
        print("5. Optional: Submit to Blender extensions marketplace")
        print(f"   - Visit: https://extensions.blender.org/submit/")
        print(f"   - Upload the dist/rendernames-{new_version}.zip file\n")
        
        print(f"{'='*60}\n")
    
    def release(self, bump_type: str):
        """Execute release."""
        if bump_type not in ("major", "minor", "patch"):
            print(f"Invalid bump type: {bump_type}")
            print("Use: patch, minor, or major")
            sys.exit(1)
        
        current = self.get_current_version()
        new_version = self.bump_version(current, bump_type)
        
        print(f"\n{'='*60}")
        print(f"RenderNames Release Manager")
        print(f"{'='*60}\n")
        print(f"Current version: {current}")
        print(f"New version:    {new_version}")
        print(f"Bump type:      {bump_type}\n")
        
        # Update files
        print("📝 Updating manifest...")
        self.update_manifest(new_version)
        
        print("📝 Updating changelog...")
        self.update_changelog(new_version)
        
        # Build
        print("🔨 Building package...")
        self.build()
        
        # Show next steps
        self.show_next_steps(new_version)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/release.py [patch|minor|major]")
        print("\nExamples:")
        print("  python3 scripts/release.py patch   # 0.1.0 → 0.1.1")
        print("  python3 scripts/release.py minor   # 0.1.0 → 0.2.0")
        print("  python3 scripts/release.py major   # 0.1.0 → 1.0.0")
        sys.exit(1)
    
    Release().release(sys.argv[1])

#!/usr/bin/env python3
"""Check for package updates in COPR repository and optionally update them."""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import json
import urllib.error
import urllib.request


class Package:
    """Represents a package with its spec file and metadata."""

    def __init__(self, spec_file: Path):
        self.spec_file = spec_file
        self.name = ""
        self.version = ""
        self.url = ""
        self.dependencies: Set[str] = set()
        self._parse_spec()

    def _parse_spec(self):
        """Parse spec file for package information."""
        content = self.spec_file.read_text()

        name_match = re.search(r'^Name:\s+(.+)$', content, re.MULTILINE)
        version_match = re.search(r'^Version:\s+(.+)$', content, re.MULTILINE)
        url_match = re.search(r'^URL:\s+(.+)$', content, re.MULTILINE)

        self.name = name_match.group(1).strip() if name_match else ""
        self.version = version_match.group(1).strip() if version_match else ""
        self.url = url_match.group(1).strip() if url_match else ""

        # Extract BuildRequires dependencies (only hypr* packages)
        for match in re.finditer(r'BuildRequires:\s+pkgconfig\(([^)]+)\)', content):
            dep = match.group(1).strip()
            if dep.startswith('hypr') or dep == 'aquamarine':
                self.dependencies.add(dep)

    def update_version(self, new_version: str) -> bool:
        """Update the version in the spec file."""
        try:
            content = self.spec_file.read_text()
            old_line = f"Version:        {self.version}"
            new_line = f"Version:        {new_version}"

            if old_line not in content:
                print(f"  Warning: Could not find exact version line in {self.spec_file}")
                return False

            new_content = content.replace(old_line, new_line, 1)
            self.spec_file.write_text(new_content)
            self.version = new_version
            return True
        except Exception as e:
            print(f"  Error updating {self.spec_file}: {e}")
            return False


def get_github_latest_tag(repo_url: str) -> Optional[str]:
    """Get latest tag version from GitHub."""
    if not repo_url.startswith("https://github.com/"):
        return None

    repo_path = repo_url.replace("https://github.com/", "")
    api_url = f"https://api.github.com/repos/{repo_path}/tags"

    try:
        req = urllib.request.Request(api_url)
        req.add_header('Accept', 'application/vnd.github.v3+json')

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data and len(data) > 0:
                tag_name = data[0].get('name', '')
                return tag_name.lstrip('v')
    except Exception as e:
        print(f"  Error fetching tags: {e}", file=sys.stderr)
    return None


def get_github_latest_release(repo_url: str) -> Optional[str]:
    """Get latest release version from GitHub, fallback to tags if no releases."""
    if not repo_url.startswith("https://github.com/"):
        return None

    repo_path = repo_url.replace("https://github.com/", "")
    api_url = f"https://api.github.com/repos/{repo_path}/releases/latest"

    try:
        req = urllib.request.Request(api_url)
        req.add_header('Accept', 'application/vnd.github.v3+json')

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            tag_name = data.get('tag_name', '')
            return tag_name.lstrip('v')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return get_github_latest_tag(repo_url)
        print(f"  Error fetching from GitHub: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  Error fetching from GitHub: {e}", file=sys.stderr)
        return None


def compare_versions(current: str, latest: str) -> bool:
    """Return True if latest > current."""
    def version_tuple(v):
        return tuple(map(int, re.findall(r'\d+', v)))

    try:
        return version_tuple(latest) > version_tuple(current)
    except:
        return current != latest


def topological_sort(packages: Dict[str, Package],
                     packages_to_build: Set[str]) -> List[List[str]]:
    """
    Perform topological sort to determine build order.
    Returns list of layers where each layer can be built in parallel.
    """
    # Build dependency graph (only for packages that need to be built)
    graph = defaultdict(set)
    in_degree = defaultdict(int)

    # Initialize all packages that need to be built
    for pkg_name in packages_to_build:
        in_degree[pkg_name] = 0

    # Build the graph
    for pkg_name in packages_to_build:
        pkg = packages[pkg_name]
        for dep in pkg.dependencies:
            # Only consider dependencies on packages that need to be built
            if dep in packages_to_build:
                graph[dep].add(pkg_name)
                in_degree[pkg_name] += 1

    # Perform topological sort by layers
    layers = []
    remaining = set(packages_to_build)

    while remaining:
        # Find all packages with no dependencies (in this iteration)
        current_layer = [pkg for pkg in remaining if in_degree[pkg] == 0]

        if not current_layer:
            # Circular dependency detected
            print("\nWarning: Circular dependency detected among:", remaining)
            current_layer = list(remaining)

        layers.append(sorted(current_layer))

        # Remove current layer from graph
        for pkg in current_layer:
            remaining.remove(pkg)
            for dependent in graph[pkg]:
                in_degree[dependent] -= 1

    return layers


def print_build_order(packages: Dict[str, Package],
                     updated_packages: Set[str]):
    """Print the build order for updated packages."""
    if not updated_packages:
        return

    print("\n" + "="*70)
    print("BUILD ORDER")
    print("="*70)

    layers = topological_sort(packages, updated_packages)

    for i, layer in enumerate(layers, 1):
        print(f"\nLayer {i} (can be built in parallel):")
        for pkg_name in layer:
            pkg = packages[pkg_name]
            deps = pkg.dependencies & updated_packages
            if deps:
                print(f"  • {pkg_name} (depends on: {', '.join(sorted(deps))})")
            else:
                print(f"  • {pkg_name} (no dependencies on updated packages)")


def main():
    parser = argparse.ArgumentParser(
        description="Check for package updates in COPR repository and optionally update them."
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check for updates without modifying spec files"
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent
    spec_files = sorted(repo_root.glob("**/*.spec"))

    # Load all packages
    packages: Dict[str, Package] = {}
    for spec_file in spec_files:
        pkg = Package(spec_file)
        if pkg.name:
            packages[pkg.name] = pkg

    updates_available: List[Tuple[str, str, str]] = []
    up_to_date: List[Tuple[str, str]] = []
    errors: List[str] = []

    print("Checking for package updates...\n")

    for pkg in packages.values():
        if not pkg.name or not pkg.version or not pkg.url:
            errors.append(f"{pkg.spec_file.parent.name}: Missing spec info")
            continue

        print(f"Checking {pkg.name} (current: {pkg.version})...", end=" ", flush=True)

        latest = get_github_latest_release(pkg.url)

        if latest is None:
            errors.append(f"{pkg.name}: Could not fetch latest version")
            print("ERROR")
            continue

        if compare_versions(pkg.version, latest):
            updates_available.append((pkg.name, pkg.version, latest))
            print(f"UPDATE AVAILABLE: {latest}")
        else:
            up_to_date.append((pkg.name, pkg.version))
            print("up to date")

    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    if updates_available:
        print(f"\n🔔 {len(updates_available)} package(s) with updates available:")
        for name, current, latest in updates_available:
            print(f"  • {name}: {current} → {latest}")

    if up_to_date:
        print(f"\n✓ {len(up_to_date)} package(s) up to date:")
        for name, version in up_to_date:
            print(f"  • {name}: {version}")

    if errors:
        print(f"\n⚠ {len(errors)} error(s):")
        for error in errors:
            print(f"  • {error}")

    # Update packages if not in check-only mode
    if updates_available and not args.check_only:
        print("\n" + "="*70)
        print("UPDATING PACKAGES")
        print("="*70 + "\n")

        updated_packages = set()
        failed_updates = []

        for name, current, latest in updates_available:
            print(f"Updating {name} from {current} to {latest}...", end=" ", flush=True)
            pkg = packages[name]
            if pkg.update_version(latest):
                print("✓")
                updated_packages.add(name)
            else:
                print("✗")
                failed_updates.append(name)

        if updated_packages:
            print(f"\n✓ Successfully updated {len(updated_packages)} package(s)")

        if failed_updates:
            print(f"\n✗ Failed to update {len(failed_updates)} package(s): {', '.join(failed_updates)}")

        # Print build order
        print_build_order(packages, updated_packages)

    elif updates_available and args.check_only:
        # Show build order even in check-only mode
        updated_set = {name for name, _, _ in updates_available}
        print_build_order(packages, updated_set)

    return 0 if not updates_available else 1


if __name__ == "__main__":
    sys.exit(main())

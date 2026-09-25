set shell := ["bash", "-uc"]

default:
    @just --list

# Rebuild the example pages and screenshots.
examples:
    cd examples/baby-names && python3 prepare.py && python3 build.py && ./screenshot.sh

# Validate the plugin manifest and justfile formatting
lint:
    jq empty plugin/.claude-plugin/plugin.json
    just --fmt --check --unstable

# Create a release: just release [patch|minor|major]
release segment="patch":
    #!/usr/bin/env bash
    set -euo pipefail
    manifest="plugin/.claude-plugin/plugin.json"
    if [ -n "$(git status --porcelain)" ]; then echo "Working tree not clean"; exit 1; fi
    # No tags yet: start from the manifest so the first tag never goes backwards.
    latest=$(git describe --tags --abbrev=0 2>/dev/null || echo "v$(jq -r .version "$manifest")")
    IFS='.' read -r major minor patch <<< "${latest#v}"
    case "{{ segment }}" in
      major) major=$((major + 1)); minor=0; patch=0 ;;
      minor) minor=$((minor + 1)); patch=0 ;;
      patch) patch=$((patch + 1)) ;;
      *) echo "Usage: just release [patch|minor|major]"; exit 1 ;;
    esac
    new="v${major}.${minor}.${patch}"
    bare="${new#v}"
    jq --arg v "$bare" '.version = $v' "$manifest" > "${manifest}.tmp" && mv "${manifest}.tmp" "$manifest"
    git add "$manifest"
    git commit -m "release: bump version to ${bare}"
    echo "Tagging ${latest} -> ${new}"
    git tag -a "$new" -m "Release ${new}"
    git push origin HEAD --follow-tags
    echo "Released ${new}"

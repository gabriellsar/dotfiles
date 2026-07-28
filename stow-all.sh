#!/usr/bin/env bash
# Stow every package folder in this dotfiles repo.
#
# Usage: ./stow-all.sh

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for pkg_dir in "$script_dir"/*/; do
    pkg="$(basename "$pkg_dir")"
    [[ "$pkg" == .* ]] && continue
    echo "Stowing '$pkg'"
    stow -d "$script_dir" -t "$HOME" "$pkg"
done

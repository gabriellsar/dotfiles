#!/usr/bin/env bash
# Create stow-compatible package folders for the given config names and
# move the existing configs from ~/.config into them.
#
# Usage: ./setup-stow.sh nvim waybar tmux ...

set -euo pipefail

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <name> [name ...]" >&2
    exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

stow_existing() {
    for pkg_dir in "$script_dir"/*/; do
        pkg="$(basename "$pkg_dir")"
        [[ "$pkg" == .* ]] && continue
        echo "Stowing '$pkg'"
        (cd "$script_dir" && stow "$pkg")
    done
}

for name in "$@"; do
    src="$HOME/.config/$name"
    dest_dir="$script_dir/$name/.config"
    dest="$dest_dir/$name"

    if [[ ! -e "$src" ]]; then
        echo "Skipping '$name': $src does not exist" >&2
        continue
    fi

    if [[ -e "$dest" ]]; then
        echo "Skipping '$name': $dest already exists" >&2
        continue
    fi

    mkdir -p "$dest_dir"
    mv "$src" "$dest"
    echo "Moved $src -> $dest"
done

stow_existing

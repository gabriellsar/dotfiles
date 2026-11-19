#!/usr/bin/env python3
"""Gera o tema de cursor Xcursor "gabriel-s-cursors" a partir de fun24.py.

Uso: python3 .tools/cursor/build.py   (na raiz do repositório dotfiles)
Saída: icons/.local/share/icons/gabriel-s-cursors/

Cada cursor é desenhado num grid 24x24 e exportado em 24px (1x) e 48px (2x,
cada pixel vira 2x2), então fica nítido nas duas escalas. Os cursores
animados (espera e em progresso) têm 2 quadros.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fun24 as f  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(ROOT, 'icons', '.local', 'share', 'icons', 'gabriel-s-cursors')
SIZES = (24, 48)
DELAY = 800  # ms por quadro

# Nomes que apps X11, GTK e Qt pedem, por forma.
ALIASES = {
    'default': ['left_ptr', 'arrow', 'top_left_arrow', 'left-arrow'],
    'pointer': ['hand2', 'hand1', 'hand', 'pointing_hand', 'openhand-link'],
    'text': ['xterm', 'ibeam'],
    'vertical-text': [],
    'wait': ['watch'],
    'progress': ['left_ptr_watch', 'half-busy'],
    'help': ['question_arrow', 'whats_this', 'dnd-ask', 'left_ptr_help'],
    'not-allowed': ['crossed_circle', 'forbidden', 'no-drop', 'dnd-no-drop', 'circle', 'pirate', 'X_cursor'],
    'crosshair': ['cross', 'tcross', 'cross_reverse', 'diamond_cross', 'color-picker'],
    'cell': ['plus'],
    'move': ['fleur', 'all-scroll', 'size_all', 'dnd-move', 'pointer-move'],
    'grab': ['openhand', 'hand-grab'],
    'grabbing': ['closedhand', 'dnd-none', 'hand-grabbing'],
    'ew-resize': ['sb_h_double_arrow', 'h_double_arrow', 'size_hor', 'e-resize', 'w-resize', 'left_side', 'right_side'],
    'ns-resize': ['sb_v_double_arrow', 'v_double_arrow', 'size_ver', 'n-resize', 's-resize', 'top_side', 'bottom_side', 'double_arrow'],
    'nwse-resize': ['bd_double_arrow', 'size_fdiag', 'nw-resize', 'se-resize', 'top_left_corner', 'bottom_right_corner'],
    'nesw-resize': ['fd_double_arrow', 'size_bdiag', 'ne-resize', 'sw-resize', 'top_right_corner', 'bottom_left_corner'],
    'col-resize': ['split_h'],
    'row-resize': ['split_v'],
    'zoom-in': [],
    'zoom-out': [],
    'copy': ['dnd-copy'],
    'alias': ['link', 'dnd-link'],
    'context-menu': [],
}


def frames(cur):
    """Lista de quadros (dict pixel->cor) do cursor."""
    base = f.finish(cur['g'])
    extra = {cls: (cells, col) for cls, cells, col in cur['g'].extra}
    if cur['name'] == 'wait':
        out = []
        for cls in ('eyeA', 'eyeB'):
            fr = dict(base)
            cells, col = extra[cls]
            for p in cells:
                fr[p] = col
            out.append(fr)
        return out
    if cur['name'] == 'progress':
        closed = dict(base)
        cells, col = extra['eyeB']
        for p in cells:
            closed[p] = col
        return [base, base, base, closed]
    return [base]


def argb(hexcol):
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (1, 3, 5))
    return (0xFF << 24) | (r << 16) | (g << 8) | b


def image(pix, size):
    k = size // 24
    data = [0] * (size * size)
    for (x, y), col in pix.items():
        v = argb(col)
        for dy in range(k):
            for dx in range(k):
                data[(y * k + dy) * size + x * k + dx] = v
    return data


def write_xcursor(path, cur):
    chunks = []
    frs = frames(cur)
    hx, hy = cur['hot']
    for size in SIZES:
        k = size // 24
        for fr in frs:
            delay = DELAY if len(frs) > 1 else 0
            px = image(fr, size)
            header = struct.pack('<9I', 36, 0xFFFD0002, size, 1, size, size, hx * k, hy * k, delay)
            chunks.append((size, header + struct.pack('<%dI' % len(px), *px)))
    ntoc = len(chunks)
    pos = 16 + ntoc * 12
    toc = b''
    body = b''
    for size, chunk in chunks:
        toc += struct.pack('<3I', 0xFFFD0002, size, pos + len(body))
        body += chunk
    with open(path, 'wb') as fh:
        fh.write(b'Xcur' + struct.pack('<3I', 16, 0x10000, ntoc) + toc + body)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    cdir = os.path.join(OUT, 'cursors')
    os.makedirs(cdir)
    with open(os.path.join(OUT, 'index.theme'), 'w') as fh:
        fh.write('[Icon Theme]\nName=gabriel-s-cursors\nComment=Cursor divertido do design system gabriel.s (pixel art 24x24)\nInherits=Adwaita\n')
    for cur in f.build():
        name = cur['name']
        write_xcursor(os.path.join(cdir, name), cur)
        for alias in [cur['x']] + ALIASES.get(name, []):
            link = os.path.join(cdir, alias)
            if alias != name and not os.path.lexists(link):
                os.symlink(name, link)
    print('ok:', OUT)


if __name__ == '__main__':
    main()

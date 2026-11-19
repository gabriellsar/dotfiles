#!/usr/bin/env python3
"""Gera o plano de fundo "heightmap" do tema gabriel-s.

Campo de pontos em grade alternada cobrindo a tela inteira. A altura do
relevo define o tamanho de cada ponto, e as curvas de nível aparecem em
verde-água.

Uso: python3 .tools/wallpaper/heightmap.py [seed]
Saída: omarchy/.config/omarchy/themes/gabriel-s/backgrounds/1-heightmap.png
       e preview.png (seletor de temas)
"""
import math
import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
THEME = os.path.join(ROOT, 'omarchy', '.config', 'omarchy', 'themes', 'gabriel-s')
W, H = 3840, 2160
SS = 2  # supersampling para bordas suaves
BG = (0x0a, 0x0c, 0x0d)
ACCENT = (0x7c, 0xf0, 0xd4)
GAP = 56          # espaço entre pontos em 4K (28px em 1080p)
LEVELS = 7        # número de curvas de nível
seed = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0x2A


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def rnd_phases(seed):
    s = seed * 9301 + 49297
    out = []
    for _ in range(4):
        s = (s * 9301 + 49297) % 233280
        out.append(s / 233280 * 6.28)
    return out


p = rnd_phases(seed)


def field(x, y):
    # coordenadas na escala 1080p, como no design
    x, y = x / 2, y / 2
    v = (0.45 * math.sin(x * 0.0042 + p[0]) * math.cos(y * 0.0051 + p[1])
         + 0.35 * math.sin((x + y) * 0.0027 + p[2])
         + 0.2 * math.cos(x * 0.0093 - y * 0.0068 + p[3]))
    return (v + 1) / 2


img = Image.new('RGB', (W * SS, H * SS), BG)
d = ImageDraw.Draw(img)
rows = H // GAP + 2
cols = W // GAP + 2
for j in range(rows):
    for i in range(cols):
        x = GAP / 2 + i * GAP + (GAP / 2 if j % 2 else 0)
        y = GAP / 2 + j * GAP
        if x > W or y > H:
            continue
        v = field(x, y)
        ph = (v * LEVELS) % 1
        on_line = ph < 0.1 or ph > 0.9
        col = mix(BG, ACCENT, 0.55 if on_line else 0.09)
        r = (1.1 + v) * 2 * SS
        cx, cy = x * SS, y * SS
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

out = img.resize((W, H), Image.LANCZOS)
os.makedirs(os.path.join(THEME, 'backgrounds'), exist_ok=True)
out.save(os.path.join(THEME, 'backgrounds', '1-heightmap.png'), optimize=True)
out.resize((1280, 720), Image.LANCZOS).save(os.path.join(THEME, 'preview.png'), optimize=True)
print('ok', os.path.join(THEME, 'backgrounds', '1-heightmap.png'))

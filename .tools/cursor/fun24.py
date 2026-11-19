"""Cursor gabriel.s · Divertido — pixel art nativo 24x24 (1px = 1px em 1x).

Cada forma é desenhada à mão em coordenadas inteiras. O contorno escuro de
1px é gerado em 4-vizinhança (degrau limpo, sem engrossar diagonais).
"""
K = '#0a0c0d'
MINT, BLUE, AMBER, VIOLET, WHITE, CORAL = '#7cf0d4', '#a8c5ff', '#ffb454', '#c9a8ff', '#f4fbfb', '#ff8a6b'
DEEP = {MINT: '#12302b', CORAL: '#3a1d16', BLUE: '#1a2638'}
LIGHT = {MINT: '#c8fbef', BLUE: '#dce8ff', AMBER: '#ffd9a3', VIOLET: '#e6d6ff', CORAL: '#ffc2b0', WHITE: '#ffffff'}
N = 24


class G:
    def __init__(self):
        self.p = {}      # (x,y) -> cor
        self.extra = []  # (classe, [(x,y)], cor)

    def px(self, x, y, c):
        if 0 <= x < N and 0 <= y < N:
            self.p[(x, y)] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def clear(self, x, y):
        self.p.pop((x, y), None)

    def rows(self, ox, oy, rows, cmap):
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch in cmap:
                    if cmap[ch] is None:
                        self.clear(ox + x, oy + y)
                    else:
                        self.px(ox + x, oy + y, cmap[ch])


# ---------------- formas base ----------------
ARROW_FILL = {  # seta clássica: linha -> intervalos de x (fill)
    2: [(2, 2)], 3: [(2, 3)], 4: [(2, 4)], 5: [(2, 5)], 6: [(2, 6)], 7: [(2, 7)], 8: [(2, 8)], 9: [(2, 9)], 10: [(2, 10)],
    11: [(2, 6)], 12: [(2, 3), (5, 6)], 13: [(2, 2), (6, 7)], 14: [(6, 7)], 15: [(7, 8)], 16: [(7, 8)],
}


def arrow(g, c=MINT):
    for y, spans in ARROW_FILL.items():
        for a, b in spans:
            g.rect(a, y, b, y, c)


def badge(g, glyph, box):
    # selo 9x9 em (13..21, 13..21), símbolo 7x7 em escuro
    g.rect(13, 13, 21, 21, box)
    for y, row in enumerate(glyph):
        for x, ch in enumerate(row):
            if ch == 'K':
                g.px(14 + x, 14 + y, K)


def big_face(g, rows, color, deep, eye_cls=None, eye_color=WHITE):
    """Rosto 7x7 ampliado 2x, ocupando 5..18."""
    eyes = []
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            x0, y0 = 5 + x * 2, 5 + y * 2
            if ch == 'X':
                g.rect(x0, y0, x0 + 1, y0 + 1, color)
            elif ch == 'E':
                g.rect(x0, y0, x0 + 1, y0 + 1, deep)
                eyes.append((x0, y0))
            elif 1 <= x <= 5 and 1 <= y <= 5:
                g.rect(x0, y0, x0 + 1, y0 + 1, deep)
    return eyes


def h_arrow(g, x0, x1, y, c, heads=(True, True)):
    """Seta dupla horizontal: haste 2px em y..y+1, pontas de 45° com 4 degraus."""
    g.rect(x0 + 3, y, x1 - 3, y + 1, c)
    for i in range(4):
        if heads[0]:
            g.rect(x0 + i, y - i, x0 + i, y + 1 + i, c)
        if heads[1]:
            g.rect(x1 - i, y - i, x1 - i, y + 1 + i, c)


def transpose(g):
    t = G()
    for (x, y), c in g.p.items():
        t.p[(y, x)] = c
    t.extra = [(cls, [(y, x) for x, y in cells], col) for cls, cells, col in g.extra]
    return t


def mirror_x(g):
    t = G()
    for (x, y), c in g.p.items():
        t.p[(N - 1 - x, y)] = c
    return t


# ---------------- os 24 cursores ----------------
def build():
    C = []

    def add(name, xname, label, hot, g):
        C.append(dict(name=name, x=xname, label=label, hot=hot, g=g))

    g = G(); arrow(g); add('default', 'left_ptr', 'Padrão', (1, 1), g)

    # mão apontando: indicador reto, três dedos dobrados, polegar em degrau
    g = G(); c = WHITE
    g.rect(8, 2, 10, 13, c)                                          # indicador
    g.rect(12, 8, 14, 13, c)                                         # médio
    g.rect(16, 9, 18, 13, c)                                         # anelar
    g.rect(20, 10, 21, 13, c)                                        # mínimo
    g.rect(8, 13, 21, 19, c)                                          # palma
    g.rect(5, 12, 7, 12, c); g.rect(4, 13, 7, 14, c); g.rect(5, 15, 7, 16, c); g.rect(6, 17, 7, 17, c)  # polegar
    g.rect(9, 20, 20, 20, c); g.rect(10, 21, 19, 21, c)               # base
    g.clear(21, 19)
    add('pointer', 'hand2', 'Link', (9, 2), g)

    g = G(); c = VIOLET
    g.rect(8, 2, 15, 3, c); g.rect(11, 4, 12, 19, c); g.rect(8, 20, 15, 21, c)
    add('text', 'xterm', 'Texto', (11, 11), g)
    add('vertical-text', 'vertical-text', 'Texto vertical', (11, 11), transpose(g))

    # espera: rosto grande, olhos olham para os lados (2 quadros)
    g = G()
    eyes = big_face(g, ['.XXXXX.', 'X.....X', 'X.E.E.X', 'X.....X', 'X.XXX.X', 'X.....X', '.XXXXX.'], MINT, DEEP[MINT])
    g.extra = [('eyeA', [(x, y + dy) for x, y in eyes for dy in (0, 1)], WHITE), ('eyeB', [(x + 1, y + dy) for x, y in eyes for dy in (0, 1)], WHITE)]
    add('wait', 'watch', 'Espera', (11, 11), g)

    # progresso: seta + mini rosto que pisca
    g = G(); arrow(g)
    g.rows(13, 13, ['XXXXXXXXX', 'XdddddddX', 'XddEdEddX', 'XddEdEddX', 'XdddddddX', 'XdEEEEEdX', 'XdddddddX', 'XdddddddX', 'XXXXXXXXX'], {'X': MINT, 'd': DEEP[MINT], 'E': WHITE})
    g.extra = [('eyeB', [(16, 15), (16, 16), (18, 15), (18, 16)], DEEP[MINT])]
    add('progress', 'left_ptr_watch', 'Em progresso', (1, 1), g)

    g = G(); arrow(g); badge(g, ['..KKK..', '.KK.KK.', '....KK.', '...KK..', '...KK..', '.......', '...KK..'], BLUE)
    add('help', 'question_arrow', 'Ajuda', (1, 1), g)

    # bloqueado: ciclope com olho em X
    g = G()
    big_face(g, ['.XXXXX.', 'X.....X', 'X.E.E.X', 'X..E..X', 'X.E.E.X', 'X.....X', '.XXXXX.'], CORAL, DEEP[CORAL])
    # olho em X branco, 1px, sobre o fundo escuro
    for i in range(6):
        g.px(9 + i, 9 + i, WHITE); g.px(14 - i, 9 + i, WHITE)
        if i < 5:
            g.px(10 + i, 9 + i, WHITE); g.px(13 - i, 9 + i, WHITE)
    add('not-allowed', 'crossed_circle', 'Bloqueado', (11, 11), g)

    g = G(); c = AMBER
    g.rect(11, 1, 12, 7, c); g.rect(11, 16, 12, 22, c); g.rect(1, 11, 7, 12, c); g.rect(16, 11, 22, 12, c)
    g.rect(11, 11, 12, 12, MINT)
    add('crosshair', 'cross', 'Mira', (11, 11), g)

    g = G(); c = BLUE
    g.rect(10, 3, 13, 20, c); g.rect(3, 10, 20, 13, c)
    add('cell', 'plus', 'Célula', (11, 11), g)

    g = G(); c = VIOLET
    h_arrow(g, 1, 22, 11, c); t = transpose(G());
    v = G(); h_arrow(v, 1, 22, 11, c); v = transpose(v)
    g.p.update(v.p)
    add('move', 'fleur', 'Mover', (11, 11), g)

    # mão aberta: 4 dedos separados por 1px de contorno + polegar
    g = G(); c = AMBER
    for x0, top in [(6, 4), (10, 2), (14, 3), (18, 6)]:
        w = 2 if x0 == 18 else 3
        g.rect(x0, top, x0 + w - 1, 12, c)
    g.rect(6, 12, 19, 19, c)
    g.rect(3, 11, 5, 11, c); g.rect(2, 12, 5, 13, c); g.rect(3, 14, 5, 15, c); g.rect(4, 16, 5, 16, c)
    g.rect(7, 20, 18, 20, c); g.rect(8, 21, 17, 21, c)
    add('grab', 'openhand', 'Pegar', (11, 11), g)

    # mão fechada: nós dos dedos
    g = G(); c = AMBER
    for x0 in (6, 10, 14):
        g.rect(x0, 8, x0 + 2, 11, c)
    g.rect(18, 9, 19, 11, c)
    g.rect(6, 11, 19, 19, c)
    g.rect(3, 12, 5, 15, c)
    g.rect(7, 20, 18, 20, c); g.rect(8, 21, 17, 21, c)
    add('grabbing', 'closedhand', 'Arrastando', (11, 12), g)

    g = G(); h_arrow(g, 1, 22, 11, MINT); add('ew-resize', 'sb_h_double_arrow', 'Redim. ↔', (11, 11), g)
    g = G(); h_arrow(g, 1, 22, 11, MINT); add('ns-resize', 'sb_v_double_arrow', 'Redim. ↕', (11, 11), transpose(g))

    def diag(c):
        g = G()
        for t in range(6, 17):
            g.px(t, t, c); g.px(t + 1, t, c); g.px(t, t + 1, c)
        for y in range(2, 9):
            for x in range(2, 9):
                if x + y <= 10:
                    g.px(x, y, c)
                    g.px(N - 1 - x, N - 1 - y, c)
        return g
    add('nwse-resize', 'bd_double_arrow', 'Redim. ⤡', (11, 11), diag(MINT))
    add('nesw-resize', 'fd_double_arrow', 'Redim. ⤢', (12, 11), mirror_x(diag(MINT)))

    g = G(); c = BLUE
    g.rect(11, 3, 12, 20, c)
    h_arrow(g, 1, 12, 11, c, heads=(True, False))
    h_arrow(g, 11, 22, 11, c, heads=(False, True))
    for y in (11, 12):
        g.clear(9, y); g.clear(14, y)
    add('col-resize', 'split_h', 'Coluna', (11, 11), g)
    add('row-resize', 'split_v', 'Linha', (11, 11), transpose(g))

    def lens(plus):
        g = G()
        cx = cy = 9.5
        for y in range(0, 20):
            for x in range(0, 20):
                d = ((x + 0.5 - cx - 0.5) ** 2 + (y + 0.5 - cy - 0.5) ** 2) ** 0.5
                if 5.0 <= d <= 7.0:
                    g.px(x, y, WHITE)
                elif d < 5.0:
                    g.px(x, y, DEEP[MINT])
        for t in range(15, 21):
            g.rect(t, t, t + 1, t + 1, WHITE)
        g.rect(7, 9, 12, 10, MINT)
        if plus:
            g.rect(9, 7, 10, 12, MINT)
        return g
    add('zoom-in', 'zoom-in', 'Zoom +', (9, 9), lens(True))
    add('zoom-out', 'zoom-out', 'Zoom −', (9, 9), lens(False))

    g = G(); arrow(g); badge(g, ['.......', '...K...', '...K...', '.KKKKK.', '...K...', '...K...', '.......'], AMBER); add('copy', 'copy', 'Copiar', (1, 1), g)
    g = G(); arrow(g); badge(g, ['.......', '..KKKK.', '....KK.', '...K.K.', '..K..K.', '.K.....', '.......'], BLUE); add('alias', 'link', 'Atalho', (1, 1), g)
    g = G(); arrow(g); badge(g, ['.......', '.KKKKK.', '.......', '.KKKKK.', '.......', '.KKKKK.', '.......'], WHITE); add('context-menu', 'context-menu', 'Menu de contexto', (1, 1), g)
    return C


def finish(g):
    """Contorno escuro de 1px em 4-vizinhança, fechando os degraus diagonais."""
    fill = dict(g.p)
    out = dict(fill)
    for (x, y), c in fill.items():
        if c == K:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q not in fill and 0 <= q[0] < N and 0 <= q[1] < N:
                out[q] = K
    # cantos externos (diagonais) só onde dois vizinhos ortogonais já são contorno: fecha o degrau
    for (x, y), c in list(fill.items()):
        if c == K:
            continue
        for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            q = (x + dx, y + dy)
            if q not in out and out.get((x + dx, y)) == K and out.get((x, y + dy)) == K and 0 <= q[0] < N and 0 <= q[1] < N:
                out[q] = K
    final = dict(out)
    for (x, y), c in out.items():
        pass  # brilho desligado: em 24px ele vira ruído
    return final


def layers(cur):
    pix = finish(cur['g'])
    by = {}
    for (x, y), c in sorted(pix.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        by.setdefault(c, []).append((x, y))
    L = []
    for c in sorted(by, key=lambda k: 0 if k == K else 1):
        d = runs(by[c])
        L.append(dict(d=d, fill=c, cls=''))
    for cls, cells, col in cur['g'].extra:
        if cells:
            L.append(dict(d=runs(cells), fill=col, cls=cls))
    return L


def runs(cells):
    rows = {}
    for x, y in cells:
        rows.setdefault(y, []).append(x)
    d = []
    for y in sorted(rows):
        xs = sorted(set(rows[y]))
        start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x
                continue
            d.append('M%d %dh%dv1h-%dz' % (start, y, prev - start + 1, prev - start + 1))
            if x is not None:
                start = prev = x
    return ''.join(d)


def svg(cur, size=24):
    parts = ''.join('<path%s d="%s" fill="%s"/>' % ((' class="%s"' % l['cls']) if l['cls'] else '', l['d'], l['fill']) for l in layers(cur))
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 24 24" shape-rendering="crispEdges">%s</svg>' % (size, size, parts)

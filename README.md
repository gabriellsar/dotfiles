# dotfiles

Configurações pessoais para o **Omarchy 4 (Quattro)**, gerenciadas com [GNU Stow](https://www.gnu.org/software/stow/). Cada pasta da raiz é um pacote que espelha o `$HOME`.

```sh
./stow-all.sh          # aplica todos os pacotes
stow ghostty vscode    # ou só alguns
```

O stow não sobrescreve arquivos que já existem. Se o Omarchy já criou algum (por exemplo `~/.config/Code/User/settings.json`), mova-o antes.

## Pacotes

| Pacote | O que tem |
| --- | --- |
| `omarchy` | Tema `gabriel-s` (design system gabriel.s) em `~/.config/omarchy/themes/`, no formato de cores do Quattro |
| `vscode` | `settings.json` do VS Code (o tema de cores vem do tema do Omarchy) |
| `ghostty`, `alacritty`, `kitty` | Terminais. As cores vêm de `~/.local/state/omarchy/current/theme/` |
| `herdr` | Atalhos do herdr no estilo do tmux. O tema segue o terminal |
| `icons` | Tema de cursor `gabriel-s-cursors` (Xcursor, 24 e 48 px), gerado por `.tools/cursor/build.py` |
| `tmux`, `starship`, `zshrc`, `nvim` | Shell, prompt e editor |

O Quattro trocou Waybar, Walker, Mako e SwayOSD pelo shell em Quickshell. A barra, o dock e os plugins ficam em `~/.config/omarchy/shell.json` e `~/.config/omarchy/plugins/`. As personalizações do Hyprland, já em Lua, estão no repositório [omarchy-supplement](https://github.com/gabriellsar/omarchy-supplement).

## Cursor

O tema `gabriel-s-cursors` é pixel art 24×24 desenhado em `.tools/cursor/fun24.py`. Para regenerar depois de mudar um desenho, rode `python3 .tools/cursor/build.py`.

Para testar sem mudar nada de forma permanente:

```sh
stow icons
hyprctl setcursor gabriel-s-cursors 24     # vale até o próximo login
```

Para manter, adicione ao Hyprland (por exemplo, no `overrides.lua` do omarchy-supplement):

```lua
hl.env("XCURSOR_THEME", "gabriel-s-cursors")
```

E aplique também nos apps GTK com `gsettings set org.gnome.desktop.interface cursor-theme gabriel-s-cursors`.

## `.legacy/`

Configs de X11 de antes do Omarchy (i3, polybar, rofi, wofi, Xresources), guardadas para consulta. O `stow-all.sh` ignora pastas que começam com ponto, então nem `.legacy/` nem `.tools/` são aplicadas.

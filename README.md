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
| `omarchy` | Temas em `~/.config/omarchy/themes/`: `gabriel-s` (design system gabriel.s) e `island-mocha`, ambos no formato de cores do Quattro |
| `backgrounds` | Planos de fundo do tema island-mocha |
| `vscode` | `settings.json` do VS Code (o tema de cores vem do tema do Omarchy) |
| `ghostty`, `alacritty`, `kitty` | Terminais. As cores vêm de `~/.local/state/omarchy/current/theme/` |
| `herdr` | Atalhos do herdr no estilo do tmux. O tema segue o terminal |
| `tmux`, `starship`, `zshrc`, `nvim` | Shell, prompt e editor |

O Quattro trocou Waybar, Walker, Mako e SwayOSD pelo shell em Quickshell. A barra, o dock e os plugins ficam em `~/.config/omarchy/shell.json` e `~/.config/omarchy/plugins/`. As personalizações do Hyprland, já em Lua, estão no repositório [omarchy-supplement](https://github.com/gabriellsar/omarchy-supplement).

## `.legacy/`

Configs de X11 de antes do Omarchy (i3, polybar, rofi, wofi, Xresources), guardadas para consulta. O `stow-all.sh` ignora pastas que começam com ponto, então elas não são aplicadas.

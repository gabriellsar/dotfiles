# gabriel.s — tema Omarchy Quattro

Tema pessoal gerado a partir do design system gabriel.s (escuro, um acento frio `#7cf0d4`, um sinal quente `#ff8a6b`).

## Arquivos

- `colors.toml` — paleta no formato do Quattro. O Omarchy gera a partir dela o terminal, o btop, o Chromium, o Hyprland, o Neovim, o Helix, o Obsidian e o shell inteiro (barra, menu, notificações, OSD e tela de bloqueio).
- `vscode-theme.json` — tema do VS Code feito à mão. Como o tema já traz este arquivo, o Omarchy não gera o seu a partir do template. Ao trocar para este tema, o `omarchy-theme-set-vscode` instala a extensão local "Omarchy" com ele e define `workbench.colorTheme`.

## Instalar

1. `stow omarchy vscode` a partir da raiz do repositório dotfiles. Se `~/.config/Code/User/settings.json` já existir, mova-o antes, porque o stow não sobrescreve arquivos.
2. `omarchy-pkg-add otf-geist-mono-nerd` para a fonte Geist Mono com os glifos Nerd Font que a barra e o terminal usam.
3. Escolha o tema em _Appearance › Theme_ (Super + Ctrl + T) ou rode `omarchy theme set gabriel-s`.

Ainda faltam os planos de fundo (`backgrounds/`) e as imagens `preview.png` e `unlock.png`.

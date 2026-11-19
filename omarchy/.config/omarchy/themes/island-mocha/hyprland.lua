-- Island Mocha: bordas, espaçamentos e efeitos (antes em hyprland.conf).
local active_border_color = "rgb(4a86a8)"
local inactive_border_color = "rgba(3d506455)"

hl.config({
  general = {
    gaps_in = 6,
    gaps_out = 12,
    col = {
      active_border = active_border_color,
      inactive_border = inactive_border_color,
    },
  },

  group = {
    col = {
      border_active = active_border_color,
      border_inactive = inactive_border_color,
    },
  },

  decoration = {
    rounding = 6,

    shadow = {
      enabled = true,
      range = 6,
      render_power = 3,
      color = "rgba(6fa8c966)",
      color_inactive = "rgba(10192b2a)",
    },

    blur = {
      enabled = true,
      size = 3,
      passes = 2,
      special = true,
      brightness = 0.65,
      contrast = 0.8,
    },
  },
})

hl.animation({ leaf = "workspaces", enabled = true, speed = 4, bezier = "easeOutQuint", style = "slide" })

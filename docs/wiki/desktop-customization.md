---
title: "Desktop Customization — Hyprland Ricing"
created: 2026-04-24
tags: [desktop, hyprland, conky, numogram]
status: active
---

# Desktop Customization — Hyprland Ricing

*Created: 2026-04-19. Numogram oracle overlay + random wallpaper cycling.*

## Components

### Conky — Numogram Oracle Quotes
- Config: `~/.config/conky/conky.conf`
- Quote file: `~/.config/conky/numogram-quotes.txt` (86 entries, one per line)
- Rotation: every 5 minutes (`update_interval = 300`)
- Position: bottom-left, Hack font, cyan "☿ NUMOGRAM ORACLE" header
- Metadata line: current zone (time-based) + gate number (HHMM)
- Wayland: `out_to_wayland = true`, `own_window_type = 'desktop'`
- Known issue: "unknown wayland session" warning — cosmetic, still renders

### Hyprpaper v0.8 — Random Wallpaper
- Config: `~/.config/hypr/hyprpaper.conf` (auto-generated)
- Picker script: `~/.config/hypr/numogram-wallpaper-picker.sh`
- Wallpaper pool: `~/Pictures/Wall/` (9 images)
- fit_mode: `contain`
- Monitor: `HDMI-A-1` (BenQ GL2450H, 1920x1080)
- v0.8+ block syntax required:
```
wallpaper {
    monitor = HDMI-A-1
    path = /path/to/image.jpg
    fit_mode = contain
}
```

### Hyprland Config
- Splash disabled: `disable_splash_rendering = true` in `misc {}`
- Autostart: `exec-once = ~/.config/hypr/numogram-wallpaper-picker.sh && waybar & hyprpaper & hyprwave & conky -c ~/.config/conky/conky.conf`

## Future Work

### Zone-Themed Wallpapers
The user wants 10 wallpapers — one per numogram zone. Each should evoke the zone's character:
- Zone 0 (Void): black, formless, the map before the map
- Zone 1 (Surge): first movement, electric, directional
- Zone 6 (The Hinge): rotational, bifurcating
- Zone 9 (Plex): tangled currents, dense, maximal
- etc.

Generation options:
- Stable Diffusion with zone-specific prompts
- Algorithmic art (p5.js/manim) — numogram topology as generative source
- Compositing existing images with zone symbols/glyphs

### Other Ideas
- Zone-based wallpaper selection (current zone from conky → wallpaper matches)
- Hyprlock integration (quote on lock screen)
- Time-of-day cycling (dawn=low zones, midnight=high zones)
- Sound integration (numogram-voices ambient tied to wallpaper/zone)

## File Manifest
```
~/.config/conky/conky.conf
~/.config/conky/numogram-quotes.txt
~/.config/hypr/hyprpaper.conf
~/.config/hypr/numogram-wallpaper-picker.sh
~/.config/hypr/hyprland.conf (lines 49, 199-202)
~/Pictures/Wall/ (9 wallpapers)
```

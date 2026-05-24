# Compendium &mdash; Skills Panel for Claude Code

A gallery-grade, warm-gold-on-obsidian skills panel that turns your Claude Code skill library into a browsable, searchable, organized experience.

![screenshot](https://via.placeholder.com/800x500/1a1816/c9a96e?text=Compendium+Screenshot)

## Features

- **18 Auto-Categorized Groups** &mdash; 116+ skills sorted into Product, Engineering, Design, DevOps, AI/ML, and more
- **Spotlight Search (Ctrl+K)** &mdash; Instant fuzzy search across all skills, macOS Spotlight-style
- **Auto-Discovery** &mdash; New skills installed to `~/.claude/skills/` appear automatically in the panel, categorized by keyword matching
- **Favorites** &mdash; Star skills for quick access. Persisted in localStorage
- **The Vault** &mdash; Archive rarely-used skills to a backup directory. Restore with one click
- **Standalone Vertical Launcher** &mdash; Detached 48px icon strip window that lives outside your browser
- **Density Toggle** &mdash; Switch between gallery cards and compact list view
- **Gallery Design System** &mdash; Warm dark palette, gold+copper accents, Playfair Display serif headings, grain texture, spring animations

## Quick Start

```bash
# Clone
git clone https://github.com/your-username/compendium.git
cd compendium

# Start the server
python3 server.py

# Open in browser
# http://127.0.0.1:8765
```

The panel automatically reads skills from `~/.claude/skills/`. You can override this:

```bash
# Custom skill directories
export COMPENDIUM_SKILLS_DIR=/path/to/skills
export COMPENDIUM_BACKUP_DIR=/path/to/backup
python3 server.py
```

## Architecture

```
compendium/
  server.py        # Python HTTP server + REST API (port 8765)
  index.html       # Main panel UI (vanilla HTML/CSS/JS, zero dependencies)
  vertical.html    # Standalone vertical launcher window
  plugin.json      # Claude Code Plugin manifest
```

**API Endpoints:**

| Endpoint | Description |
|----------|-------------|
| `GET /api/stats` | All skills with auto-detected descriptions |
| `GET /api/backup` | Archived (vault) skills |
| `GET /api/backup-skill?skill=name` | Move skill to vault |
| `GET /api/restore-backup?skill=name` | Restore from vault |
| `GET /api/launch-vertical` | Open standalone vertical window |

## Design System

| Token | Value |
|-------|-------|
| Background | `#0a0908` (warm obsidian) |
| Surface | `#131211` → `#1a1816` |
| Accent | `#c9a96e` (gold), `#c17e60` (copper) |
| Typography | Playfair Display (headings), JetBrains Mono (commands), system sans (body) |
| Motion | 350ms spring curves, grain texture overlay, warm radial ambient glow |

## License

MIT

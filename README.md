# Clavis &mdash; The Key to Your Claude Code Skills

A gallery-grade, warm-gold-on-obsidian skills panel that turns your Claude Code skill library into a browsable, searchable, organized experience.

<p align="center">
  <img src="https://via.placeholder.com/800x450/1a1816/c9a96e?text=Compendium+Screenshot" alt="Compendium Screenshot" width="800">
</p>

---

## Features

| Feature | Description |
|---------|-------------|
| **18 Auto-Categorized Groups** | 116+ skills sorted into Product, Engineering, Design, DevOps, AI/ML, and more. New skills auto-detected and placed by keyword matching |
| **Spotlight Search** `Ctrl+K` | Instant fuzzy search across all skills. Arrow keys to navigate, Enter to copy. macOS Spotlight-style floating overlay |
| **Auto-Discovery** | Install a new skill to `~/.claude/skills/` → appears in Compendium automatically on next refresh. No manual editing |
| **Favorites** | Star skills for quick access. Click the star on any card or right-click → Favorite. Persisted in localStorage |
| **The Vault** | Right-click → "Move to Vault" archives rarely-used skills to `~/.claude/skills-backup/`. Click "Restore" to bring them back |
| **Standalone Vertical Launcher** | Click the popout icon → opens a detached 48px icon strip in Edge --app mode. Lives outside your browser |
| **Density Toggle** | Switch between gallery cards (comfortable) and compact single-line list. Preference saved |
| **Gallery Design** | Warm obsidian + gold/copper accents, Playfair Display headings, grain texture, 350ms spring animations |

---

## Quick Start

### Prerequisites

- Python 3.8+ (for the HTTP server)
- Claude Code installed (skills read from `~/.claude/skills/`)
- Any modern browser

### One-Command Start

```bash
git clone https://github.com/NUYoah700/clavis.git
cd clavis
python3 server.py
```

Then open **http://127.0.0.1:8765** in your browser.

### Auto-Start with Claude Code

Add this to your `~/.claude/settings.json` hooks to auto-start Compendium with every session:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "command": "cd /path/to/clavis && pythonw.exe server.py &",
            "type": "command"
          }
        ],
        "matcher": ""
      }
    ]
  }
}
```

### Custom Skill Directories

```bash
export COMPENDIUM_SKILLS_DIR=/custom/path/to/skills
export COMPENDIUM_BACKUP_DIR=/custom/path/to/backup
python3 server.py
```

---

## How to Use

### Browse Skills
Click any category icon on the left sidebar to see its skills. The sidebar expands on hover to show category names and counts.

### Search
Press **Ctrl+K** (or click the search button) to open Spotlight. Type any keyword &mdash; it searches across skill names and descriptions. Use arrow keys + Enter to pick, or click any result to copy the command.

### Copy a Skill
Click any skill card to copy its slash command to clipboard (e.g. `/brainstorm`). A toast notification confirms the copy. Paste it into Claude Code chat with Ctrl+V.

### Favorite Skills
**Method 1:** Hover over any card → click the star icon that appears in the top-right corner.

**Method 2:** Right-click any card → "Favorite".

Favorites appear in the "My Favorites" section at the top of the sidebar. Click it to see only your starred skills.

### Archive Skills (The Vault)
Have skills you rarely use? **Right-click → "Move to Vault"** archives them to `~/.claude/skills-backup/`. This saves tokens (fewer skill descriptions loaded per session).

Click "The Vault" in the sidebar to see all archived skills. Click **"Restore"** on any to bring it back.

### Auto-Discovery of New Skills
When you install new skills to `~/.claude/skills/`:
1. Compendium automatically detects them on page refresh
2. Categorizes them using 200+ keyword matching rules
3. Adds them to the appropriate category
4. Header shows "X skills (+Y auto)" indicating auto-added count

No manual editing of the panel needed.

### Compact Mode
Click the **三 (list)** icon in the header to toggle density. Compact mode shows skills as single-line rows &mdash; fit 30+ skills on screen without scrolling.

### Standalone Vertical Window
Click the **popout** icon (rightmost in header) to launch a detached 48px wide icon strip. This window:
- Lives outside your browser (Edge --app mode)
- Shows category icons in a vertical strip
- Click any icon to open a skill list popup
- Click **X** to close, or the folder icon to reopen the full panel

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+K` | Open Spotlight search |
| `↑` / `↓` | Navigate search results |
| `Enter` | Select highlighted result |
| `Esc` | Close Spotlight / context menu |
| Click card | Copy command to clipboard |
| Right-click card | Context menu (copy, favorite, vault) |

---

## Architecture

```
clavis/
  server.py        # Python HTTP server + REST API (port 8765)
  index.html       # Main panel UI — vanilla HTML/CSS/JS, zero npm, zero frameworks
  vertical.html    # Standalone vertical launcher window
  plugin.json      # Claude Code Plugin manifest
  README.md
```

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/stats` | All active skills with auto-detected descriptions |
| `GET /api/backup` | Archived (vault) skills |
| `GET /api/backup-skill?skill=name` | Move a skill from active → vault |
| `GET /api/restore-backup?skill=name` | Restore a skill from vault → active |
| `GET /api/launch-vertical` | Opens standalone vertical window via Edge --app |

---

## Design System

| Token | Value |
|-------|-------|
| Background | `#0a0908` warm obsidian |
| Surface | `#131211` → `#1a1816` layered depths |
| Accent | `#c9a96e` gold · `#c17e60` copper |
| Typography | Playfair Display italic (headings) · JetBrains Mono (commands) · System sans (body) |
| Radius | 50% (sidebar buttons) · 8px (cards) |
| Motion | 350ms spring curves · grain texture overlay · warm radial ambient glow |
| Shadows | Warm-tinted, layered depth |

---

## FAQ

**Q: Does this modify my skills?**
A: Only when you explicitly use Move to Vault or Restore. Otherwise, Compendium is read-only.

**Q: Can I use this without Claude Code?**
A: Yes. Set `COMPENDIUM_SKILLS_DIR` to any directory containing skill folders, or use it as a general-purpose bookmark launcher by editing the CATS data in `index.html`.

**Q: Why does the panel show more/less skills than I have?**
A: The header shows "X skills (Y indexed)" — X is actual directory count, Y is what the panel has categorized. Some auto-detected skills may fall into "Other".

**Q: How do I add custom skills that aren't Claude Code skills?**
A: Edit the `CATS` array in `index.html` and add your own entries. They'll persist and be searchable.

---

## License

MIT — Build your own, sell it, fork it, do whatever you want.

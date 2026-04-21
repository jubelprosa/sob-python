---
description: "Taskboard + aktive Sprints anzeigen"
---

# Tasks Overview

Erstelle eine Orientierungs-Übersicht.

## 1. Source of Truth

Lies das Taskboard des Projekts. Prüfe CLAUDE.md für den Pfad — typisch: `docs/TASKBOARD.md`, `TASKBOARD.md`, `ROADMAP.md` oder `docs/Taskboard.md`.

Für die letzten 3 Releases: `git tag --sort=-v:refname | head -3` + `git log` für Datum und Beschreibung.

## 2. Formatiere als Übersicht

```
═══════════════════════════════════════════════════════
 TASKS OVERVIEW
═══════════════════════════════════════════════════════

VERSION: v[X.Y.Z] | PHASE: [Phase aus Taskboard Header]

───────────────────────────────────────────────────────
 🔥 NEXT UP
───────────────────────────────────────────────────────
• Sprint [N]: [Name] — [Kurzbeschreibung]

───────────────────────────────────────────────────────
 📋 PLANNED
───────────────────────────────────────────────────────
• Sprint [N]: [Name] — [Kurzbeschreibung]

───────────────────────────────────────────────────────
 ⏸️  PAUSIERT
───────────────────────────────────────────────────────
• Sprint [N]: [Name] — [Grund]

───────────────────────────────────────────────────────
 ✅ RELEASES
───────────────────────────────────────────────────────
• v[X.Y.Z] — [Titel] ([Datum])
• v[X.Y.Z] — [Titel] ([Datum])
• v[X.Y.Z] — [Titel] ([Datum])

═══════════════════════════════════════════════════════
```

## 3. Regeln

- **Source of Truth ist das Taskboard** — Phase, Version, alles kommt von dort
- **Gruppierung:** NEXT UP (P0) → PLANNED (P1) → Pausiert
- **Nur offene Sprints** (ohne abgeschlossene)
- **Releases** = letzte 3 Git-Tags absteigend
- **Leere Gruppen weglassen**
- **Kompakt bleiben**: Keine Metriken, keine Commands-Liste

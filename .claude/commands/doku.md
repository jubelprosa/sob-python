---
description: "Release dokumentieren: /doku \"Titel\""
---

# Release Documentation

Dokumentiere Release: $ARGUMENTS

## Input

Flexibles Format — Version wird automatisch ermittelt:

**Mit Version:** `vX.Y.Z "Kurztitel"` (überschreibt Auto-Detect)
**Ohne Version:** `"Kurztitel"` oder einfach eine Beschreibung

**Superpowers:** Invoke Skill `verification-before-completion` before committing the release.

## Scope-Regel

**WICHTIG:** Dokumentiere NUR Änderungen, die in der aktuellen Session gemacht wurden. Andere unstaged/uncommitted Changes können von parallelen Sessions stammen — diese NICHT aufnehmen.

## Workflow

### 1. Kontext sammeln

```bash
git status --short
git diff HEAD --name-only
git log --oneline -10
git tag --sort=-v:refname | head -5
```

### 2. Version automatisch bestimmen (Semantic Versioning)

1. Hole aktuellen Tag: `git tag --sort=-v:refname | head -1`
2. Analysiere Änderungen:

| Änderungstyp | Version |
|-------------|---------|
| Neue Features, Commands, Endpoints | **Minor** (v1.2.0 → v1.3.0) |
| Bugfixes, Refactoring, Docs, Config | **Patch** (v1.2.0 → v1.2.1) |
| Breaking API/Schema Changes | **Major** (v1.2.0 → v2.0.0) |

### 3. CHANGELOG.md aktualisieren

Füge neuen Block ein:

```markdown
## [VERSION] - YYYY-MM-DD

**TITEL**

### Added|Changed|Fixed
- **Feature/Änderung** — Kurzbeschreibung
  - Detail 1
  - Detail 2
```

### 4. Taskboard aktualisieren

Lies CLAUDE.md für den Taskboard-Pfad. Aktualisiere Version und Datum im Header.

### 5. Sprint-Archivierung prüfen

Für jeden abgeschlossenen Sprint:
1. Sprint-Datei ins Archiv: `mv docs/sprints/SPRINT{N}_*.md docs/archive/sprints/`
2. Sprint-Abschnitt aus Taskboard entfernen
3. In "Abgeschlossene Sprints" Tabelle eintragen

### 6. Commit und Tag

```bash
git add CHANGELOG.md {Taskboard} {weitere Dateien}
git commit -m "docs: Release vX.Y.Z — TITEL

Co-Authored-By: Claude <noreply@anthropic.com>"
git tag -a vX.Y.Z -m "vX.Y.Z - TITEL"
```

**Frage den User vor dem Push:**
```bash
git push origin main
git push origin vX.Y.Z
```

### 7. Bestätigung

```
✅ Release vX.Y.Z dokumentiert

Änderungen: [Bereiche]
Version: vX.Y.Z ([Minor|Patch]) — [Begründung]
Commit: [SHORT_HASH]
Tag: vX.Y.Z
```

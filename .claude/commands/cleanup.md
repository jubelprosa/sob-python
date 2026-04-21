---
description: "Housekeeping: /cleanup [option]"
context: fork
---

# Cleanup

Führe Housekeeping-Tasks durch: $ARGUMENTS

## Optionen

- (leer) / `status` — Zeige Speicherverbrauch
- `docker` — Docker Cleanup (images, build cache)
- `logs` — Docker Logs truncaten
- `git` — Git Cleanup (merged branches, stale refs)
- `all` — Alles bereinigen

## Workflow

### 1. Status prüfen (immer zuerst)

```bash
# Docker (falls vorhanden)
docker system df 2>/dev/null

# Disk Usage
du -sh .git/
du -sh node_modules/ 2>/dev/null

# Git
git branch --merged main | grep -v main | wc -l
```

### 2. Docker Cleanup (wenn `docker` oder `all`)

```bash
docker image prune -f
docker builder prune -f
```

**Warnung:** Keine `--all` oder `-a` Flags ohne explizite Bestätigung!

### 3. Git Cleanup (wenn `git` oder `all`)

```bash
# Merged branches auflisten (nicht automatisch löschen!)
git branch --merged main | grep -v main
git remote prune origin --dry-run
```

### 4. Zusammenfassung

Zeige Vorher/Nachher Speicherverbrauch + was bereinigt wurde.

## Sicherheit

- **Keine destruktiven Operationen** ohne `status` vorher
- **Keine `-a/--all` Flags** bei prune ohne Bestätigung
- **Branches** nur auflisten, nicht automatisch löschen

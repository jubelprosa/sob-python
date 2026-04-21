---
description: "Projekt-Status anzeigen"
---

# Status-Check

Zeige den aktuellen Status des Projekts.

## Anweisungen

1. Lies CLAUDE.md um die Infrastruktur zu verstehen (Container, Services, URLs, DB)
2. Prüfe was relevant ist:

### Für Docker-Projekte
```bash
# Container-Status (Projektname aus CLAUDE.md)
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -i "PROJEKTNAME"
```

### Für Web-Services
```bash
# Erreichbarkeit prüfen (URLs aus CLAUDE.md)
curl -s -o /dev/null -w "%{http_code}" --max-time 5 "URL"
```

### Für Libraries/SDKs
```bash
# Tests + Version
python3 -m pytest --tb=short 2>/dev/null | tail -5
```

### Immer
```bash
# Git-Status
git status --short
git log --oneline -3
```

## Output-Format

```
=== {Projektname} Status ===

Services:  ✓/✗ {Service}: {Status}
Git:       {Branch}, {clean/dirty}
Letzter Commit: {hash} {message}
```

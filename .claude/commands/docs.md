---
description: "Dokumentations-Health-Check: /docs [subcommand]"
context: fork
---

# Documentation Health Check

Führe einen Dokumentations-Health-Check durch.

## Subcommands

Argument: $ARGUMENTS

### Wenn kein Argument → Quick Health Check

Führe alle 3 Checks aus:

#### 1. Zahlen-Validierung

Prüfe Counts in CLAUDE.md gegen aktuelle Quellen:

| Zahl | So prüfen |
|------|-----------|
| Slash Commands | Zähle `.claude/commands/*.md` Dateien |
| Services | Zähle Services in `docker-compose.yml` (falls vorhanden) |

#### 2. Link-Check (Top-Level)

Prüfe Links in CLAUDE.md und README.md:
Für jeden `[text](./pfad)` Link: Existiert die Ziel-Datei?

#### 3. Freshness-Check (Top-5)

Finde die 5 Docs die am längsten nicht aktualisiert wurden:
- `git log -1 --format=%ci` für jede .md-Datei
- Melde Docs wo Code im gleichen Verzeichnis neuer ist

**Output:**
```
=== Doku Health Check ===

Zahlen:   ✅/❌ [Details]
Links:    ✅ [N] OK, ❌ [N] tot
Freshness: [Top 5 veraltete Docs]
```

---

### "inventory" → Datei-Inventar

Alle `.md`-Dateien mit Pfad, Zeilen, letztem Git-Datum. Gruppiert: Aktiv vs. Archiv.

### "freshness" → Detaillierter Freshness-Check

Alle READMEs prüfen. Veraltet = Verzeichnis-Code > 7 Tage neuer als README.

### "links" → Vollständiger Link-Check

Alle internen Links in allen `.md`-Dateien prüfen.

### "archive" → Archivierungs-Check

Sprint-Docs mit Status COMPLETE finden → Archivierungs-Kandidaten melden.

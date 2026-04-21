---
description: "Verfügbare Commands anzeigen"
---

# Hilfe

Zeige alle verfügbaren Commands.

## Standard-Commands

| Command | Beschreibung |
|---------|--------------|
| `/sprint N "Name"` | Sprint-Gerüst erstellen (Datei + Taskboard) |
| `/tasks` | Taskboard-Übersicht (Prio-Gruppen, letzte Releases) |
| `/status` | Projekt-Status (Services, Git, Health) |
| `/debug <beschreibung>` | Problem analysieren (Root Cause + Empfehlung) |
| `/deploy` | Deployment-Workflow (Pre-Check → Deploy → Verify) |
| `/doku "Titel"` | Release dokumentieren (Changelog, SemVer-Tag, Sprint-Archivierung) |
| `/docs [subcommand]` | Doku Health Check (freshness, links, inventory, archive) |
| `/cleanup [option]` | Housekeeping (docker, logs, git) |
| `/help` | Diese Hilfe |

## Beispiele

### Sprint-Workflow
```
/tasks                         # Was steht an?
/sprint 5 "Auth Refactor"     # Sprint erstellen
# ... implementieren ...
/doku "Auth Refactor"          # Release dokumentieren
```

### Maintenance
```
/status                        # Alles am Laufen?
/debug "Service X antwortet nicht"  # Problem analysieren
/cleanup docker                # Docker aufräumen
/docs                          # Doku-Qualität prüfen
```

## Projekt-spezifische Commands

Prüfe `.claude/commands/` für weitere projektspezifische Commands.
Lies CLAUDE.md für Projekt-Kontext und Konventionen.

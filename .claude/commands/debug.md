---
description: "Problem debuggen: /debug <beschreibung>"
context: fork
---

# Debug

Debugge das Problem: $ARGUMENTS

**Superpowers:** Invoke Skill `systematic-debugging` before starting analysis.

## Debug-Workflow

### 1. Kontext aus CLAUDE.md lesen

Lies CLAUDE.md um die Infrastruktur zu verstehen: Container-Namen, Ports, DB-Zugriff, Service-Architektur.

### 2. Status prüfen

```bash
# Git Status
git status --short

# Container (falls Docker-Projekt)
docker ps --format "table {{.Names}}\t{{.Status}}" 2>/dev/null

# Logs (Container-Name aus CLAUDE.md)
docker logs CONTAINER --tail 30 2>&1
```

### 3. Fehler eingrenzen

- Welcher Service/welche Komponente ist betroffen?
- Seit wann tritt der Fehler auf?
- Was hat sich zuletzt geändert? (`git log --oneline -10`)
- Logs auf Fehler durchsuchen

### 4. Root Cause Analysis

- Ist es ein Code-Fehler, Config-Problem oder Infrastruktur-Issue?
- Lässt sich der Fehler reproduzieren?
- Gibt es ähnliche Probleme in der Git-History?

### 5. Diagnose ausgeben

```
=== Debug Report ===

Problem:   {Beschreibung aus $ARGUMENTS}
Bereich:   {Service/Komponente}
Status:    {Was funktioniert, was nicht}

Root Cause: {Analyse}
Evidence:   {Logs, Fehlermeldungen, Beobachtungen}

Empfehlung: {Konkreter Fix oder nächster Schritt}
```

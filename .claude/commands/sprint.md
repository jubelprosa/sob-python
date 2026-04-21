---
description: "Sprint-Gerüst erstellen: /sprint N \"Name\""
---

# Sprint Setup

Erstelle Sprint-Gerüst: $ARGUMENTS

## Input

Flexibles Format:

**Mit Nummer und Name:** `107 "User Auth Refactor"` → Sprint 107
**Mit Nummer, Name und Prio:** `107 "User Auth Refactor" P0`
**Nur Name:** `"User Auth Refactor"` → Auto-detect nächste Nummer

Parse aus $ARGUMENTS:
- **Nummer**: Falls Zahl vorhanden, nutze diese. Sonst: höchste existierende + 1
- **Name**: Text in Anführungszeichen
- **Priorität**: P0/P1/P2/P3 (Default: P1)

**Superpowers:** Invoke Skill `brainstorming` for scope/approach decisions, then `writing-plans` for the sprint plan.

## Workflow

### 1. Kontext sammeln

```bash
# Höchste Sprint-Nummer ermitteln
ls docs/sprints/SPRINT*.md docs/archive/sprints/SPRINT*.md 2>/dev/null | grep -oP 'SPRINT\K[0-9]+' | sort -n | tail -1

# Prüfen ob Sprint-Nummer bereits existiert
ls docs/sprints/SPRINT{N}_*.md docs/archive/sprints/SPRINT{N}_*.md 2>/dev/null
```

- Wenn die Nummer bereits existiert → Fehler anzeigen und abbrechen
- Wenn keine Nummer angegeben → höchste + 1 verwenden

### 2. Dateiname ableiten

Aus dem Namen einen UPPER_SNAKE_CASE Slug generieren:
- Leerzeichen → `_`
- Umlaute → ae/oe/ue/ss
- Sonderzeichen entfernen
- Alles UPPERCASE

Dateiname: `docs/sprints/SPRINT{N}_{SLUG}.md`

### 3. Sprint-Datei erstellen

Erstelle die Datei mit diesem Template:

```markdown
# Sprint {N}: {Name}

> **Status:** BACKLOG
> **Priorität:** {Prio}
> **Größe:** <!-- S | M | L | XL — siehe SPRINT_GUIDE.md -->
> **Erstellt:** {YYYY-MM-DD}
> **Abhängigkeiten:** <!-- Sprint X | keine -->
> **Git-Strategie:** <!-- Auto-Fill: S=Single commit, M+=Commit pro Phase -->

---

## Kontext

<!--
Warum jetzt? Was ist das konkrete Problem oder die Gelegenheit?
Was ist der Ist-Zustand?
Welche Auswirkung hat das?
-->

**Ziel:** <!-- Ein Satz: Was ist am Ende anders? (Outcome, nicht Maßnahme) -->

---

## Ansatz

### 1. <!-- Schritt-Name -->

<!-- Was genau passiert? Welche Dateien werden geändert? -->

~~~bash
# Verifizierung: ...
# Erwartung: ...
~~~

### 2. <!-- Schritt-Name -->

~~~bash
# Verifizierung: ...
# Erwartung: ...
~~~

---

## Dateien

| Datei | Änderung |
|-------|----------|
| <!-- `pfad/datei.py` --> | <!-- Beschreibung --> |

---

## Deployment

<!-- [M+] Reihenfolge, Migration vor Rebuild? -->

---

## Verifizierung

~~~bash
# End-to-End Check nach Deployment
~~~

---

## Rollback

<!-- [M+] Was tun bei Fehler? -->

---

## Learnings

<!-- Nach Abschluss ausfüllen -->
```

**Git-Strategie Auto-Fill:** S → `Single commit + push am Ende`, M/L/XL → `Commit pro Phase, push am Ende`

### 4. Taskboard aktualisieren

Lies CLAUDE.md um den Taskboard-Pfad zu ermitteln (TASKBOARD.md, ROADMAP.md oder docs/TASKBOARD.md).

Füge neuen Sprint-Abschnitt ein:

```markdown
### Sprint {N}: {Name} ({Prio})

> **Ziel:** <!-- Ziel hier eintragen -->
> **Details:** [SPRINT{N}_{SLUG}.md](./sprints/SPRINT{N}_{SLUG}.md)

| Phase | Task | Status |
|-------|------|--------|
| <!-- Phase 1 --> | <!-- Task --> | ⬜ |
| <!-- Phase 2 --> | <!-- Task --> | ⬜ |

---
```

### 5. Bestätigung

```
✅ Sprint {N} angelegt: "{Name}" ({Prio})

Dateien:
- docs/sprints/SPRINT{N}_{SLUG}.md (Template)
- {Taskboard} (neuer Abschnitt)

Nächste Schritte:
1. Sprint-Datei ausfüllen: Kontext, Ziel, Ansatz
2. Taskboard Phasen/Tasks konkretisieren
3. Implementieren
→ Sprint-Best-Practices: docs/SPRINT_GUIDE.md
```

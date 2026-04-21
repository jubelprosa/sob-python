# sob-python

> **Typ:** Technical Reference
> **Projekt:** sob-python — Python SDK für State of Biz API
> **Letztes Update:** 2026-03-29
> **Version:** 1.0

---

## Kontext

Python SDK für die [State of Biz (SOB)](https://state-of.biz) Central Bank Intelligence API. Publiziert auf PyPI. Inkludiert LangChain und LlamaIndex Integrationen für RAG-Pipelines.

**Stack:** Python 3.10+, httpx, Pydantic 2, Hatchling (Build)
**PyPI:** `pip install sob-python`

---

## Schnellnavigation

| Ich will... | Gehe zu... |
|-------------|------------|
| Slash Commands | [.claude/commands/](./.claude/commands/) |
| Sprint-Prozess | [docs/SPRINT_GUIDE.md](./docs/SPRINT_GUIDE.md) |
| Build Config | [pyproject.toml](./pyproject.toml) |

---

## Struktur

```
sob-python/
├── sob/                  # SDK Source
├── tests/                # pytest Test-Suite
├── .claude/              # Claude Code Konfiguration
├── docs/
│   ├── SPRINT_GUIDE.md
│   └── sprints/
├── pyproject.toml        # Build + Tool Config
├── CLAUDE.md             # Diese Datei
├── README.md             # PyPI README
└── LICENSE
```

---

## Konventionen

### Dev
```bash
pip install -e ".[dev]"        # Editable Install mit Dev-Dependencies
pytest                         # Tests
ruff check .                   # Linting
```

### Publish
```bash
python -m build
twine upload dist/*
```

### Commit Messages
```
feat|fix|docs|refactor|chore(scope): Beschreibung
```

---

## Routing-Regeln

| Request-Typ | Rolle | Beispiel |
|-------------|-------|----------|
| Bug/Error | debugger | "SDK wirft Auth-Fehler" |
| Neues Feature | architect | "Neuer Endpoint" |
| Code schreiben | coder | "LlamaIndex Reader" |
| Release | deployer | "PyPI Release" |
| Tests | tester | "Test Coverage erhöhen" |

---

## Superpowers-Integration

| Trigger | Skill | Wann |
|---------|-------|------|
| Debugging | `systematic-debugging` | VOR der Analyse |
| Feature-Planung | `brainstorming` → `writing-plans` | VOR dem Code |
| Tests schreiben | `test-driven-development` | VOR dem Implementierungscode |
| Release | `verification-before-completion` | VOR dem PyPI-Upload |

---

## Slash Commands

| Command | Beschreibung |
|---------|--------------|
| `/status` | Test- und Package-Status |
| `/tasks` | Taskboard |
| `/sprint N "Name"` | Sprint erstellen |
| `/debug <beschreibung>` | Problem debuggen |
| `/deploy` | PyPI Release-Workflow |

---

*CLAUDE.md v1.0 — sob-python*

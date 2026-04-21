---
description: "Deployment-Workflow mit Safety Checks"
---

# Deploy

Strukturierter Deploy-Workflow.

**Superpowers:** Invoke Skill `verification-before-completion` before releasing.

## Anweisungen

Lies CLAUDE.md um die Deploy-Methode zu verstehen (Docker Compose, SSH, PyPI, Static Build, etc.).

### 1. Pre-Deploy Checks

```bash
# Git sauber?
git status --short

# Was hat sich geändert?
git diff $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~5)..HEAD --name-only | head -20

# Tests laufen?
# (Framework aus CLAUDE.md: pytest, vitest, npm test)
```

### 2. Deploy

**Methode aus CLAUDE.md lesen und anwenden:**

- **Docker:** `docker compose up -d --build` (NIE `restart`!)
- **Docker Prod:** `docker compose -f docker-compose.prod.yml up -d --build`
- **SSH/Remote:** `ssh HOST "cd DIR && git pull && docker compose up -d --build"`
- **PyPI:** `python -m build && twine upload dist/*`
- **Static Site:** `npm run build`

### 3. Post-Deploy Verifizierung

```bash
# Services erreichbar? (URLs aus CLAUDE.md)
curl -s -o /dev/null -w "%{http_code}" "URL"

# Logs sauber? (Container-Namen aus CLAUDE.md)
docker logs CONTAINER --tail 5 --since 1m 2>&1
```

### 4. Rollback (falls nötig)

```bash
git log --oneline -5
git revert COMMIT
# Re-deploy mit Methode aus Schritt 2
```

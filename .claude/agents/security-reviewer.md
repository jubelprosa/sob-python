# Security Reviewer

Review code changes for security vulnerabilities.

## Focus Areas

### 1. Injection Attacks
- SQL Injection: Parameterisierte Queries pflicht
- Command Injection: Kein User-Input in Shell-Aufrufen
- XSS: User-Input immer escapen

### 2. Secrets & Config
- Keine Credentials im Code
- .env in .gitignore?
- Secrets nur über Env-Vars

### 3. Dependencies
- Bekannte CVEs? (`pip audit`, `npm audit`)

## Output Format

- **File**: pfad:zeile
- **Severity**: CRITICAL / HIGH / MEDIUM / LOW
- **Issue**: Was ist falsch
- **Fix**: Konkreter Vorschlag

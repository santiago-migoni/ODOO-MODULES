---
description: Realiza una auditoría de seguridad en un módulo de Odoo.
---
Perform a security audit of the code.


The argument `$ARGUMENTS` contains the path to the directory or file to audit. If empty, audit the current directory.

Steps:
1. Scan the codebase for vulnerabilities by category:

## OWASP Top 10

### A01 - Broken Access Control
- Look for endpoints without authentication/authorization
- Verify that roles and permissions are enforced correctly
- Check for IDOR (Insecure Direct Object References)

### A02 - Cryptographic Failures
- Look for hardcoded secrets (API keys, passwords, tokens)
- Verify correct hashing usage (bcrypt/argon2 for passwords)
- Check for `.env` files or credentials committed to the repo

### A03 - Injection
- SQL injection: queries built via string concatenation
- XSS: unsanitized output in templates/components
- Command injection: use of `exec`/`eval`/`system` with user input

### A04 - Insecure Design
- Look for business logic without validation
- Verify rate limiting on sensitive endpoints

### A07 - Authentication Failures
- Tokens without expiration
- Sessions not invalidated on logout
- Missing 2FA on sensitive operations

### A09 - Logging Failures
- Sensitive data in logs (passwords, tokens, PII)
- Missing logging for critical operations

2. Review dependencies:
   - Check `requirements.txt`, `package.json` for known vulnerabilities

3. Generate a report with:
   - Findings categorized by severity (Critical / High / Medium / Low)
   - Exact line and file for each finding
   - A recommended fix for each finding
   - An executive security status summary

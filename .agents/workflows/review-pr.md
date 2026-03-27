---
description: Revisa un Pull Request siguiendo los estándares de calidad.
---
Review a GitHub Pull Request with a quality checklist.


The argument `$ARGUMENTS` contains the PR number or the URL to review.

Steps:
1. Get PR details using `gh pr view $ARGUMENTS`.
2. Review the full diff with `gh pr diff $ARGUMENTS`.
3. Analyze the changes by evaluating each checklist item:

## Review Checklist

### Correctness
- [ ] The logic implements what the PR claims
- [ ] No edge cases are left unhandled
- [ ] Types are correct (no unnecessary `any`)

### Security
- [ ] No OWASP issues (XSS, SQL injection, etc.)
- [ ] No secrets/credentials are exposed
- [ ] User inputs are validated and sanitized

### Quality
- [ ] Readable code with descriptive names
- [ ] No avoidable code duplication
- [ ] No unnecessary dependencies added

### Tests
- [ ] Changes are covered by tests
- [ ] Tests verify behavior, not implementation details

### Performance
- [ ] No N+1 queries or costly loops
- [ ] No obvious memory leaks

4. Produce a summary with:
   - Verdict: Approve / Request changes / Comment
   - Categorized findings (blocking / suggestion / nitpick)
   - Inline comments for specific issues

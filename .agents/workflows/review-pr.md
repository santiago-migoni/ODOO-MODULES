---
description: Revisa un Pull Request siguiendo los estándares de calidad.
---
# Review PR Workflow (Odoo 19)

Complete process for reviewing and validating Odoo custom modules in Pull Requests.

The argument `$ARGUMENTS` contains the PR number or the URL.

## 1. Context Collection

1. Get PR details using `gh pr view $ARGUMENTS`.
2. Review the full diff using `gh pr diff $ARGUMENTS`.
3. Identify all affected models, views, and security files.

## 2. Odoo 19 Review Checklist

- [ ] **Technical Conventions**:
    - [ ] Uses `<list>` instead of legacy `<tree>`.
    - [ ] Uses `invisible="..."` instead of `attrs="..."`.
    - [ ] Correct use of `@api.ondelete` in place of `unlink()`.
- [ ] **Security**:
    - [ ] New models have an entry in `ir.model.access.csv`.
    - [ ] Multi-company models have an appropriate record rule.
    - [ ] No unsafe `sudo()` usage in public-facing methods.
- [ ] **Performance**:
    - [ ] No `search()` calls inside loops (N+1 check).
    - [ ] Correct use of `mapped()` or filtered for recordsets.
    - [ ] Computed fields are `stored` if used in list views/filters.
- [ ] **Naming & Metadata**:
    - [ ] Technical name prefixed with `dipl_`.
    - [ ] Stable XML IDs with module namespace.
    - [ ] Version follows `19.0.x.y.z`.
- [ ] **Quality**:
    - [ ] `TransactionCase` covers new logic.
    - [ ] `i18n/es.po` is updated with all new strings.
    - [ ] `CHANGELOG.md` reflects the changes.

## 3. Verdict

Provide a summary:
- **Major Issues**: (N+1 queries, missing security, broken logic).
- **Minor Issues**: (Naming, formatting, typos).
- **Summary**: Approve, Request Changes, or Comment.

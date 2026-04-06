# Module Changelog Policy

## Scope
This policy applies to every installable module with the `dipl_*` prefix.
Each module must own its own `CHANGELOG.md` file at module root.

## Release Gate Severity
- Promotion from `dev` to `test` is blocked if the affected module changelog is missing or outdated.
- PR creation or merge recommendation to `master` is blocked if the module changelog is not frozen into a versioned, dated release entry.

## What Counts as a Relevant Change
Update `CHANGELOG.md` when the module changes in ways that matter for delivery, support, rollback, or release communication.
Relevant changes include:
- Functional behavior additions or removals.
- Technical refactors or hardening with operational impact.
- Compatibility updates across core modules, environments, or assets.
- Testing additions, fixes, or new safety coverage that materially improves release confidence.

## Operating Rules
- Use `## Unreleased` as the working section during implementation.
- Keep `## Unreleased` current while slices are being delivered.
- Before `dev -> test`, confirm that `## Unreleased` reflects the module scope that will be validated.
- Before `test -> master`, freeze `## Unreleased` into a versioned and dated entry, then reopen a fresh `## Unreleased` section for the next cycle.

## Final Audit Expectations
Before recommending production, verify that:
- The affected module has `CHANGELOG.md`.
- The changelog scope matches the implementation and QA evidence.
- The versioned release entry is suitable for support, release notes, and rollback context.

## Authoring Rules
- The changelog must be manual and curated.
- Do not auto-generate entries from commit history.
- Keep entries concise and release-oriented.

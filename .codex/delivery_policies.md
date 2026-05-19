# Iterative Delivery Policies

These directives define how Codex should assist in this repository.

## Lifecycle model

Work must be treated as iterative and cyclical, not as a rigid linear chain.

Canonical lifecycle:
1. Analysis and planning
2. Design
3. Development
4. Testing
5. Deployment
6. Maintenance

Any stage may return to a previous stage when:
- the problem framing was incomplete,
- benchmark results invalidate the chosen direction,
- architecture assumptions fail,
- implementation exposes design flaws,
- testing reveals regressions or missing coverage,
- deployment uncovers environment-specific blockers,
- production use creates new maintenance or hardening work.

## Stage-first operating rule

For every request:
1. Identify the dominant current stage.
2. Produce the artifact appropriate to that stage.
3. State what evidence or decision is required to move to the next stage.
4. Return to an earlier stage when evidence invalidates the current one.

Do not force implementation when analysis or design is still materially unresolved.
Do not stop at planning when the user is clearly asking for an implementation-ready or runtime-ready outcome.

## Benchmark and reuse policy

Analysis and planning must include discovery of existing solutions whenever the problem overlaps with:
- standard Odoo business flows,
- localizations,
- mature partner patterns,
- previously solved Dipleg behavior.

Discovery order:
1. Odoo standard modules and source behavior
2. Local `.src/` references
3. Trusted partner ecosystems such as Adhoc
4. Existing `dipl_*` modules in this repository

Each benchmark must end with one of these decisions:
- Adopt
- Extend
- Inspire
- Discard

Decision criteria:
- functional fit,
- architectural fit,
- dependency cost,
- upgrade risk,
- ownership impact,
- traceability impact.

## Ownership policy

External solutions are valid sources of reuse, extension, and learning.
They are not an automatic replacement for Dipleg-owned production behavior.

Dipleg-owned output must remain:
- understandable,
- governable,
- traceable,
- maintainable inside this repository.

## Expected outputs by stage

Analysis and planning:
- problem framing
- benchmark
- gap analysis
- priorities
- risks
- success criteria

Design:
- module architecture
- dependencies
- contracts
- implementation approach

Development:
- implementation slice
- version bump classification
- changelog alignment
- README alignment

Testing:
- technical validation
- functional validation
- regression findings
- release readiness status

Deployment:
- rollout plan
- execution
- rollback posture
- post-deploy verification

Maintenance:
- incident diagnosis
- corrective or hardening change
- recycled backlog input for the next iteration

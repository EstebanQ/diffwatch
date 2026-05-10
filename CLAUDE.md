# CLAUDE.md

This file provides standing instructions for Claude Code when working in this repository.

---

## Read these files at the start of every session

Before doing any work, read the following files in this order:

1. **`PROJECT.md`** — the project vision, design principles, end-product description, and what is explicitly out of scope. This is the *why* and the *what*.
2. **`ROADMAP.md`** — the milestone breakdown, current progress, and definitions of done for each milestone. This is the *when* and the *in what order*.
3. **`NOTES.md`** — the running learning log. Contains decisions made, things tried, problems encountered, ways of working established, and future ideas. This is the *what we've learned so far*.

If any of these files do not yet exist, note that and ask before proceeding.

---

## Use NOTES.md actively

`NOTES.md` is a living document. Update it during the session whenever any of the following happens:

### Important details discovered
- A non-obvious behavior of a library, API, or tool that took time to figure out.
- A constraint or limitation that affects design (e.g., GitHub API rate limits, webhook payload quirks, vector store update semantics).
- A bug or pitfall encountered and how it was resolved.
- Anything future-me would want to know but would otherwise forget.

### Ways of working established
- Conventions adopted (naming, file layout, error handling patterns, logging format).
- Tooling decisions (which linter, which test runner, how to run things locally).
- Workflow patterns that worked well or didn't.

### Future features and ideas
- Anything interesting that comes up but is out of scope for the current milestone or for v1 entirely.
- These belong in a clearly labeled "Ideas / Future" section so they don't get confused with current work.

### Decisions made
- Significant technical decisions and the reasoning behind them. Especially decisions where there were real tradeoffs and the alternative was non-obvious. Capture the *why*, not just the *what*.

### Format guidance for NOTES.md

Keep entries dated and grouped by category. Suggested top-level sections:

```
## Decisions
## Important details / gotchas
## Ways of working
## Ideas / Future (explicitly out of scope for now)
## Open questions
```

Append, don't rewrite. The honest history is more valuable than a polished summary. If something was tried and abandoned, leave it in with a note about why — that record is part of the learning.

---

## Working principles for this project

These come from `PROJECT.md` but are worth restating because they shape day-to-day decisions:

- **Finishability over ambition.** Always favor a working end-to-end version over a polished single component. If a milestone is taking 3x longer than estimated, the right move is usually to scope down, not to push through.
- **Resist scope expansion.** When new ideas come up, write them in the "Ideas / Future" section of `NOTES.md`. Do not silently expand the current milestone.
- **Stay within the current milestone.** If a request would take work outside the current milestone in `ROADMAP.md`, flag it and ask whether to proceed anyway, defer it, or note it as a future idea.
- **Local-first, simple tooling.** Prefer Redpanda over Kafka, local vector stores (Qdrant or LanceDB) over hosted, simple Python over frameworks. The point is learning the patterns, not building production infrastructure.
- **Public repo from day one.** Boring early commits are part of the story. Don't hide work-in-progress.
- **Real public data only.** No synthetic datasets. The project's value comes from operating on real GitHub activity.

---

## What to ask before doing significant work

Before any substantial change, briefly confirm:

- Which milestone in `ROADMAP.md` does this work belong to?
- Is it within the current milestone's scope, or does it expand it?
- Does it conflict with anything in `PROJECT.md`'s "Out of Scope for v1" section?

If the work is outside the current milestone or out of scope for v1, surface that explicitly before doing it.

---

## Update ROADMAP.md as milestones progress

When a milestone item is completed, check it off in `ROADMAP.md`. When a milestone's definition of done is met, mark the milestone complete and call it out at the end of the session so I can confirm before moving on.

If during the work it becomes clear that a milestone needs to be re-scoped (split, combined, or reordered), propose the change rather than silently restructuring.

---

## Style and tone

- Be direct. Push back when something seems wrong or under-considered.
- Don't pad responses with unnecessary acknowledgement or summary.
- When there's a real tradeoff, name both sides honestly rather than picking the one that sounds best.
- Treat me as a senior engineer making my own technical decisions. Explain reasoning, but don't over-justify.

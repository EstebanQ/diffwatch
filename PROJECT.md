# Project: Real-Time Semantic Search Over GitHub PRs

## The Idea

A streaming system that ingests GitHub Pull Request activity in real time, maintains a fresh vector index of PR content, and supports semantic search and analysis over what's happening across selected repositories.

When a PR is opened, edited, commented on, merged, or closed in any of the watched repositories, the system reflects that change in its searchable index within seconds — not the next batch run, not the next nightly job.

## Why This Project

This project is a deliberate vehicle for building deep technical expertise in three areas that compound across multiple career paths (data infrastructure, database engineering, AI infrastructure, distributed systems):

1. **Streaming data systems** — real ingestion pipelines, message brokers, consumer patterns, backpressure, exactly-once semantics, freshness guarantees.
2. **Vector search infrastructure** — embedding strategies, vector store mechanics, index freshness, the consistency problem between a source of truth and a derived index.
3. **The integration between the two** — how change data flows from a source through a pipeline into a derived store, and how to keep that derived store correct, fresh, and observable.

The project is also a portfolio artifact. It should be public, demoable, and accompanied by writing that explains the design decisions and tradeoffs encountered.

## End Product Vision

A working system, deployed locally (and optionally to a small cloud environment), that includes:

### Ingestion layer
- Subscribes to GitHub events (webhooks for live data, REST API for backfill) for a configurable set of repositories.
- Handles PR lifecycle events: opened, edited, synchronized (new commits), reviewed, commented, closed, reopened, merged.
- Writes raw events to a durable message broker (Redpanda / Kafka).

### Processing layer
- Consumes events from the broker.
- Fetches full PR context as needed (title, description, commit messages, file paths touched, review comments).
- Generates embeddings using a chosen embedding model.
- Writes embeddings and metadata to a vector store, handling inserts, updates, and deletions correctly.
- Maintains observability: how fresh is the index, how long does an event take from emission to searchable, where are the bottlenecks.

### Query layer
- A semantic search interface: "find PRs related to authentication refactoring."
- A similarity interface: "given this PR, find others like it."
- A recency-aware query: "what's been happening in [topic / area] over the last N days."
- A simple frontend (CLI first, web UI optional later) to demonstrate these queries.

### Observability and operational concerns
- Metrics on ingestion rate, processing latency, end-to-end freshness.
- Logging that lets you trace a single PR's journey through the system.
- A clear story for how to recover from failure (consumer crashes, embedding service outages, vector store unavailability).

## Use Cases the System Should Support

These are the concrete things a user (initially: me) should be able to do with the finished system:

- **Find similar PRs** — "I'm reviewing this PR; show me other PRs that touched similar code or solved similar problems."
- **Topic search** — "Show me all PRs across these repos related to performance optimization in the last quarter."
- **Recent activity in an area** — "What's been happening in the storage subsystem of [repo] in the last two weeks?"
- **Regression candidates** — "A bug appeared. Find recent PRs whose descriptions or diffs are semantically related to the affected functionality."
- **Cross-repo pattern detection** — "Show me PRs across multiple repos that all dealt with the same kind of problem."

Not every use case has to ship in v1. The architecture has to support them.

## Constraints and Principles

- **Finishability over ambition.** Every scope decision favors getting a working version end-to-end over getting any single piece perfect. A complete v1 with rough edges beats a polished v0.5.
- **Real public data.** No synthetic data, no toy datasets. The project's value comes from operating on real GitHub activity.
- **Public and visible from day one.** The repository is public from the first commit. The README evolves with the project. Boring early commits are part of the story.
- **Write as you build.** A series of blog posts at major milestones. Writing forces understanding and is a major part of the portfolio value.
- **Avoid premature scope expansion.** New ideas go into `IDEAS.md`, not into v1.
- **Resist over-engineering early.** Choose simple, local-first tools (Redpanda over Kafka, Qdrant or LanceDB over hosted vector DBs, OpenAI or sentence-transformers for embeddings). Optimize for getting unstuck, not for production-grade architecture, until v1 is working.

## Out of Scope for v1

These are interesting and probably useful eventually. They are *not* part of the first finishable version:

- Code diff embeddings (v1 embeds PR text only).
- A polished web UI (v1 is CLI; a basic web UI may come later).
- Multi-tenancy or authentication.
- Public deployment with a real domain.
- Regression detection as a packaged feature (v1 supports the underlying queries; a dedicated regression workflow is a follow-on).
- Sophisticated relevance tuning (rerankers, hybrid search, learned-to-rank).
- Cross-repo correlation analysis as a packaged feature.

## What "Done" Looks Like for v1

- A public GitHub repo containing the working system.
- A README that explains what it does, why it was built, the architecture, how to run it locally, and what was learned.
- At least one substantive blog post explaining a non-trivial design decision encountered during the build.
- A demo I can give in 5 minutes that shows live PRs flowing in and being immediately searchable.
- An honest section in the README about known limitations and what would change in v2.

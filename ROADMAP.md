# Roadmap: Real-Time Semantic Search Over GitHub PRs

This roadmap breaks the project into small, finishable milestones. Each milestone has a clear definition of done. The goal is steady forward motion, not perfection at any single step.

**Timeline target:** 8 weeks of evening/weekend work to v1. This is a target, not a deadline — but if a milestone is taking 3x longer than estimated, that's a signal to scope down, not to push through.

---

## Milestone 0: Pre-work (≤ 2 hours, do not exceed)

The temptation will be to research extensively before writing any code. Resist this. The right amount of pre-work is small.

- [ ] Skim GitHub REST API docs for the `pulls` endpoint and the events endpoint.
- [ ] Glance at one quickstart for the chosen vector DB (Qdrant or LanceDB — pick in 5 minutes, do not deliberate).
- [ ] Create a GitHub personal access token with `public_repo` scope.
- [ ] Create a new public GitHub repository for the project.
- [ ] Decide on the embedding approach: OpenAI `text-embedding-3-small` (fastest start, costs cents) or `sentence-transformers` locally (no API, slower setup). Pick one in 5 minutes.

**Done when:** repo exists on GitHub, token is in a `.env` file (gitignored), embedding choice is made.

---

## Milestone 1: End-to-end batch pipeline, one repo (Week 1)

The goal of this week is to have data flowing all the way through the pipeline, even if every component is crude. No streaming yet. Just batch.

- [ ] Pick one interesting repo to start with (something you'd actually want to explore — e.g. `apache/iceberg`, `pola-rs/polars`, `duckdb/duckdb`, your choice).
- [ ] Write a Python script that fetches the last 100 PRs from that repo via the GitHub REST API.
- [ ] For each PR, store the raw JSON in a local SQLite database or as JSONL on disk. (Either is fine. Pick fast.)
- [ ] Write a script that reads stored PRs, generates embeddings for `title + body`, and writes them to a vector store (Qdrant or LanceDB) along with PR metadata (id, number, title, url, author, state, created_at).
- [ ] Write a query script that takes a string from the command line, embeds it, and returns the top 10 most similar PRs as a list of `(score, title, url)`.

**Done when:** running `python query.py "authentication refactor"` returns a ranked list of relevant PRs from the chosen repo.

**Estimate:** 3-5 evenings. If it's taking longer, you're over-engineering.

---

## Milestone 2: Multiple repos and basic backfill (Week 2)

- [ ] Make the repo list configurable (a YAML or TOML file).
- [ ] Expand to 3-5 repos.
- [ ] Backfill the last 3 months of PRs for each repo.
- [ ] Handle pagination correctly (GitHub's API paginates at 100 items).
- [ ] Handle GitHub API rate limits gracefully (sleep and retry on 429s, log progress).
- [ ] Add a `repo` field to the vector store metadata so queries can be filtered by repo.

**Done when:** the index contains PRs from multiple repos and queries can be scoped to a specific repo or run across all of them.

**Estimate:** 2-4 evenings.

---

## Milestone 3: Live ingestion via webhooks (Weeks 3-4)

This milestone introduces the streaming spine. Until now, ingestion has been a script you run manually. Now it becomes a service that reacts to live events.

- [ ] Set up Redpanda locally via Docker Compose (Kafka-compatible, easier to run than Kafka).
- [ ] Create a webhook receiver service (FastAPI or Flask) that accepts GitHub webhook POSTs.
- [ ] Use [smee.io](https://smee.io) or `ngrok` to forward webhooks from GitHub to your local service.
- [ ] Configure GitHub webhooks on your watched repos for `pull_request` events.
- [ ] On webhook receipt, validate the signature (basic security hygiene — even locally, get the pattern right) and write the event to a Redpanda topic.
- [ ] Write a consumer service that reads from the Redpanda topic, fetches full PR details if needed, embeds, and upserts to the vector store.
- [ ] Verify end-to-end: open a test PR in one of the watched repos, observe the event flowing through and the index updating.

**Done when:** a PR opened on GitHub is searchable in the local index within ~30 seconds, with no manual intervention.

**Estimate:** 4-7 evenings. This milestone is the densest in terms of new concepts. Take your time.

**Common pitfalls to expect:**
- Webhook signature validation is fiddly the first time.
- The webhook payload doesn't always contain everything you need; sometimes you have to call the API for full details.
- Local development with webhooks is annoying without ngrok/smee.

---

## Milestone 4: Updates and deletions handled correctly (Week 5)

PRs are not immutable. They get edited, closed, reopened, merged. The index has to reflect the current state.

- [ ] Handle `edited` events: re-embed and upsert when PR title or body changes.
- [ ] Handle `closed` and `merged` events: update the metadata (`state`, `merged_at`).
- [ ] Decide on a policy for closed PRs: keep them in the index (probably yes — they're still useful for search) but mark them clearly.
- [ ] Handle `synchronize` events: when new commits are pushed to a PR, decide whether to re-embed (probably not for v1, since title/body may not have changed).
- [ ] Add a "last updated" timestamp to vector store metadata.
- [ ] Write a small integration test or manual verification script that exercises edit / close / reopen flows.

**Done when:** the index reflects the current state of PRs accurately, including edits and state changes.

**Estimate:** 2-4 evenings.

---

## Milestone 5: Freshness observability (Week 6)

Until now, you've been hoping the system is fresh. Now you measure it.

- [ ] Define a freshness metric: e.g., "p50 / p95 time from GitHub event timestamp to event being searchable in the index."
- [ ] Add timing instrumentation at key points: webhook received, written to topic, consumed from topic, embedded, written to vector store.
- [ ] Log these as structured logs.
- [ ] Build a simple script (or a `/metrics` endpoint) that reports current freshness percentiles over the last hour.
- [ ] Identify and document the slowest stage. Decide whether to optimize or accept it.

**Done when:** you can answer "how fresh is the index right now?" with a number, and you understand where time is spent.

**Estimate:** 2-3 evenings.

---

## Milestone 6: Better queries (Week 7)

Up to now, queries have been basic semantic search. This milestone adds the queries the project was actually built for.

- [ ] Implement "find PRs similar to PR #X": given a PR id, retrieve its embedding and find nearest neighbors (excluding itself).
- [ ] Implement a recency-aware query: "what's been happening in [topic] recently" — combine semantic similarity with a recency filter or boost.
- [ ] Add filtering: by repo, by state (open/closed/merged), by date range, by author.
- [ ] Build a simple CLI that exposes these queries cleanly.

**Done when:** all three of the headline use cases (semantic search, similarity, recent activity) work via the CLI.

**Estimate:** 3-5 evenings.

---

## Milestone 7: Polish, write-up, and demo (Week 8)

The system works. Now make it presentable.

- [ ] Clean up the README. Make it the document a senior engineer would read to understand the project. Include: what it does, why it exists, the architecture (with a diagram), how to run it, what was learned, what the limitations are.
- [ ] Finalize `NOTES.md` — keep it as the running learning log; don't sanitize it. The honest record is more valuable than a polished one.
- [ ] Write at least one substantive blog post. Suggested topics: "Building a streaming GitHub PR indexer," "Handling updates and deletions in a real-time vector index," or "What I learned about embedding strategies for PR text." Pick whichever you have the most to say about.
- [ ] Record a 5-minute demo video (or write a demo script) showing the system in action.
- [ ] Update LinkedIn and CV to reflect the work.

**Done when:** someone unfamiliar with the project can clone the repo, read the README, understand what was built and why, and run it locally without asking questions.

**Estimate:** 3-5 evenings.

---

## After v1 (the IDEAS.md graveyard / runway)

When ideas come up during the build that you want to do but shouldn't do now, write them in `IDEAS.md`. After v1 is done, the most likely high-value follow-ons are:

- Code diff embeddings (embed actual code changes, not just PR text).
- Hybrid search (combine semantic with BM25 or keyword search).
- A web UI.
- Public deployment.
- A second data source (Reddit, HN) using the same architecture, to demonstrate the pattern is reusable.
- The CDC version of the project: introduce Postgres + Debezium between ingestion and processing, to learn CDC properly.
- Regression detection as a packaged feature.
- Cross-repo pattern detection.

Pick one and treat it as a follow-on project of similar scope. Don't try to do all of them.

---

## Anti-goals

Things explicitly not being optimized for, listed so they don't sneak in:

- Production-grade reliability. This is a learning project, not a product.
- High availability. One node, one process per service is fine.
- Cost optimization. If embeddings cost a few dollars in OpenAI credits, that's fine.
- Pixel-perfect UI. The CLI is the interface. A basic web UI is optional polish.
- Supporting every GitHub event type. Pull request events are enough for v1.

---

## How to use this roadmap

- Work the milestones in order. Don't skip ahead. Each one builds on the previous.
- If a milestone is too big, split it. If it's too small, combine it. The milestone count is not sacred.
- Update this file as the project evolves. The roadmap is a living document, not a contract.
- When stuck, pick the smallest possible next step and do that. Momentum beats deliberation.

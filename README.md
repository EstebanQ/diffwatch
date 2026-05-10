# diffwatch

> Real-time semantic search over GitHub Pull Requests. Watch a set of repositories, ingest PR activity as it happens, and query the resulting index with natural language.

**Status:** Pre-development — architecture and planning complete, no code yet.

---

## What it does

`diffwatch` watches a configurable set of public GitHub repositories and maintains a continuously-updated semantic index of their Pull Request activity. When a PR is opened, edited, or closed, the index reflects that change within seconds.

You can then ask the index questions like:

- "Find PRs related to authentication refactoring."
- "Show me PRs similar to this one I'm reviewing."
- "What's been happening in the storage layer over the last two weeks?"

For the full project rationale and design principles, see [PROJECT.md](./PROJECT.md).

---

## Why this exists

This is a learning project built to develop depth in three areas:

1. **Streaming data systems** — message brokers, consumer patterns, backpressure, freshness guarantees.
2. **Vector search infrastructure** — embedding strategies, vector store mechanics, index consistency with a source of truth.
3. **The integration between the two** — the patterns for keeping a derived index in sync with a continuously-changing source.

It is also a portfolio artifact intended to demonstrate end-to-end systems thinking, not just isolated component knowledge.

---

## Architecture

```
┌─────────────────┐
│  GitHub events  │
│   (webhooks)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌─────────────────┐
│  Ingest service │─────▶│    Redpanda     │
│   (FastAPI)     │      │   (Kafka API)   │
└─────────────────┘      └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Embed + index   │
                         │    consumer     │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  Vector store   │
                         │ (Qdrant/LanceDB)│
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  Query CLI      │
                         └─────────────────┘
```

---

## Design decisions

- **Redpanda over Kafka** — same API, much simpler local setup. Migrating later is straightforward if needed.
- **Local-first vector store (Qdrant or LanceDB)** — avoids cloud dependencies during development; decision between the two pending.
- **Embed PR title + body in v1** — simplest signal that's still meaningful. Code diff embeddings are a follow-on once the rest of the pipeline is solid.
- **Public repos only** — no auth complexity, no privacy concerns, all data is reproducible by anyone.

---

## Getting started

> The project is not yet runnable. This section will be filled in as components are built.

### Prerequisites (planned)

- Python 3.11+
- Docker and Docker Compose (for Redpanda and the vector store)
- A GitHub personal access token with `public_repo` scope
- An embedding provider — either an OpenAI API key or a local `sentence-transformers` model

---

## License

MIT

# pr-stream

> Real-time semantic search over GitHub Pull Requests. Watch a set of repositories, ingest PR activity as it happens, and query the resulting index with natural language.

**Status:** 🚧 Early development. Not yet functional. See [ROADMAP.md](./ROADMAP.md) for current progress.

---

## What it does

`pr-stream` watches a configurable set of public GitHub repositories and maintains a continuously-updated semantic index of their Pull Request activity. When a PR is opened, edited, or closed, the index reflects that change within seconds.

You can then ask the index questions like:

- "Find PRs related to authentication refactoring."
- "Show me PRs similar to this one I'm reviewing."
- "What's been happening in the storage layer over the last two weeks?"

The system is designed as an exploration of streaming data infrastructure and real-time vector search, using GitHub PRs as a real, public, high-signal data source.

---

## Why this exists

This is a learning project, built deliberately to develop depth in three areas:

1. **Streaming data systems** — message brokers, consumer patterns, backpressure, freshness guarantees.
2. **Vector search infrastructure** — embedding strategies, vector store mechanics, index consistency with a source of truth.
3. **The integration between the two** — the patterns for keeping a derived index in sync with a continuously-changing source.

It is also a portfolio artifact intended to demonstrate end-to-end systems thinking, not just isolated component knowledge.

For the full project rationale, design principles, and what the finished system should look like, see [PROJECT.md](./PROJECT.md).

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
                         │  Query CLI / API│
                         └─────────────────┘
```

For backfill, a separate batch process pulls historical PRs via the GitHub REST API and writes them through the same embedding + indexing path.

A more detailed architecture write-up will land here as the system is built.

---

## Getting started

> ⚠️ This section will be filled in as the project becomes runnable. For now, see [ROADMAP.md](./ROADMAP.md) to follow progress.

### Prerequisites (planned)

- Python 3.11+
- Docker and Docker Compose (for Redpanda and the vector store)
- A GitHub personal access token with `public_repo` scope
- An embedding provider — either an OpenAI API key or a local `sentence-transformers` model

### Installation (planned)

```bash
git clone https://github.com/<your-username>/pr-stream.git
cd pr-stream
cp .env.example .env
# Fill in GITHUB_TOKEN and embedding provider credentials
docker compose up -d
pip install -r requirements.txt
```

### Configuration (planned)

Edit `repos.yaml` to specify which repositories to watch:

```yaml
repos:
  - owner: apache
    name: iceberg
  - owner: pola-rs
    name: polars
```

### Running the backfill (planned)

```bash
python -m pr_stream.backfill --since 2026-02-01
```

### Running the live ingestion (planned)

```bash
python -m pr_stream.ingest        # webhook receiver
python -m pr_stream.consumer      # embedding + indexing consumer
```

### Querying (planned)

```bash
python -m pr_stream.query "authentication refactor"
python -m pr_stream.query --similar-to apache/iceberg#1234
python -m pr_stream.query --topic "performance" --since 14d
```

---

## Project layout (planned)

```
pr-stream/
├── PROJECT.md            # Project vision and design principles
├── ROADMAP.md            # Milestones and current progress
├── README.md             # This file
├── NOTES.md              # Running learning log
├── IDEAS.md              # Out-of-scope ideas to revisit later
├── docker-compose.yaml   # Redpanda, vector store, anything else local
├── repos.yaml            # Which repos to watch
├── pr_stream/
│   ├── backfill.py       # Historical PR ingestion via REST API
│   ├── ingest.py         # Webhook receiver service
│   ├── consumer.py       # Embedding + indexing consumer
│   ├── query.py          # Query CLI
│   ├── embedding.py      # Embedding provider abstraction
│   ├── store.py          # Vector store abstraction
│   └── models.py         # Shared data models
└── tests/
```

---

## Design decisions and tradeoffs

> This section will grow as decisions are made and documented. The intent is to capture the *why* behind significant choices, not just the *what*.

Notable decisions made or pending:

- **Redpanda over Kafka** — same API, much simpler local setup. The Kafka-compatible interface means migrating later is straightforward if needed.
- **Local-first vector store (Qdrant or LanceDB)** — avoids cloud dependencies during development; decision between the two pending.
- **Embed PR title + body in v1** — simplest signal that's still meaningful. Code diff embeddings are a follow-on once the rest of the pipeline is solid.
- **Public repos only** — no auth complexity, no privacy concerns, all data is reproducible by anyone.

---

## What's been learned

> This section will be updated at each milestone. See [NOTES.md](./NOTES.md) for the full running log.

---

## Limitations

> This section will document the honest limitations of v1 once it ships. Examples to be filled in: index size limits, freshness ceiling, query types not supported, failure modes not handled.

---

## License

MIT (or your choice — update before making the repo public).

---

## Acknowledgements

This project is a personal learning exercise. The architecture draws on patterns from production streaming and vector search systems, but the implementation prioritizes learning over production-readiness.

"""
Fetch pull requests from a GitHub repo and store them as JSONL.

Usage:
    python fetch_prs.py --repo pola-rs/polars --pr-count 100
    python fetch_prs.py --repo pola-rs/polars --pr-count 500 --out data/prs.jsonl
"""

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def fetch_page(owner: str, repo: str, page: int, per_page: int) -> list[dict]:
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"
    params = {"state": "all", "per_page": per_page, "page": page, "sort": "created", "direction": "desc"}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 429:
        reset = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
        wait = max(reset - int(time.time()), 1)
        print(f"Rate limited. Sleeping {wait}s...")
        time.sleep(wait)
        return fetch_page(owner, repo, page, per_page)

    response.raise_for_status()
    return response.json()


def fetch_prs(owner: str, repo: str, n: int) -> list[dict]:
    per_page = min(n, 100)
    pages_needed = math.ceil(n / per_page)
    collected = []

    for page in range(1, pages_needed + 1):
        remaining = n - len(collected)
        batch_size = min(remaining, per_page)
        prs = fetch_page(owner, repo, page, batch_size)
        collected.extend(prs)
        print(f"  Page {page}: fetched {len(prs)} PRs (total so far: {len(collected)})")

        if len(prs) < batch_size:
            break  # repo has fewer PRs than requested

    return collected[:n]


def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub PRs and store as JSONL.")
    parser.add_argument("--repo", required=True, help="owner/repo, e.g. pola-rs/polars")
    parser.add_argument("--pr-count", type=int, default=100, dest="pr_count", help="Number of PRs to fetch (default: 100)")
    parser.add_argument("--out", default=None, help="Output file path (default: data/<repo_slug>.jsonl)")
    args = parser.parse_args()

    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)

    if "/" not in args.repo:
        print("Error: --repo must be in owner/repo format", file=sys.stderr)
        sys.exit(1)

    owner, repo = args.repo.split("/", 1)

    out_path = Path(args.out) if args.out else Path("data") / f"{owner}_{repo}.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Fetching {args.pr_count} PRs from {args.repo}...")
    prs = fetch_prs(owner, repo, args.pr_count)

    with out_path.open("w", encoding="utf-8") as f:
        for pr in prs:
            f.write(json.dumps(pr) + "\n")

    print(f"Saved {len(prs)} PRs to {out_path}")


if __name__ == "__main__":
    main()

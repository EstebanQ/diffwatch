# GitHub REST API — Reference for diffwatch

API version: `2022-11-28`  
Base URL: `https://api.github.com`  
Auth header: `Authorization: Bearer <token>`  
Accept header: `application/vnd.github+json`

---

## Endpoints used

### List pull requests

```
GET /repos/{owner}/{repo}/pulls
```

Returns a paginated list of PRs for a repository.

**Key query parameters:**

| Parameter | Values | Notes |
|---|---|---|
| `state` | `open`, `closed`, `all` | Default is `open` — always pass `all` for backfill |
| `per_page` | 1–100 | Max 100 per request |
| `page` | integer | Starts at 1 |
| `sort` | `created`, `updated` | `updated` is useful for incremental fetches |
| `direction` | `asc`, `desc` | Default `desc` |

**Pagination:** iterate `page` until the response returns fewer than `per_page` results (or an empty array).

---

### Get a single pull request

```
GET /repos/{owner}/{repo}/pulls/{pull_number}
```

Returns full detail for one PR. Use this when the list response doesn't include everything needed (e.g., `body` can be null in list responses for very large descriptions).

---

## Pull request object — fields we use

| Field | Type | Notes |
|---|---|---|
| `id` | integer | GitHub's internal unique ID (stable across renames) |
| `number` | integer | The PR number shown in the UI (`#42`) |
| `title` | string | PR title — embedded in v1 |
| `body` | string or null | PR description — embedded in v1; can be null |
| `state` | `open` / `closed` | Closed covers both closed-without-merge and merged |
| `html_url` | string | The URL to display in search results |
| `user.login` | string | Author's GitHub username |
| `created_at` | ISO 8601 | When the PR was opened |
| `updated_at` | ISO 8601 | Last activity timestamp — useful for incremental sync |
| `closed_at` | ISO 8601 or null | When closed |
| `merged_at` | ISO 8601 or null | Non-null means it was merged, not just closed |
| `draft` | boolean | Draft PRs are usually lower signal; index them but note the flag |
| `labels` | array | Label names — useful metadata for filtering |

---

## Webhook events — `pull_request`

GitHub sends a POST to your webhook URL on PR activity. The payload always includes an `action` field and a full `pull_request` object.

### Action types we handle

| Action | What happened | What to do |
|---|---|---|
| `opened` | New PR created | Embed and index |
| `edited` | Title or body changed | Re-embed and upsert |
| `closed` | PR closed or merged | Update `state`, `closed_at`, `merged_at` in metadata |
| `reopened` | Closed PR reopened | Update `state` back to `open` |
| `synchronize` | New commits pushed | No action in v1 (title/body usually unchanged) |

### Action types we ignore (v1)

`assigned`, `unassigned`, `labeled`, `unlabeled`, `locked`, `unlocked`, `milestoned`, `demilestoned`, `auto_merge_enabled`, `auto_merge_disabled`, `converted_to_draft`, `ready_for_review`, `enqueued`, `dequeued`, `review_requested`, `review_request_removed`

### Payload structure

```json
{
  "action": "opened",
  "number": 42,
  "pull_request": { /* full PR object — same fields as REST API response */ },
  "repository": { "full_name": "owner/repo", ... },
  "sender": { "login": "username", ... }
}
```

The `pull_request` object in the webhook payload contains full PR detail. **You do not need a follow-up API call** for `opened`, `edited`, `closed`, or `reopened` events — the payload has everything needed to embed and index.

### What's NOT in the webhook payload

- File paths changed (need `GET /pulls/{number}/files`)
- Commit messages (need `GET /pulls/{number}/commits`)
- Review comments (separate `pull_request_review_comment` event)

These are out of scope for v1.

---

## Rate limits

- **Authenticated requests:** 5,000 requests/hour
- **Secondary rate limits:** triggered by creating content too quickly — not relevant for reads
- On a 429 response: check the `Retry-After` or `X-RateLimit-Reset` header and sleep until then
- The `X-RateLimit-Remaining` response header shows requests left in the current window

For backfill of 100 PRs across a few repos: well within limits. Not a concern until scaling to many repos.

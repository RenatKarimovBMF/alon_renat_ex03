# API Cost Breakdown — real `--live` runs

Static record kept as submission evidence; `docs/COST.md` is auto-generated on
every run ($0.00 in the default offline-fixtures mode). Each live run also
writes its own `session/COST.md` inside its `examples/<topic>-<stamp>/` folder.

## Final run — Claude Opus 4.8 ($0.5019) ✓ kept in `examples/`

**Session:** `6b331193` · `examples/the_moon_race_ussr_vs_us-20260612-233248/`
· 20-sheet PDF, **16 subject pages** (hard ≥15 rule met), 5,038 words
(every section 405–443), **all 8 sources cited**, 0 unresolved citations,
Hebrew summaries with correct LTR digits (1961 renders as 1961).

| Agent | Model | Calls | Input tokens | Output tokens | Est. USD |
|-------|-------|------:|-------------:|--------------:|---------:|
| chapter_writer | claude-opus-4-8 | 1 | 5,411 | 11,754 | $0.3209 |
| outline_architect | claude-opus-4-8 | 1 | 3,706 | 3,640 | $0.1095 |
| research_director | claude-opus-4-8 | 2 | 3,169 | 2,224 | $0.0714 |

**Total: $0.5019** · 12,286 input · 17,618 output tokens.

## Failed / superseded test runs (folders deleted; costs recorded here)

| Run | Result | Cost | Lesson |
|-----|--------|-----:|--------|
| Opus 4.8 #1 | timed out client-side at the old hard-coded 120 s HTTP timeout; billed server-side, never logged | ~$0.5 (est.) | timeout moved to `rate_limits.json: timeout_seconds = 600` |
| Opus 4.8 #2 (`5b8f0376`) | 13 subject pages — writer ignored the soft "320–400 words" instruction (~280/section) | $0.5993 | prompts need explicit floors, not ranges |
| Opus 4.8 #3 (`7c7628c6`) | 15 subject pages but its PDF carried the reversed-digit Hebrew bug (1961 → 1691) | $0.4661 | digits/Latin runs in RTL need `\beginL…\endL` islands |
| Opus 4.8 #4 (`b49e9a58`) | 14 subject pages (~339 words/section, one source uncited) | $0.7628 | per-paragraph word contract (5 × 80–95) finally sticks |
| max_tokens probe | confirmed `claude-opus-4-8` accepts a 64,000-token output ceiling | $0.0002 | ceiling ≠ purchase; only generated tokens bill |

**Total real Anthropic spend for this exercise: ≈ $2.8** (well inside the $20
test budget).

## Free-tier run — Gemini 3.1 Flash Lite ($0.00 actual)

**Session:** `719d0721` · billed $0.00 on the AI Studio free tier; paid-rate
equivalent ≈ $0.0223 (5,369 input · 5,641 output tokens; same pipeline,
sparser prose).

## Observations (cost-optimization notes per Guidelines §11)

- Output tokens dominate (Opus output is 5× input price); the writer stage is
  ~60–75% of every run. Splitting the writer per chapter would cap per-call
  output and reduce truncation risk at similar total cost.
- `ANTHROPIC_MAX_TOKENS` is a per-response output *ceiling*, not a purchase —
  set high (64K, probe-verified) so book-length JSON is never truncated; the
  gatekeeper budget still caps the number of calls per run.
- LLMs systematically undershoot word targets: a range ("320–400 words")
  yielded ~280; an explicit per-paragraph contract ("5 paragraphs of 80–95
  words each, recount before returning") yielded 405–443. Prompt-level length
  contracts are cheaper than retry loops.
- The free-tier Flash run produced a structurally valid book for $0; Opus
  produced richer prose that met the 15-subject-page floor. Drafting cheap and
  polishing strong is the obvious optimization.
- Every call is routed through `ApiGatekeeper` (budget guard + paced calls +
  retry on 429/5xx/timeouts) and logged as JSONL, from which these tables are
  generated.

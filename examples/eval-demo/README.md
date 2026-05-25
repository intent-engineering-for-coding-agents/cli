# eval-demo: Agent Evaluation A/B Example

This directory is the working example for the [Agent Evaluation and Regression](https://ase-book.dev/quality/agent-evaluation) chapter.

It shows how a single line added to `AGENTS.md` — "Prefer functions over classes for utility code" — caused an agent to drift away from the team's architectural conventions over the course of a week. The drift was invisible in code review. The eval suite caught it.

## Structure

```
eval-demo/
├── eval/                    # the eval suite (same tasks run against both states)
│   ├── 01-service-architecture/
│   ├── 02-test-traceability/
│   └── 03-documentation/
├── baseline/                # agent output with the correct AGENTS.md
│   ├── AGENTS.md
│   ├── src/user_service.py
│   ├── tests/test_user_service.py
│   └── docs/INDEX.md
├── after-drift/             # agent output after the AGENTS.md change
│   ├── AGENTS.md
│   ├── src/user_service.py
│   ├── tests/test_user_service.py
│   └── docs/INDEX.md
├── score-baseline.txt       # pre-committed: ase eval output for baseline
└── score-after-drift.txt    # pre-committed: ase eval output for after-drift
```

## Running it yourself

From this directory:

```bash
ase eval --path baseline --eval-dir eval
ase eval --path after-drift --eval-dir eval
```

Compare the output to `score-baseline.txt` and `score-after-drift.txt`.

## What the AGENTS.md change was

The team added one line to `AGENTS.md`:

```
Prefer functions over classes for utility code
```

It sounded reasonable. Over the following week, the agent started rewriting service classes into standalone functions, stopped placing validation in the service layer, and dropped `@pytest.mark.ac` markers from tests because the function-based style it was following did not use them. Each PR looked plausible. The eval suite caught the pattern on the next configuration change.

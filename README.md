# Sushi Go Round: moderate neural policy

**Day 1 passed in a live CrazyGames run on November 3, 2026.** The game displayed
**YOU WIN!**, ¥1,140 earned, 23 customers served, 2 lost, and 4 unhappy.
See [the result](evaluations/moderate-day1-win.png).

The new candidate-scoring network has **69,121 float32 parameters** (11 → 256 →
256 → 1, ReLU hidden layers), about 270 KiB of weights. It was initialized from
scratch with seed 42 and fitted using NumPy and Adam to 8,192 synthetic examples
of a hand-written strategy. No pretrained weights or reinforcement learning were
used. This is a small neural policy by modern standards, substantially larger than
the previous 11-coefficient ranker.

Perception is still hand-coded pixel recognition, with explicit recipe legality,
inventory estimates, pending-food tracking, and browser clicks. The network scores
legal candidate actions; it does not see raw pixels. The successful run used the
model for decisions and normal browser clicks, without changing game internals.
Assistant-operated tools started the game and executed batches of decisions.

Two live attempts were made with this model. The first exceeded the money target
but ended without advancing. Before the second attempt, pending-food expiry was
shortened to 18 seconds and a 5-second plate-clearing cooldown was added. The second
attempt passed. This is one verified success, not an established success rate.
The original failed agent report is preserved in
[evaluations/previous-agent-report.md](evaluations/previous-agent-report.md).

## Run

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
# Recreate weights from random initialization:
VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -m sushi_policy.neural
# Synthetic checks (not a substitute for live evaluation):
.venv/bin/python evaluations/check_neural.py
# One screenshot to one action:
.venv/bin/python -m sushi_policy.auto /absolute/path/screenshot.png
```

The included `sushi_policy/moderate.npz` is ready for inference. Move aside
`evaluations/auto-state.json` before starting a new Day 1. The command updates this
runtime memory when selecting actions; execute returned clicks successfully before
the next observation. Recipe actions require about 1.1 seconds to roll; phone-menu
clicks need about 300 ms between clicks. The host-tool browser loop is included in
`evaluations/browser-harness.js`; it requires T3 preview and shell tools.

Coordinates assume a 1280×800 CrazyGames viewport and the game at x216–775,
y76–496. Resizing or scrolling requires recalibration. Missed clicks, imperfect
order classification, and stock-estimate drift remain limitations. In particular,
the policy has no terminal-screen detector: stop the loop when the day ends.

## Files

- `sushi_policy/neural.py`: model, deterministic synthetic training, inference.
- `sushi_policy/moderate.npz`: trained weights.
- `sushi_policy/auto.py`: observation memory and action selection.
- `sushi_policy/adapter.py`: recipes, legal actions, click coordinates.
- `sushi_policy/vision.py`: pixel-based observation.
- `evaluations/moderate-summary.json`: live outcome and training provenance.
- `evaluations/auto-decisions.jsonl`: decisions from both moderate-model attempts.

The old linear model and its historical evaluation files remain available.

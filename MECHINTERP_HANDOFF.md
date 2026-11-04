Build a mechanistic interpretability solution on top of this repository's moderate-sized model for https://www.crazygames.com/game/sushi-go-round, and get past the first day.

Starting point:
- Read README.md and inspect the implementation before making changes.
- sushi_policy/moderate.npz contains a 69,121-parameter ReLU MLP (11 → 256 → 256 → 1). sushi_policy/neural.py implements training and inference in NumPy.
- The network was initialized from scratch and trained with Adam to imitate a known linear teacher on synthetic feature vectors. It was not trained with game rewards. Hand-coded perception and state tracking feed candidate-action features to the network.
- One live Day 1 pass is documented in evaluations/moderate-day1-win.png and evaluations/moderate-summary.json: ¥1,140 earned, 23 served, 2 lost, 4 unhappy. A prior attempt failed. No mechanistic interpretability analysis has been done.

Your job is to explain causally how this network implements its action scoring, then demonstrate that the analyzed model can still clear Day 1. Preserve the existing checkpoint as a baseline; a larger or newly trained model is optional, not a substitute for interpreting this one.

Required work:
1. Reproduce inference and characterize the network on realistic candidate features from recorded decisions plus controlled feature sweeps. Compare predictions and local input gradients against the known teacher, including feature interactions and out-of-distribution behavior. Distinguish behavioral sensitivity from internal mechanistic evidence.
2. Capture hidden preactivations/activations and examine paths from named input features through both hidden layers to the output. Identify a small set of candidate neurons or distributed directions responsible for meaningful decisions such as serving orders, avoiding duplicates, clearing plates, and refilling supplies. Do not infer importance from weight magnitude alone.
3. Test those hypotheses with causal interventions: neuron/path ablations or activation patching on paired observations. Measure effects on scores, action margins, and selected actions. Include matched random-ablation controls and held-out cases. Report redundancy, failures, and uncertainty; do not claim a neat circuit if the evidence supports a distributed implementation.
4. Separate what the network controls from what explicit legality masks, perception, inventory memory, and click logic enforce. In particular, duplicate avoidance is also enforced outside the network. Test the network's preference separately from the complete agent's masked choice.
5. Produce reproducible analysis scripts, saved measurements, and a clear report with figures linking specific internal components to causally verified effects. Record exact checkpoint hashes, seeds, feature distributions, and intervention definitions. State whether the explanation is local or general.
6. Run the analyzed baseline or an explicitly identified revised checkpoint in the actual CrazyGames game using normal gameplay actions. Do not modify cash, timers, inventory, customers, reputation, or win conditions. Save a YOU WIN result and confirm advancement to Day 2. Document attempts and any manual assistance honestly. Stop the automation at terminal screens. If live access is blocked, report the blocker and do not claim a new pass from the historical screenshot.

Keep runtime tracking fixes distinct from neural weight changes. If you retrain, preserve and compare checkpoints and repeat the causal analysis for the checkpoint used in the final successful run. Aim for a compact, evidence-backed explanation of what actually drives this agent's decisions, not just an activation visualization or a restatement of the teacher formula.

# Experiment Results

| Run | Description | Easy Pass | Hard Pass | Easy % | Hard % | Cost ($) | Log Dir |
|-----|-------------|-----------|-----------|--------|--------|----------|---------|
| 0 | Baseline (submit_answer only, temp=0.6) | 0/64 | 0/64 | 0.0% | 0.0% | $0.04 | `logs/run_20260510_053738/` |
| 1 | Phase 1: db+guide tools, BM25, new prompt, temp=0.1, compress | 40/64 | 25/64 | 62.5% | 39.1% | $0.65 | `logs/run_20260510_054527/` |
| 2 | Add search_columns tool (REGRESSION — reverted) | 31/64 | 18/64 | 48.4% | 28.1% | $0.39 | `logs/run_20260510_055406/` |

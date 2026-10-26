# Fact check: Google Research, "Towards a science of scaling agent systems" (arXiv 2512.08296)

Checked by doc-checker on 2026-10-24 against the arXiv HTML for v1 (9 Dec 2025) and v3 (8 Apr 2026), the v2 abstract, and the Google Research blog (28 Jan 2026). The PDF was not read.

## Versions differ

The page's counts (180 configurations, 4 benchmarks, +80.9%) match v1 and the blog. v3 reports 260 configurations, 6 benchmarks and +80.8%. It keeps the original four as a subset, with numbers within about 0.1 point. The page should name the version it plots: v1, December 2025.

## Verdicts on the page's claims

| Claim | Verdict | Note |
|---|---|---|
| 180 configurations | PARTLY | v1 and blog yes; v3 says 260 |
| 4 benchmarks, 3 model families | PARTLY | v1 yes; v3 says 6 benchmarks |
| Finance, centralized +80.9% | TRUE | v1 §4.2; v3 +80.8% |
| Web navigation, decentralized +9.2% | TRUE | best case on BrowseComp-Plus; Independent is −35% on the same benchmark |
| Planning, best −39%, worst −70% | TRUE | PlanCraft: Hybrid −39.0%, Independent −70.0% |
| Gains turn negative above about 45% | PARTLY | v1 says "diminishing or negative" above an empirical threshold of ~45%. This is a fitted crossover, not an observed cliff. v3 says only "diminishing". Workbench (single-agent 0.629) still gains +5.7% |
| Independent 17.2× vs centralized 4.4× errors | TRUE | Both are relative to a single agent (=1.0). These are architecture-level constants, not per-benchmark figures |

## Per-benchmark results (v1)

All values are relative change in mean success versus the single-agent mean, across the three model families combined. Values marked ≈ are rounded labels from the paper's Figure 2.

| Benchmark (task) | Single-agent baseline | Best multi-agent | Worst multi-agent |
|---|---|---|---|
| Finance-Agent (financial reasoning) | 0.349 | Centralized +80.9% | Independent ≈ +57% |
| BrowseComp-Plus (web navigation) | 0.318 | Decentralized +9.2% | Independent ≈ −35% |
| Workbench (workflows and tools) | 0.629 | Decentralized +5.7% | Independent ≈ −11% |
| PlanCraft (step-by-step planning) | 0.568 | Hybrid −39.0% | Independent −70.0% |

Figure 2 labels for all four setups (rounded):

| Benchmark | Independent | Decentralized | Centralized | Hybrid |
|---|---|---|---|---|
| Finance Agent | +57% | +75% | +81% | +73% |
| Workbench | −11% | +6% | −1% | −1% |
| BrowseComp-Plus | −35% | +9% | +0% | +6% |
| PlanCraft | −70% | −41% | −50% | −39% |

Sample sizes are small: 50 Finance questions, 100 BrowseComp-Plus tasks and 100 Workbench scenarios. The overall mean multi-agent change was −3.5% (95% CI −18.6% to +25.7%) in v1.

Sources:
- https://arxiv.org/abs/2512.08296v1
- https://arxiv.org/html/2512.08296v3
- https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/

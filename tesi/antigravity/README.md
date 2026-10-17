# BlueAgent Testing & Evaluation Source Repository

This directory serves as the centralized empirical and analytical source repository for the validation, benchmarking, and experimental evaluation of **BlueAgent**.

---

## Directory Taxonomy

```
antigravity/
├── context.md               # AI Engineer System Context & Resource Navigation Index
├── README.md                # This directory index and testing taxonomy
│
├── notes/                   # Analytical writeups and chapter drafts
│   ├── thesis_notes.md      # Quantitative scaling tables, speedup factors, memory density
│   ├── thesis_evaluation_chapter.md # Draft text for Chapter 5 (Experimental Evaluation)
│   ├── walkthrough.md       # Synchronized 6-barrier methodology & CPU/RAM sampler validation
│   └── implementation_plan.md # Original execution plan for the benchmark suite
│
├── data/                    # Empirical evaluation datasets
│   ├── raw/                 # High-frequency 100ms time-series (~20,000 samples)
│   │   ├── thesis_alpine_raw_samples.csv
│   │   ├── thesis_alpine_timeseries.csv
│   │   ├── thesis_ubuntu_raw_samples.csv
│   │   └── thesis_ubuntu_timeseries.csv
│   ├── processed/           # Aggregated barrier metrics & step resource consumption
│   │   ├── thesis_alpine_results.csv
│   │   ├── thesis_alpine_step_resources.csv
│   │   ├── thesis_ubuntu_results.csv
│   │   └── thesis_ubuntu_step_resources.csv
│   └── reports/             # Generated test run reports and state JSONs
│       ├── thesis_alpine_report.md
│       ├── thesis_alpine_state.json
│       ├── thesis_ubuntu_report.md
│       └── thesis_ubuntu_state.json
│
├── scripts/                 # Benchmark runners and telemetry tools
│   ├── benchmark_suite.py   # 9-scenario scaling matrix runner (up to 100 containers)
│   ├── resource_sampler.py  # 100ms background CPU/RAM subprocess sampler
│   ├── plot_thesis_graphs.py # Publication graph generator
│   ├── plot_graphs_3_4_5.py # Telemetry scaling and lifecycle timeline generator
│   └── helpers/             # Testing API routes and challenge helpers
│       ├── api_challenges.py
│       ├── services_challenges.py
│       └── client.py
│
└── figures/                 # Publication-ready vector and raster evaluation figures
    ├── graph1_cow_vs_deploy.{pdf,png}
    ├── graph2_microphase_breakdown.{pdf,png}
    ├── graph3_memory_scaling.{pdf,png}
    ├── graph4_lifecycle_timeline.{pdf,png}
    └── graph5_step_cpu_iowait.{pdf,png}
```

---

## Key Experimental Findings Summary

1. **ZFS CoW Scaling Advantage:** At peak concurrency ($M=10, N=5$, 100 concurrent instances), cloning running instances (`22.17s`) is **$3.44\times$ faster** than cold provisioning (`76.19s`), preserving over 80% of round scoring windows.
2. **Container Footprint:** Lightweight Alpine idles at **~15.3 MB/ct**; full Ubuntu Heavy instances (with systemd, PostgreSQL 16, Nginx, Python) idle at **~52.5 MB/ct**. 100 concurrent Ubuntu instances fit in 9.23 GiB host RAM with 0 swap.

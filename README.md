# COMP7507 Visualization & Visual Analytics — Group Project

**Topic: The AI Race (2023–2026)** — visual analysis of the LLM frontier:
Arena leaderboard evolution, open vs. closed models, US–China competition,
and the market response to model releases.

Course project requirements: see `comp7507-project-requirements (2026-27 sem 1).html`.
Topic brainstorming / dataset inventory: see `COMP7507-项目构思.md` and `数据集盘点与选题分析.md`.

## Repository structure

```
datasets/
├── AI Index Report/        # Stanford AI Index 2026 raw data (9 chapters, CSV, unzipped + original zips)
├── lmarena-leaderboard/    # Arena leaderboard historical snapshots (23 categories x full/latest, parquet)
├── lmarena-arena55k/       # Arena human preference battles 2023-2024 (train.csv.zip)
├── lmarena-arena140k/      # Arena human preference battles 2024-2025 (see note below, ~1.5 GB)
└── yfinance/               # Daily stock prices of 22 AI-related tickers (2015-2026-09), prices_all.csv
download_hf.py              # Script that downloads the Hugging Face datasets
fetch_yfinance.py           # Script that re-fetches the stock data via yfinance
explore_hf.py / explore_hf2.py  # Quick data exploration scripts (schema, stats)
openalex-group-by-20260913.csv  # OpenAlex AI publications aggregation
```

## Getting the large datasets (important)

GitHub rejects files larger than 100 MB, so the biggest files are not stored here directly:

1. **arena-human-preference-140k** (7 parquet files, ~1.5 GB) — not in the repo.
   Download it with:
   ```bash
   python download_hf.py
   ```
   This downloads the leaderboard dataset, the 55k CSV and the 140k parquet files
   from Hugging Face (all public, no account needed) into `datasets/`.

2. **arena-human-preference-55k** (`train.csv`, 176 MB) — stored as `train.csv.zip` (56 MB).
   Unzip it with any tool, or:
   ```bash
   python -c "import zipfile; zipfile.ZipFile('datasets/lmarena-arena55k/train.csv.zip').extractall('datasets/lmarena-arena55k')"
   ```

## Data sources

| Dataset | Source | Notes |
|---|---|---|
| Stanford AI Index 2026 | https://hai.stanford.edu/ai-index/2026-ai-index-report | Raw Data button → official CSVs |
| Arena Leaderboard Dataset | https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset | CC-BY-4.0, no account needed |
| Arena Human Preference 55k | https://huggingface.co/datasets/lmarena-ai/arena-human-preference-55k | Apache-2.0 |
| Arena Human Preference 140k | https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k | CC-BY-4.0 |
| Stock prices | Yahoo Finance via `yfinance` (Python) | daily, auto-adjusted |
| OpenAlex | https://openalex.org/ | AI publications aggregation |

# -*- coding: utf-8 -*-
"""Explore downloaded datasets: schema, sizes, dates, top models."""
import os
import pandas as pd
import pyarrow.parquet as pq

ROOT = r"C:\Users\86136\Desktop\hku\7507\datasets"

# ---------- 1. leaderboard text/full ----------
p = os.path.join(ROOT, "lmarena-leaderboard", "text", "full-00000-of-00001.parquet")
df = pd.read_parquet(p)
print("=== lmarena leaderboard: text/full ===")
print("rows:", len(df))
print("cols:", list(df.columns))
print("publish_date range:", df["leaderboard_publish_date"].min(), "->", df["leaderboard_publish_date"].max())
print("unique dates:", df["leaderboard_publish_date"].nunique())
print("unique models:", df["model_name"].nunique(), "| orgs:", df["organization"].nunique())
print("licenses:", sorted(df["license"].dropna().unique()))
print("categories:", sorted(df["category"].dropna().unique()))
latest = df[df["leaderboard_publish_date"] == df["leaderboard_publish_date"].max()].sort_values("rank")
print("\nlatest snapshot top 12 (text):")
print(latest[["rank", "model_name", "organization", "license", "rating", "vote_count"]].head(12).to_string(index=False))

# ---------- 2. leaderboard other configs: date spans ----------
print("\n=== other configs (full): rows / date span ===")
for cfg in ["text_style_control", "text_factuality", "vision", "search", "webdev", "agent"]:
    fp = os.path.join(ROOT, "lmarena-leaderboard", cfg, "full-00000-of-00001.parquet")
    if os.path.exists(fp):
        d = pd.read_parquet(fp, columns=["leaderboard_publish_date", "model_name"])
        print(f"{cfg:<20} rows={len(d):>8} dates={d['leaderboard_publish_date'].min()} -> {d['leaderboard_publish_date'].max()} models={d['model_name'].nunique()}")

# ---------- 3. arena 55k ----------
print("\n=== arena-human-preference-55k (train.csv) ===")
c55 = pd.read_csv(os.path.join(ROOT, "lmarena-arena55k", "train.csv"), nrows=200)
print("cols:", list(c55.columns))
print("sample rows:")
print(c55[["model_a", "model_b", "winner_model_a", "winner_model_b"]].head(5).to_string(index=False))
import ast
def tstamp(s):
    try: return pd.to_datetime(s, unit="s")
    except Exception: return pd.NaT
ts = pd.to_datetime(c55["tstamp"], unit="s", errors="coerce")
print("tstamp range (first 200 rows):", ts.min(), "->", ts.max())

# ---------- 4. arena 140k (first shard) ----------
print("\n=== arena-human-preference-140k (shard 0) ===")
p140 = os.path.join(ROOT, "lmarena-arena140k", "data", "train-00000-of-00007.parquet")
d140 = pd.read_parquet(p140)
print("rows:", len(d140))
print("cols:", list(d140.columns))
print("timestamp range:", d140["timestamp"].min(), "->", d140["timestamp"].max())
print("unique models:", d140["model_a"].nunique() + d140["model_b"].nunique() if True else 0)
print("winner values:", d140["winner"].value_counts().head(6).to_dict())
print("languages:", d140["language"].value_counts().head(6).to_dict())

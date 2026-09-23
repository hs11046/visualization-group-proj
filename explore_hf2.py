# -*- coding: utf-8 -*-
"""Follow-up stats for the summary report."""
import os
import pandas as pd

ROOT = r"C:\Users\86136\Desktop\hku\7507\datasets"

# ---------- 140k shard 0 ----------
p140 = os.path.join(ROOT, "lmarena-arena140k", "train-00000-of-00007.parquet")
d = pd.read_parquet(p140, columns=["model_a", "model_b", "winner", "language", "timestamp", "is_code"])
print("=== arena140k shard0 ===")
print("rows:", len(d))
print("timestamp:", d["timestamp"].min(), "->", d["timestamp"].max())
print("winner dist:", d["winner"].value_counts(dropna=False).head(6).to_dict())
models = pd.unique(pd.concat([d["model_a"], d["model_b"]]))
print("distinct models (shard):", len(models))
print("languages:", d["language"].value_counts().head(6).to_dict())
print("is_code share:", round(d["is_code"].mean(), 4))

# ---------- 55k full stats ----------
print("\n=== arena55k full ===")
c = pd.read_csv(os.path.join(ROOT, "lmarena-arena55k", "train.csv"),
                usecols=["model_a", "model_b", "winner_model_a", "winner_model_b", "winner_tie"])
print("rows:", len(c))
ma = pd.unique(pd.concat([c["model_a"], c["model_b"]]))
print("distinct models:", len(ma))
print("tie share:", round(c["winner_tie"].mean(), 4))
print("top models by appearances:")
print(pd.concat([c["model_a"], c["model_b"]]).value_counts().head(8).to_string())
wins = pd.concat([c.loc[c["winner_model_a"] == 1, "model_a"], c.loc[c["winner_model_b"] == 1, "model_b"]])
print("top models by wins:")
print(wins.value_counts().head(8).to_string())

# ---------- leaderboard text/full aggregates ----------
print("\n=== leaderboard text/full aggregates ===")
lb = pd.read_parquet(os.path.join(ROOT, "lmarena-leaderboard", "text", "full-00000-of-00001.parquet"))
lb["dt"] = pd.to_datetime(lb["leaderboard_publish_date"])
print("rows per year:")
print(lb.groupby(lb["dt"].dt.year).size().to_string())
ov = lb[lb["category"] == "overall"]
last = ov["dt"].max()
print("\nlatest overall top 10:", last.date())
top = ov[ov["dt"] == last].sort_values("rank").head(10)
print(top[["rank", "model_name", "organization", "license", "rating", "vote_count"]].to_string(index=False))
first = ov["dt"].min()
print("\nearliest overall top 10:", first.date())
top0 = ov[ov["dt"] == first].sort_values("rank").head(10)
print(top0[["rank", "model_name", "organization", "license", "rating", "vote_count"]].to_string(index=False))

def lic_type(x):
    x = str(x)
    if "Proprietary" in x: return "Proprietary"
    if not x.strip() or x == "nan": return "Unknown"
    return "Open-ish"
print("\nlicense type share (latest overall snapshot):", top.assign(t=top["license"].apply(lic_type))["t"].value_counts().to_dict())

# votes scale
print("total votes (sum vote_count, text full):", int(lb["vote_count"].sum()))
print("orgs with most rows (text full):")
print(lb["organization"].value_counts().head(10).to_string())

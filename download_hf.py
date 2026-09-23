# -*- coding: utf-8 -*-
"""Download HF datasets: leaderboard-dataset (46 parquet), arena 55k CSV, arena 140k (7 parquet)."""
import urllib.request
import os
import sys
import threading
import time

ROOT = r"C:\Users\86136\Desktop\hku\7507\datasets"
BASE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}?download=true"

LB_DIRS = [
    "agent", "agent_bash_recovery_steps", "agent_praise_complaint",
    "agent_steerability", "agent_task_outcome_explicit", "agent_tool_hallucination",
    "document", "document_style_control", "image_edit", "image_to_video",
    "search", "search_factuality", "search_style_control", "text",
    "text_factuality", "text_style_control", "text_to_image", "text_to_video",
    "video_edit", "vision", "vision_style_control", "webdev",
]

jobs = []
for d in LB_DIRS:
    for split in ("full", "latest"):
        jobs.append((f"lmarena-ai/leaderboard-dataset",
                     f"{d}/{split}-00000-of-00001.parquet",
                     os.path.join(ROOT, "lmarena-leaderboard", d)))
jobs.append(("lmarena-ai/arena-human-preference-55k", "train.csv",
             os.path.join(ROOT, "lmarena-arena55k")))
for i in range(7):
    jobs.append(("lmarena-ai/arena-human-preference-140k",
                 f"data/train-{i:05d}-of-00007.parquet",
                 os.path.join(ROOT, "lmarena-arena140k")))

results = []
lock = threading.Lock()

def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f}{unit}"
        n /= 1024

def dl(repo, path, outdir):
    os.makedirs(outdir, exist_ok=True)
    dest = os.path.join(outdir, os.path.basename(path))
    tmp = dest + ".part"
    url = BASE.format(repo=repo, path=path)
    for attempt in range(4):
        try:
            if os.path.exists(dest) and os.path.getsize(dest) > 0:
                with lock:
                    results.append(("skip", repo, path))
                return
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as f:
                total = 0
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk:
                        break
                    f.write(chunk)
                    total += len(chunk)
            os.replace(tmp, dest)
            with lock:
                results.append(("ok", repo, path, total))
                print(f"[ok] {path}  {human(total)}", flush=True)
            return
        except Exception as e:
            if os.path.exists(tmp):
                try: os.remove(tmp)
                except OSError: pass
            if attempt == 3:
                with lock:
                    results.append(("FAIL", repo, path, str(e)))
                    print(f"[FAIL] {path}: {e}", flush=True)
                return
            time.sleep(3 * (attempt + 1))

threads = []
sem = threading.Semaphore(6)
def worker(j):
    with sem:
        dl(*j)
for j in jobs:
    t = threading.Thread(target=worker, args=(j,), daemon=True)
    t.start()
    threads.append(t)
for t in threads:
    t.join()

ok = sum(1 for r in results if r[0] == "ok")
skip = sum(1 for r in results if r[0] == "skip")
fail = sum(1 for r in results if r[0] == "FAIL")
print(f"\nDONE ok={ok} skip={skip} fail={fail} total={len(jobs)}", flush=True)
for r in results:
    if r[0] == "FAIL":
        print("FAILED:", r[1], r[2], r[3], flush=True)

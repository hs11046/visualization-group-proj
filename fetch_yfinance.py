# -*- coding: utf-8 -*-
"""Download AI-related stock/ETF price history via yfinance -> CSV."""
import os
import pandas as pd
import yfinance as yf

OUT = r"C:\Users\86136\Desktop\hku\7507\datasets\yfinance"
os.makedirs(OUT, exist_ok=True)

TICKERS = {
    # GPU / chips
    "NVDA": "NVIDIA", "AMD": "AMD", "TSM": "TSMC", "AVGO": "Broadcom",
    "MU": "Micron", "INTC": "Intel", "SMCI": "Super Micro", "ARM": "Arm",
    # Hyperscalers / big tech
    "MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon",
    "META": "Meta", "ORCL": "Oracle", "AAPL": "Apple",
    # AI software / pure play
    "PLTR": "Palantir", "AI": "C3.ai", "SNOW": "Snowflake",
    "CRM": "Salesforce", "NOW": "ServiceNow",
    # AI ETFs
    "BOTZ": "Robotics&AI ETF", "AIQ": "AI&Tech ETF", "ROBT": "AI ETF",
}
START = "2015-01-01"

frames = []
errors = []
for tk, name in TICKERS.items():
    try:
        df = yf.download(tk, start=START, interval="1d", auto_adjust=True,
                         progress=False, threads=False)
        if df is None or len(df) == 0:
            errors.append((tk, "empty"))
            print(f"[EMPTY] {tk}", flush=True)
            continue
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df.reset_index()
        df.insert(1, "ticker", tk)
        df.insert(2, "name", name)
        path = os.path.join(OUT, f"prices_{tk}.csv")
        df.to_csv(path, index=False)
        frames.append(df)
        print(f"[ok] {tk:<6} {len(df):>5} rows  {df['Date'].min().date()} -> {df['Date'].max().date()}", flush=True)
    except Exception as e:
        errors.append((tk, str(e)[:120]))
        print(f"[FAIL] {tk}: {str(e)[:120]}", flush=True)

if frames:
    all_df = pd.concat(frames, ignore_index=True)
    all_df.to_csv(os.path.join(OUT, "prices_all.csv"), index=False)
    print(f"\nTOTAL rows={len(all_df)} tickers={all_df['ticker'].nunique()}", flush=True)
    print("last date:", all_df["Date"].max(), flush=True)
    for tk, err in errors:
        print("ERR:", tk, err, flush=True)
else:
    print("NO DATA", flush=True)

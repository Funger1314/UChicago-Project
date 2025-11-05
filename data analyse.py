
import re
from typing import Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = "real_estate_data_chicago.csv"
"""
Return the first column name that regex-matches any candidate (case-insensitive).
"""
def pick_col(candidates, columns):
    pattern = re.compile("|".join([re.escape(x) for x in candidates]), flags=re.IGNORECASE)
    for col in columns:
        if pattern.search(col):
            return col
    return None

df = pd.read_csv(CSV_PATH) #load data
date_col = pick_col(["date", "sold", "list", "closing"], df.columns) # Parse one likely date column
if date_col is not None:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

# Coerce typical numeric columns
for guess in [["price", "sale_price", "list_price"],
              ["sqft", "square", "area"],
              ["beds", "bedrooms"],
              ["baths", "bathrooms"]]:
    col = pick_col(guess, df.columns)
    if col is not None:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# One likely categorical column
cat_col = pick_col(["neigh", "zip", "community", "type"], df.columns)
if cat_col is not None:
    df[cat_col] = df[cat_col].astype("category")

# Feature engineering: price_per_sqft
price_col = pick_col(["price", "sale_price", "list_price"], df.columns)
sqft_col  = pick_col(["sqft", "square", "area"], df.columns)
if price_col and sqft_col:
    df["price_per_sqft"] = df[price_col] / df[sqft_col]

#Data processing
# Basic cleaning
if price_col:
    df = df[df[price_col] > 1]
if sqft_col:
    df = df[df[sqft_col] > 50]

# Clip extreme outliers for robustness
if "price_per_sqft" in df.columns:
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df[df["price_per_sqft"].notna()]
    lo, hi = df["price_per_sqft"].quantile([0.01, 0.99])
    df["price_per_sqft_clipped"] = df["price_per_sqft"].clip(lo, hi)

#analysis function
#Compute robust summary stats for `metric`. If `by` exists, return grouped stats. Returns columns: count, mean, median, std, p25, p75
def analyze_metric(frame: pd.DataFrame, metric: str, by: Optional[str] = None) -> pd.DataFrame:
    if by is not None and by in frame.columns:
        grp = frame.groupby(by, dropna=False)[metric]
        return grp.agg(
            count="count",
            mean="mean",
            median="median",
            std="std",
            p25=lambda s: s.quantile(0.25),
            p75=lambda s: s.quantile(0.75),
        ).reset_index()
    s = frame[metric].dropna()
    return pd.DataFrame({
        "count": [s.count()],
        "mean":  [s.mean()],
        "median":[s.median()],
        "std":   [s.std()],
        "p25":   [s.quantile(0.25)],
        "p75":   [s.quantile(0.75)],
    })

#Choose metric & run analysis
metric_for_analysis = (
    "price_per_sqft_clipped" if "price_per_sqft_clipped" in df.columns
    else (price_col if price_col else (sqft_col if sqft_col else df.select_dtypes(include=[np.number]).columns[0]))
)
group_for_analysis = cat_col if (cat_col in df.columns) else None
summary_df = analyze_metric(df, metric_for_analysis, group_for_analysis)

#Inspect outputs
print("=== DATA PREVIEW (head) ===")
print(df.head(8).to_string(index=False))
print("\n=== SUMMARY STATS ===")
print(summary_df.head(12).to_string(index=False))

#Visualization (optional)
plt.figure()
plt.title(f"Distribution of {metric_for_analysis}")
plt.hist(df[metric_for_analysis].dropna(), bins=30)  # default colors
plt.xlabel(metric_for_analysis)
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

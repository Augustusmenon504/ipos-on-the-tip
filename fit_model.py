"""Fit the IPOs on the Tip listing-gain model.

Model: listing-open gain % = a + b * ln(1 + QIB subscription)
Run:   python model/fit_model.py   (needs numpy)
"""
import csv, math, pathlib
import numpy as np

rows = list(csv.DictReader(open(pathlib.Path(__file__).parent.parent / "data" / "ipos.csv")))
q = np.array([math.log1p(float(r["qib"])) for r in rows])
y = np.array([(float(r["listing_open"]) / float(r["issue_price"]) - 1) * 100 for r in rows])
X = np.column_stack([np.ones(len(q)), q])

a, b = np.linalg.lstsq(X, y, rcond=None)[0]
r2 = 1 - ((y - X @ [a, b]) ** 2).sum() / ((y - y.mean()) ** 2).sum()

# leave-one-out error vs. guessing the average
n = len(y); errs, base = [], []
for i in range(n):
    m = np.ones(n, bool); m[i] = False
    c = np.linalg.lstsq(X[m], y[m], rcond=None)[0]
    errs.append(abs(X[i] @ c - y[i])); base.append(abs(y[m].mean() - y[i]))

# forward test: train on 2024-25, predict 2026
tr = np.array([r["listing_date"] < "2026" for r in rows])
c = np.linalg.lstsq(X[tr], y[tr], rcond=None)[0]
fwd = np.abs(X[~tr] @ c - y[~tr]).mean()
fwd_base = np.abs(y[tr].mean() - y[~tr]).mean()

print(f"n={n}  gain% = {a:.2f} + {b:.3f} * ln(1+QIB)  R2={r2:.3f}")
print(f"leave-one-out MAE {np.mean(errs):.1f} pts (baseline {np.mean(base):.1f})")
print(f"forward test 2026: MAE {fwd:.1f} pts on {(~tr).sum()} IPOs (baseline {fwd_base:.1f})")

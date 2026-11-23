"""Risk-return analyzer.

Reads prices.csv (date,symbol,close), computes daily returns per symbol
and prints total return, annualised volatility, Sharpe ratio and
maximum drawdown.

Usage:
    python risk_return.py
    python risk_return.py --file prices.csv --risk-free 0.03
"""
import argparse
import csv
import math
from collections import defaultdict


def load(path):
    series = defaultdict(list)
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            series[row["symbol"]].append((row["date"], float(row["close"])))
    for symbol in series:
        series[symbol].sort()
    return series


def analyse(closes, risk_free=0.03):
    returns = []
    for i in range(1, len(closes)):
        prev, curr = closes[i - 1][1], closes[i][1]
        returns.append(curr / prev - 1)
    if len(returns) < 2:
        return None
    n = len(returns)
    mean = sum(returns) / n
    var = sum((r - mean) ** 2 for r in returns) / (n - 1)
    vol_daily = math.sqrt(var)
    vol_annual = vol_daily * math.sqrt(252)
    sharpe = (mean * 252 - risk_free) / vol_annual if vol_annual else 0.0
    total_return = closes[-1][1] / closes[0][1] - 1
    peak = closes[0][1]
    max_dd = 0.0
    for _, price in closes:
        peak = max(peak, price)
        max_dd = min(max_dd, price / peak - 1)
    return {
        "days": n,
        "total_return": total_return,
        "vol_annual": vol_annual,
        "sharpe": sharpe,
        "max_drawdown": max_dd,
    }


def main():
    p = argparse.ArgumentParser(description="Risk-return analyzer")
    p.add_argument("--file", default="prices.csv")
    p.add_argument("--risk-free", type=float, default=0.03,
                   help="Annual risk-free rate (0.03 = 3%)")
    a = p.parse_args()
    for symbol, closes in sorted(load(a.file).items()):
        r = analyse(closes, a.risk_free)
        if r is None:
            print(f"{symbol}: not enough data")
            continue
        print(f"{symbol}: {r['days']} trading days")
        print(f"  Total return:        {r['total_return']:+.2%}")
        print(f"  Annualised volatility: {r['vol_annual']:.2%}")
        print(f"  Sharpe ratio:          {r['sharpe']:.2f} (rf {a.risk_free:.0%})")
        print(f"  Max drawdown:          {r['max_drawdown']:.2%}")


if __name__ == "__main__":
    main()

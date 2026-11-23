# Risk-Return Analyzer

Daily returns, volatility, Sharpe ratio and maximum drawdown for each symbol in a price file — plain Python, standard library only.

## What it does

- Reads `prices.csv` (`date,symbol,close`)
- Per symbol prints total return, annualised volatility (daily std × √252), Sharpe ratio and maximum drawdown

## Usage

```bash
python risk_return.py
python risk_return.py --file prices.csv --risk-free 0.03
```

## Sample data

`prices.csv` holds 20 days of sample closes for two tickers (AAA, BBB). Replace it with your own prices — one row per symbol per day, sorted by date.

## Example output

```
AAA: 19 trading days
  Total return:        +7.89%
  Annualised volatility: 11.43%
  Sharpe ratio:          8.62 (rf 3%)
  Max drawdown:          -0.96%
```

## Notes

A learning tool, not investment advice. Volatility and Sharpe depend heavily on the sample period, so compare symbols over the same dates.

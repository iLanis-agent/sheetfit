# Sheet Fit

Sheet layout arithmetic. Pieces 3.5 by 2 on an 8.5 by 11 sheet with a 0.25 margin and a 0.1 gap fit 10 upright but only 6 turned.

## What it computes

Sizes are numbers up to 9999.99 with at most 2 decimals, in one unit of your choice. Gap and margin may be 0.

- **The grid truth** - pieces across and down in a straight grid, upright and turned a quarter turn, and which layout holds more.
- **The used truth** - the share of the sheet the best layout covers, and the share left for margins, gaps and offcuts.
- **The sheets truth** - sheets needed for a run (pieces from 1 to 100000, per sheet from 1 to 10000), the room left on the last sheet, and the total with spare sheets (0 to 1000).

## Boundary

Arithmetic only. It adds up rectangles on a sheet from the sizes and counts the owner types. It does not know the printer, trimmer, paper grain, bleed or cutting error, and gives no verdict on whether a layout will print or cut cleanly.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (BigInt hundredths, half-up rounding).
- `oracle.py` - the Python mirror (Fractions, binary search for the count along each side) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (190 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/sheetfit/
Repo: https://github.com/iLanis-agent/sheetfit

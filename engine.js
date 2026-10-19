// Sheet Fit engine: how many equal rectangles fit on a sheet in a grid, upright or turned, and how many sheets a run needs. Exact BigInt hundredths.
function _dec(t, name, zeroOk) {
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{1,4})(?:\.([0-9]{1,2}))?$/.exec(t);
  var err = "the " + name + " must be a number " + (zeroOk ? "from 0" : "above 0") + " and up to 9999.99, with at most 2 decimals";
  if (!m) throw new Error(err);
  var v = BigInt(m[1]) * 100n + BigInt((m[2] || "").padEnd(2, "0"));
  if (v === 0n && !zeroOk) throw new Error(err);
  return v;
}
function _int(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,6}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _fmt(v) {
  var s = (v / 100n).toString(), f = (v % 100n).toString();
  if (f.length < 2) f = "0" + f;
  f = f.replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _tenths(num, den) { // num/den rounded half up to tenths, shown with trailing .0 dropped
  var v = (2n * num + den) / (2n * den);
  var s = (v / 10n).toString(), f = (v % 10n).toString();
  return f === "0" ? s : s + "." + f;
}
function _plural(n, one, many) { return n + " " + (String(n) === "1" ? one : many); }
function _along(room, piece, gap) { return piece > room ? 0n : (room + gap) / (piece + gap); }

function _layout(sw, sh, pw, ph, g, m) {
  var rw = sw - 2n * m, rh = sh - 2n * m;
  if (rw <= 0n || rh <= 0n) throw new Error("the margins leave no room on the sheet");
  var a = _along(rw, pw, g), b = _along(rh, ph, g), c = _along(rw, ph, g), d = _along(rh, pw, g);
  return { a: a, b: b, up: a * b, c: c, d: d, turn: c * d };
}
function _read(sheetW, sheetH, pieceW, pieceH, gap, margin) {
  return {
    sw: _dec(sheetW, "sheet width", false), sh: _dec(sheetH, "sheet height", false),
    pw: _dec(pieceW, "piece width", false), ph: _dec(pieceH, "piece height", false),
    g: _dec(gap, "gap", true), m: _dec(margin, "margin", true)
  };
}
function _head(x) {
  return "Sheet " + _fmt(x.sw) + " by " + _fmt(x.sh) + ", margin " + _fmt(x.m) + ", gap " + _fmt(x.g) + ", pieces " + _fmt(x.pw) + " by " + _fmt(x.ph);
}

function gridTruth(sheetW, sheetH, pieceW, pieceH, gap, margin) {
  var x = _read(sheetW, sheetH, pieceW, pieceH, gap, margin), L = _layout(x.sw, x.sh, x.pw, x.ph, x.g, x.m);
  var s = _head(x) + ": upright gives " + L.a + " across by " + L.b + " down, " + _plural(L.up.toString(), "piece", "pieces") + "; turned gives " + L.c + " across by " + L.d + " down, " + _plural(L.turn.toString(), "piece", "pieces") + ". ";
  if (L.up === 0n && L.turn === 0n) return s + "No piece fits on the sheet.";
  if (L.up === L.turn) return s + "Both give " + _plural(L.up.toString(), "piece", "pieces") + ".";
  return s + "Best is " + (L.up > L.turn ? "upright" : "turned") + " with " + _plural((L.up > L.turn ? L.up : L.turn).toString(), "piece", "pieces") + ".";
}
function usedTruth(sheetW, sheetH, pieceW, pieceH, gap, margin) {
  var x = _read(sheetW, sheetH, pieceW, pieceH, gap, margin), L = _layout(x.sw, x.sh, x.pw, x.ph, x.g, x.m);
  var n = L.up > L.turn ? L.up : L.turn;
  var used = _tenths(n * x.pw * x.ph * 1000n, x.sw * x.sh);
  var usedT = (2n * n * x.pw * x.ph * 1000n + x.sw * x.sh) / (2n * x.sw * x.sh); // tenths of a percent
  var left = _tenths(1000n - usedT, 1n);
  return _head(x) + ": the best layout puts " + _plural(n.toString(), "piece", "pieces") + " on the sheet, covering " + used + "% of it and leaving " + left + "% for margins, gaps and offcuts.";
}
function sheetsTruth(pieces, perSheet, spare) {
  var n = _int(pieces, "the number of pieces must be a whole number from 1 to 100000", 1, 100000);
  var p = _int(perSheet, "the pieces per sheet must be a whole number from 1 to 10000", 1, 10000);
  var r = _int(spare, "the spare sheets must be a whole number from 0 to 1000", 0, 1000);
  var s = Math.floor((n + p - 1) / p), room = s * p - n, total = s + r;
  return _plural(n, "piece", "pieces") + " at " + p + " per sheet need " + _plural(s, "sheet", "sheets") + ", with room for " + _plural(room, "more piece", "more pieces") + " on the last sheet. With " + _plural(r, "spare sheet", "spare sheets") + " that is " + _plural(total, "sheet", "sheets") + " to buy.";
}

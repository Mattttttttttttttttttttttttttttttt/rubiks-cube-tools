// helpers.js — ported from helpers.py
// All functions exported as named exports for ES module usage

export function numPart(time) {
  return [...String(time)].filter(c => /[\d.:]/.test(c)).join('');
}

export function noBrackets(time) {
  return String(time).replace(/\[.*?\]/g, '');
}

export function noMultiphase(time) {
  let r = String(time).replace(/=.*?,/g, ',');
  return r.replace(/=.*?$/gm, '');
}

export function noParen(time) {
  return String(time).replace(/[()]/g, '');
}

export function validNum(num) {
  const s = String(num);
  return s.split('.')[0].length === 1 && !s.startsWith('-') ? '0' + s : s;
}

export function minutes(a) {
  if (typeof a === 'number' && !isNaN(a)) return a;
  const s = String(a);
  if (s.includes('DNF')) return Number.MAX_SAFE_INTEGER;
  const np = numPart(s);
  if (np.includes(':')) {
    const [minPart, secPart] = np.split(':');
    const dec = secPart.includes('.') ? secPart.split('.')[1].length : 0;
    return +((parseFloat(secPart) + 60 * parseInt(minPart)).toFixed(dec));
  }
  return parseFloat(np) || 0;
}

export function seconds(a) {
  if (a === 'DNF') return 'DNF';
  const str = String(a);
  const hasPlus = str.endsWith('+');
  const numStr = hasPlus ? str.slice(0, -1) : str;
  const val = parseFloat(numStr);
  if (isNaN(val)) return str;
  const dec = numStr.includes('.') ? numStr.split('.')[1].length : 0;
  const suffix = hasPlus ? '+' : '';
  if (val < 60) return str;
  const mins = Math.floor(val / 60);
  const secsFixed = (val % 60).toFixed(dec);
  const secsNum = parseFloat(secsFixed);
  const secsStr = secsNum < 10 ? '0' + secsFixed : secsFixed;
  return `${mins}:${secsStr}${suffix}`;
}

export function ndnf(a) {
  return typeof a === 'string' ? !a.includes('DNF') : true;
}
export function ydnf(a) {
  return typeof a === 'string' ? a.includes('DNF') : false;
}
export function prths(a)  { return String(a)[0] === '('; }
export function nprths(a) { return String(a)[0] !== '('; }

export function keep(thing, fn) { return thing.filter(fn); }

export function findAll(parent, daughter) {
  const s = Array.isArray(parent) ? parent.join('') : String(parent);
  let count = 0, idx = 0;
  while ((idx = s.indexOf(daughter, idx)) !== -1) { count++; idx += daughter.length; }
  return count;
}

export function deepjoin(lst, joiner) { return lst.map(String).join(joiner); }

export function frwrd(lst, start, value) { return lst.slice(start, start + value); }

export function repeat(lst) {
  const sorted = [...keep(lst, ndnf)].sort((a, b) => parseFloat(a) - parseFloat(b));
  const result = {};
  let i = 0;
  while (i < sorted.length) {
    let count = 1;
    while (i + count < sorted.length && sorted[i] === sorted[i + count]) count++;
    if (count > 1) result[sorted[i]] = count;
    i += count;
  }
  return result;
}

function _isDNF(s) { return String(s).includes('DNF'); }

function _minEl(arr) {
  let best = arr[0], bestV = minutes(arr[0]);
  for (const s of arr) { const v = minutes(s); if (v < bestV) { bestV = v; best = s; } }
  return best;
}
function _maxEl(arr) {
  let best = arr[0], bestV = minutes(arr[0]);
  for (const s of arr) { const v = minutes(s); if (v > bestV) { bestV = v; best = s; } }
  return best;
}

function trimArr(arr) {
  const minE = _minEl(arr), maxE = _maxEl(arr);
  arr.splice(arr.indexOf(minE), 1);
  arr.splice(arr.indexOf(maxE), 1);
}

export function avg(solves, numSolves, decimals = 0) {
  if (numSolves <= 2) throw new Error('avg requires >= 3 solves');
  const delete_ = Math.floor(numSolves / 20) + 1;

  if (numSolves === 3) {
    if (solves.some(_isDNF)) return Number.MAX_SAFE_INTEGER;
    const sum = solves.reduce((acc, s) => acc + parseFloat(s), 0);
    return decimals ? +(sum / numSolves).toFixed(decimals) : sum / numSolves;
  }

  const nonDnfs = solves.filter(s => !_isDNF(s));
  if (nonDnfs.length >= numSolves - delete_) {
    const copy = [...solves];
    for (let i = 0; i < delete_; i++) trimArr(copy);
    const sum = copy.reduce((acc, s) => acc + parseFloat(s), 0);
    const count = numSolves - 2 * delete_;
    return decimals ? +(sum / count).toFixed(decimals) : sum / count;
  }
  return 'DNF';
}

export function avgCompare(time) {
  return time === 'DNF' ? Number.MAX_SAFE_INTEGER : time;
}

export function roundDecimal(solves, avgVal) {
  if (avgVal === 'DNF') return 'DNF';
  let decimals = Math.max(...solves.map(s => {
    const np = numPart(s);
    return np.includes('.') ? np.split('.')[1].length : 0;
  }));
  if (decimals === 0) decimals = 2;

  let result = String(avgVal);
  const curDec = () => result.includes('.') ? result.split('.')[1].length : 0;

  if (curDec() > decimals) {
    const val = minutes(result);
    const rounded = +val.toFixed(decimals);
    result = seconds(String(rounded));
  }
  if (curDec() === 0) result += '.';
  return result + '0'.repeat(Math.max(0, decimals - curDec()));
}

// ── Average Generator specific ──────────────────────────────────────────────

export function minutesDnf(a) {
  const s = String(a);
  if (s.includes('DNF')) return s;
  const np = numPart(s);
  if (np.includes(':')) {
    const [m, sec] = np.split(':');
    const dec = sec.includes('.') ? sec.split('.')[1].length : 0;
    return +(parseFloat(sec) + 60 * parseInt(m)).toFixed(dec);
  }
  return parseFloat(np);
}

export function plusTwoSolve(raw, penalty) {
  // returns new penalty state - toggles +2
  if (penalty === 'dnf') return 'dnf'; // can't +2 a DNF (handled in UI)
  return penalty === 'p2' ? null : 'p2';
}

export function dnfSolve(raw, penalty) {
  return penalty === 'dnf' ? null : 'dnf';
}

export function solveString(raw, penalty) {
  // Given a raw time string and penalty, return the formatted solve string
  if (!raw) return '';
  if (penalty === 'dnf') return `DNF(${raw})`;
  if (penalty === 'p2') {
    const val = minutes(raw);
    return seconds(String(val + 2)) + '+';
  }
  return raw;
}

function addParenthese(copy, solves) {
  const fastEl = _minEl(copy);
  copy.splice(copy.indexOf(fastEl), 1);
  const fi = solves.findIndex(s => noParen(s) === fastEl || s === fastEl);
  if (fi !== -1) solves[fi] = '(' + solves[fi] + ')';

  const slowEl = _maxEl(copy);
  copy.splice(copy.indexOf(slowEl), 1);
  const si = solves.findIndex(s => noParen(s) === slowEl || s === slowEl);
  if (si !== -1) solves[si] = '(' + solves[si] + ')';
}

export function avgStr(num, solvesIn) {
  // solvesIn: array of formatted strings like "9.45", "DNF(9.45)", "11.45+"
  const solves = [...solvesIn];
  const dnfs = findAll(solves.join(''), 'DNF');

  if (num === 3) {
    // mean of 3
    if (dnfs > 0) {
      if (dnfs !== 3) {
        const fi = solves.reduce((best, s, i) =>
          minutes(minutesDnf(s)) < minutes(minutesDnf(solves[best])) ? i : best, 0);
        solves[fi] = `**${solves[fi]}**`;
      }
      return { avg: 'DNF', solves };
    }
    const rawVals = solves.map(s => String(minutesDnf(s)));
    const avgVal = roundDecimal(solves, seconds(String(avg(rawVals, 3))));
    const fi = solves.reduce((best, s, i) =>
      minutes(s) < minutes(solves[best]) ? i : best, 0);
    solves[fi] = `**${solves[fi]}**`;
    return { avg: avgVal, solves };
  }

  // average of n (trim best/worst)
  const delete_ = Math.floor(num / 20) + 1;
  const copy = [...solves];
  const rawVals = solves.map(s => String(minutesDnf(s)));
  const avgVal = roundDecimal(solvesIn, seconds(String(avg(rawVals, num))));
  for (let i = 0; i < delete_; i++) addParenthese(copy, solves);
  return { avg: avgVal, solves };
}

// ── Stats Calculator ─────────────────────────────────────────────────────────

export function stdev(arr) {
  if (arr.length < 2) return 0;
  const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
  return Math.sqrt(arr.reduce((acc, v) => acc + (v - mean) ** 2, 0) / (arr.length - 1));
}

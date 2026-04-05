// sq1lib.js — Square-1 library, ported from get_scramble.py
// Used by sq1/ and oblp/ tools

// ── Constants ────────────────────────────────────────────────────────────────

export const INV_NORM = {
  ' U U\' U U\' ': ' U4 ', ' U\' U U\' U ': ' U4\' ',
  ' D D\' D D\' ': ' D4 ', ' D\' D D\' D ': ' D4\' ',
  ' u u\' u u\' ': ' u4 ', ' u\' u u\' u ': ' u4\' ',
  ' d d\' d d\' ': ' d4 ', ' d\' d d\' d ': ' d4\' ',
  ' U U\' U ': ' U3 ', ' U\' U U\' ': ' U3\' ',
  ' D D\' D ': ' D3 ', ' D\' D D\' ': ' D3\' ',
  ' u u\' u ': ' u3 ', ' u\' u u\' ': ' u3\' ',
  ' d d\' d ': ' d3 ', ' d\' d d\' ': ' d3\' ',
  ' F F\' F ': ' F3 ', ' F\' F F\' ': ' F3\' ',
  ' f f\' f ': ' f3 ', ' f\' f f\' ': ' f3\' ',
  ' U U\' ': ' W ', ' U\' U ': ' W\' ',
  ' D D\' ': ' B ', ' D\' D ': ' B\' ',
  ' u u\' ': ' w ', ' u\' u ': ' w\' ',
  ' d d\' ': ' b ', ' d\' d ': ' b\' ',
  ' F F\' ': ' F2 ', ' F\' F ': ' F2\' ',
  ' f f\' ': ' f2 ', ' f\' f ': ' f2\' ',
  ' U U ': ' UU ', ' U\' U\' ': ' UU\' ',
  ' D D ': ' DD ', ' D\' D\' ': ' DD\' ',
  ' 6,0 ': ' U2 ', ' 6,3 ': ' U2D ', ' 6,-3 ': ' U2D\' ',
  ' 6,6 ': ' U2D2 ', ' 0,6 ': ' D2 ', ' 3,6 ': ' UD2 ', ' -3,6 ': ' U\'D2 ',
  ' 3,0 ': ' U ', ' -3,0 ': ' U\' ', ' 0,3 ': ' D ', ' 0,-3 ': ' D\' ',
  ' 3,-3 ': ' E ', ' -3,3 ': ' E\' ', ' 3,3 ': ' e ', ' -3,-3 ': ' e\' ',
  ' 2,-1 ': ' u ', ' -1,2 ': ' d ', ' -4,-1 ': ' F\' ', ' -1,-4 ': ' f\' ',
  ' 2,-4 ': ' T ', ' -4,2 ': ' t\' ', ' 2,2 ': ' m ', ' -1,-1 ': ' M\' ',
  ' 5,-1 ': ' u2 ', ' -1,5 ': ' d2 ', ' -2,1 ': ' u\' ', ' 1,-2 ': ' d\' ',
  ' 4,1 ': ' F ', ' 1,4 ': ' f ', ' -2,4 ': ' T\' ', ' 4,-2 ': ' t ',
  ' -2,-2 ': ' m\' ', ' 1,1 ': ' M ', ' -5,1 ': ' u2\' ', ' 1,-5 ': ' d2\' ',
  ' -5,-2 ': ' K\' ', ' 5,2 ': ' K ', ' 2,5 ': ' k ', ' -2,-5 ': ' k\' '
};

export const NORM = Object.fromEntries(Object.entries(INV_NORM).map(([k,v]) => [v,k]));

export const OPTIM = {
  '/3,3/3,3/': '-3,-3/-3,-3',
  '/-3,-3/-3,-3/': '3,3/3,3',
  '/2,2/-2,-2/': '2,2/-2,-2',
  '/-2,-2/2,2/': '-2,-2/2,2',
  '/1,1/-1,-1/': '1,1/-1,-1',
  '/-1,-1/1,1/': '-1,-1/1,1',
  '/2,-4/-2,4/2,-4/': '2,-4/-2,4/2,-4',
  '/-2,4/2,-4/-2,4/': '-2,4/2,-4/-2,4',
  '/5,-1/-5,1/5,-1/': '5,-1/-5,1/5,-1',
  '/-5,1/5,-1/-5,1/': '-5,1/5,-1/-5,1'
};

export const GOOD = [
  '11','-1-1','22','-2-2','2-1','-21','1-2','-12',
  '30','-30','03','0-3','33','3-3','-3-3','-33',
  '41','-4-1','14','-1-4','2-4','-24','4-2','-42',
  '5-1','-51'
];

// ── Core utilities ────────────────────────────────────────────────────────────

export function dictReplace(s, d) {
  const keys = Object.keys(d).sort((a, b) => b.length - a.length);
  const pattern = new RegExp(keys.map(k => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|'), 'g');
  let prev = '';
  while (s !== prev) { prev = s; s = s.replace(pattern, m => d[m]); }
  return s;
}

export function legalMove(m) {
  m = parseInt(m);
  if (m < -5) return m + 12;
  if (m > 6) return m - 12;
  return m;
}

export function addMovesStr(move1, move2) {
  const [u1, d1] = move1.split(',').map(Number);
  const [u2, d2] = move2.split(',').map(Number);
  return `${legalMove(u1 + u2)},${legalMove(d1 + d2)}`;
}

export function changesAlignment(m) {
  return parseInt(m) % 3 !== 0;
}

export function addCommas(scramble) {
  const sep = scramble.includes(' / ') ? ' / ' : scramble.includes('/') ? '/' : ' ';
  const parts = scramble.split(sep);
  return parts.map(m => {
    if (m.includes(',') || m.toLowerCase() === 'a') return m;
    switch (m.length) {
      case 2: return m[0] + ',' + m[1];
      case 3: return m[0] === '-' ? m.slice(0,2) + ',' + m[2] : m[0] + ',' + m.slice(1);
      case 4: return m.slice(0,2) + ',' + m.slice(2);
      default: return m;
    }
  }).join(sep);
}

export function karnify(scramble) {
  const sep = scramble.includes(' / ') ? ' / ' : scramble.includes('/') ? '/' : ' ';
  scramble = (' ' + scramble.replace(new RegExp(sep.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), ' / ') + ' ');
  scramble = dictReplace(scramble, INV_NORM).replace(/,/g, '').trim();
  return scramble.replace(/ +/g, ' ');
}

export function optimize(scramble) {
  const OPTIM_KEYS = Object.keys(OPTIM);
  let changed = true;
  while (changed) {
    changed = false;
    for (const key of OPTIM_KEYS) {
      if (scramble.includes(key)) {
        // find position
        const idx = scramble.indexOf(key);
        // count slashes before idx to know at_slice
        const atSlice = scramble.slice(0, idx + 1).split('/').length - 1;
        const moves = scramble.split('/');
        const optimTo = OPTIM[key].split('/');
        const optimableL = key.split('/').length;
        const delSliceNum = optimableL - optimTo.length;

        if (atSlice === 1) {
          if (optimTo.length > 0) {
            const first = optimTo.shift();
            if (changesAlignment(first.split(',')[0])) {
              moves[0] = moves[0] === 'a' ? 'A' : 'a';
            }
          }
          if (optimTo.length > 0) {
            const last = optimTo.pop();
            moves[atSlice + optimableL - 2] = addMovesStr(moves[atSlice + optimableL - 2], last);
          }
        } else if (atSlice + optimableL - 1 === moves.length) {
          if (optimTo.length > 0) {
            const last = optimTo.pop();
            if (changesAlignment(last.split(',')[0])) {
              const lastEl = moves.pop();
              moves.push(lastEl === 'a' ? 'A' : 'a');
            }
          }
          if (optimTo.length > 0) {
            const first = optimTo.shift();
            moves[atSlice - 1] = addMovesStr(moves[atSlice - 1], first);
          }
        } else {
          if (optimTo.length > 0) {
            const first = optimTo.shift();
            moves[atSlice - 1] = addMovesStr(moves[atSlice - 1], first);
          }
          if (optimTo.length > 0) {
            const last = optimTo.pop();
            moves[atSlice + optimableL - 2] = addMovesStr(moves[atSlice + optimableL - 2], last);
          }
        }
        moves.splice(atSlice, delSliceNum, ...optimTo);
        scramble = moves.join('/');
        changed = true;
        break;
      }
    }
  }
  return scramble;
}

// ── sq1normalizer functions ───────────────────────────────────────────────────

function obKarn(a) {
  return /[a-zA-Z]/.test(a);
}

function sepIndex(a) {
  let inx = 0;
  for (const char of a) { inx++; if (/\d/.test(char)) break; }
  return inx;
}

function compl(a) {
  const inx = sepIndex(a);
  const parts = [a.slice(0, inx), a.slice(inx)];
  return String(legalMove(6 + parseInt(parts[0]))) + String(legalMove(6 + parseInt(parts[1])));
}

function lf(a) {
  const inx = sepIndex(a);
  return a.slice(inx) + a.slice(0, inx);
}

function comma(a) {
  const inx = sepIndex(a);
  return a.slice(0, inx) + ',' + a.slice(inx);
}

export function normalize(algIn, lfLst, k = null, leave = true) {
  let alg = algIn.replace(/\[.*?\]/g, '').trim();
  if (!lfLst || lfLst.length === 0) lfLst = [-1];

  const ki = obKarn(alg);
  const kOut = k === null ? ki : k;

  if (ki) {
    alg = dictReplace(alg, NORM);
    // result has commas, may have spaces for slices; remove commas
    alg = alg.replace(/,/g, '').trim();
  } else {
    alg = alg.replace(/[()]/g, '');
    if (alg.includes('/')) {
      alg = alg.replace(/ /g, '');
      alg = alg.split('/').map(m => {
        const [u, d] = m.split(',');
        return String(legalMove(parseInt(u))) + String(legalMove(parseInt(d)));
      }).join(' ');
    } else {
      alg = alg.replace(/ +/g, ' ').trim();
      alg = alg.split(' ').map(m => {
        const p = m.includes(',') ? m.split(',') : [m.slice(0, sepIndex(m)), m.slice(sepIndex(m))];
        return String(legalMove(parseInt(p[0]))) + String(legalMove(parseInt(p[1])));
      }).join(' ');
    }
  }

  // alg now in "10 5-1 -51 -10" space-separated no-comma format
  let alst = alg.split(' ');

  if (alst[0].toLowerCase() !== 'a') {
    const lastDigit0 = parseInt(alst[0].slice(-1));
    const lastDigitN = parseInt(alst[alst.length - 1].slice(-1));
    alst[0] = lastDigit0 % 3 === 0 ? 'A' : 'a';
    alst[alst.length - 1] = lastDigitN % 3 === 0 ? 'A' : 'a';
  }

  // Apply layer flips
  let lfing = false;
  let facingD = false;
  for (let i = 1; i <= alst.length - 3; i++) {
    let m = alst[i];
    m = facingD ? lf(m) : m;
    if ((!leave && !GOOD.includes(m)) || lfLst.includes(i)) {
      m = compl(m);
      lfing = !lfing;
    }
    facingD = lfing ? !facingD : facingD;
    alst[i] = m;
  }

  // Change last actual move
  const lastMoveIdx = alst.length - 2;
  alst[lastMoveIdx] = facingD ? lf(alst[lastMoveIdx]) : alst[lastMoveIdx];
  alst[lastMoveIdx] = (lfing !== facingD) ? compl(alst[lastMoveIdx]) : alst[lastMoveIdx];
  const lastMove = alst[lastMoveIdx];

  // Add commas for optimize
  for (let i = 1; i < alst.length - 1; i++) alst[i] = comma(alst[i]);
  alg = optimize('/' + alst.join('/'));

  // Format output
  let comment = GOOD.includes(lastMove) || ['-45','-54','63'].includes(lastMove) ? '' : ' (bad finish)';
  const algParts = alg.split('/').filter(p => p);
  const startA = algParts[0] || '';
  const endA = algParts[algParts.length - 1] || '';
  if (startA !== endA) comment += ' (alignment changes)';

  if (kOut) {
    alg = alg.replace(/ /g, '/');
    alg = addCommas(alg);
    alg = karnify(alg);
  }

  return alg + comment;
}

// ── OBLP Trainer functions ────────────────────────────────────────────────────

export function layerFlip(state) {
  return [...state].map(c => {
    if (c === 'b') return 'w';
    if (c === 'B') return 'W';
    if (c === 'w') return 'b';
    if (c === 'W') return 'B';
    return c;
  }).join('');
}

export function shift(a, amount) {
  amount = -amount;
  if (amount < 0) amount += a.length;
  return a.slice(amount) + a.slice(0, amount);
}

// OBL dict from oblp_visualize_trainer.py (pattern → case name)
export const OBL_PATTERNS = {
  'BBwWWwWWwWWw': '1c',
  'BBwBBwWWwWWw': 'cadj',
  'BBwWWwBBwWWw': 'copp',
  'BBwBBwBBwWWw': '3c',
  'BBwBBwBBwBBw': '4e',
  'WWbWWbWWbWWw': '3e',
  'WWbWWwWWbWWw': 'line',
  'WWbWWbWWwWWw': 'L',
  'WWbWWwWWwWWw': '1e',
  'WWbBBwWWwWWw': 'left pair',
  'BBbWWwWWwWWw': 'right pair',
  'BBwWWwWWbWWw': 'left arrow',
  'BBwWWbWWwWWw': 'right arrow',
  'WWbBBbWWwWWw': 'gem',
  'WWwWWbWWbBBw': 'left knight',
  'BBbWWbWWwWWw': 'right knight',
  'WWwWWbWWwBBb': 'left axe',
  'BBwWWbWWwWWb': 'right axe',
  'BBwWWbWWbWWw': 'squid',
  'WWwWWbBBbWWb': 'left thumb',
  'WWbBBbWWwWWb': 'right thumb',
  'WWwBBbWWbWWb': 'left bunny',
  'WWbWWbBBwWWb': 'right bunny',
  'BBbBBwWWwWWw': 'shell',
  'BBwWWwWWbBBw': 'left bird',
  'BBwBBbWWwWWw': 'right bird',
  'BBwWWbWWwBBw': 'hazard',
  'BBbBBbWWwWWw': 'left kite',
  'WWwWWbBBbBBw': 'right kite',
  'BBwBBwWWbWWb': 'left cut',
  'BBwBBbWWbWWw': 'right cut',
  'BBbBBwWWbWWw': 'black T',
  'WWwWWbBBwBBb': 'white T',
  'WWbBBwWWbBBw': 'left N',
  'WWwBBbWWwBBb': 'right N',
  'WWbBBbWWwBBw': 'black tie',
  'BBwWWwBBbWWb': 'white tie',
  'BBbWWwBBwWWw': 'left yoshi',
  'WWwBBwWWbBBw': 'right yoshi'
};

export const POSSIBLE_OBL = [
  ['','solved','solved'],
  ['','1c','1c'],['','cadj','cadj'],['','cadj','copp'],['','copp','copp'],
  ['','3c','3c'],['','4e','4e'],['','3e','3e'],['','line','line'],
  ['','L','line'],['','L','L'],['','1e','1e'],
  ['good','pair','pair'],['bad','pair','pair'],
  ['good','arrow','pair'],['bad','arrow','pair'],
  ['good','arrow','arrow'],['bad','arrow','arrow'],
  ['','gem','gem'],['','gem','knight'],['','gem','axe'],['','gem','squid'],
  ['good','knight','knight'],['bad','knight','knight'],
  ['good','knight','axe'],['bad','knight','axe'],
  ['same','axe','axe'],['diff','axe','axe'],
  ['','squid','knight'],['','squid','axe'],['','squid','squid'],
  ['good','thumb','thumb'],['bad','thumb','thumb'],
  ['good','thumb','bunny'],['bad','thumb','bunny'],
  ['good','bunny','bunny'],['bad','bunny','bunny'],
  ['','shell','shell'],['','shell','bird'],['','shell','hazard'],
  ['','yoshi','shell'],
  ['good','bird','bird'],['bad','bird','bird'],
  ['','bird','hazard'],['','hazard','hazard'],
  ['good','yoshi','bird'],['bad','yoshi','bird'],
  ['','yoshi','hazard'],['same','yoshi','yoshi'],['diff','yoshi','yoshi'],
  ['good','kite','kite'],['bad','kite','kite'],
  ['good','kite','cut'],['bad','kite','cut'],
  ['','kite','T'],['good','kite','N'],['bad','kite','N'],['','kite','tie'],
  ['','cut','T'],['good','cut','N'],['bad','cut','N'],['','cut','tie'],
  ['good','cut','cut'],['bad','cut','cut'],
  ['good','T','T'],['bad','T','T'],['','T','N'],
  ['good','T','tie'],['bad','T','tie'],
  ['good','N','N'],['bad','N','N'],['','tie','N'],
  ['good','tie','tie'],['bad','tie','tie']
];

export const OBL_TRANSLATION = {
  'solved/solved': ['solved/solved'],
  '1c/1c': ['1c/1c'],
  'cadj/cadj': ['cadj/cadj'],
  'cadj/copp': ['cadj/copp'],
  'copp/copp': ['copp/copp'],
  '3c/3c': ['3c/3c'],
  '4e/4e': ['4e/4e'],
  '3e/3e': ['3e/3e'],
  'line/line': ['line/line'],
  'L/line': ['L/line'],
  'L/L': ['L/L'],
  '1e/1e': ['1e/1e'],
  'good pair/pair': ['left pair/left pair','right pair/right pair'],
  'bad pair/pair': ['left pair/right pair'],
  'good arrow/pair': ['left arrow/right pair','right arrow/left pair'],
  'bad arrow/pair': ['left arrow/left pair','right arrow/right pair'],
  'good arrow/arrow': ['left arrow/left arrow','right arrow/right arrow'],
  'bad arrow/arrow': ['left arrow/right arrow'],
  'gem/gem': ['gem/gem'],
  'gem/knight': ['gem/left knight','gem/right knight'],
  'gem/axe': ['gem/left axe','gem/right axe'],
  'gem/squid': ['gem/squid'],
  'good knight/knight': ['left knight/right knight'],
  'bad knight/knight': ['left knight/left knight','right knight/right knight'],
  'good knight/axe': ['left knight/left axe','right knight/right axe'],
  'bad knight/axe': ['left knight/right axe','right knight/left axe'],
  'same axe/axe': ['left axe/left axe','right axe/right axe'],
  'diff axe/axe': ['left axe/right axe'],
  'squid/knight': ['squid/left knight','squid/right knight'],
  'squid/axe': ['squid/left axe','squid/right axe'],
  'squid/squid': ['squid/squid'],
  'good thumb/thumb': ['left thumb/left thumb','right thumb/right thumb'],
  'bad thumb/thumb': ['left thumb/right thumb'],
  'good thumb/bunny': ['left thumb/right bunny','right thumb/left bunny'],
  'bad thumb/bunny': ['left thumb/left bunny','right thumb/right bunny'],
  'good bunny/bunny': ['left bunny/left bunny','right bunny/right bunny'],
  'bad bunny/bunny': ['left bunny/right bunny'],
  'shell/shell': ['shell/shell'],
  'shell/bird': ['shell/left bird','shell/right bird'],
  'shell/hazard': ['shell/hazard'],
  'yoshi/shell': ['left yoshi/shell','right yoshi/shell'],
  'good bird/bird': ['left bird/right bird'],
  'bad bird/bird': ['left bird/left bird','right bird/right bird'],
  'bird/hazard': ['left bird/hazard','right bird/hazard'],
  'hazard/hazard': ['hazard/hazard'],
  'good yoshi/bird': ['left yoshi/left bird','right yoshi/right bird'],
  'bad yoshi/bird': ['left yoshi/right bird','right yoshi/left bird'],
  'yoshi/hazard': ['left yoshi/hazard','right yoshi/hazard'],
  'same yoshi/yoshi': ['left yoshi/left yoshi','right yoshi/right yoshi'],
  'diff yoshi/yoshi': ['left yoshi/right yoshi'],
  'good kite/kite': ['left kite/left kite','right kite/right kite'],
  'bad kite/kite': ['left kite/right kite'],
  'good kite/cut': ['left kite/left cut','right kite/right cut'],
  'bad kite/cut': ['left kite/right cut','right kite/left cut'],
  'kite/T': ['left kite/black T','left kite/white T','right kite/black T','right kite/white T'],
  'good kite/N': ['left kite/right N','right kite/left N'],
  'bad kite/N': ['left kite/left N','right kite/right N'],
  'kite/tie': ['left kite/black tie','left kite/white tie','right kite/black tie','right kite/white tie'],
  'cut/T': ['left cut/black T','left cut/white T','right cut/black T','right cut/white T'],
  'good cut/N': ['left cut/left N','right cut/right N'],
  'bad cut/N': ['left cut/right N','right cut/left N'],
  'cut/tie': ['left cut/black tie','left cut/white tie','right cut/black tie','right cut/white tie'],
  'good cut/cut': ['left cut/left cut','right cut/right cut'],
  'bad cut/cut': ['left cut/right cut'],
  'good T/T': ['black T/black T','white T/white T'],
  'bad T/T': ['black T/white T'],
  'T/N': ['black T/left N','black T/right N','white T/left N','white T/right N'],
  'good T/tie': ['black T/black tie','white T/white tie'],
  'bad T/tie': ['black T/white tie','white T/black tie'],
  'good N/N': ['left N/left N','right N/right N'],
  'bad N/N': ['left N/right N'],
  'tie/N': ['black tie/left N','black tie/right N','white tie/left N','white tie/right N'],
  'good tie/tie': ['black tie/black tie','white tie/white tie'],
  'bad tie/tie': ['black tie/white tie']
};

function oblName(obl) {
  return obl[0] ? `${obl[0]} ${obl[1]}/${obl[2]}` : `${obl[1]}/${obl[2]}`;
}

function layerFlipName(obl) {
  obl = obl.replace('/', ' ');
  const parts = obl.split(' ');
  if (parts.length === 2) return parts[1] + '/' + parts[0];
  return parts[0] + ' ' + parts[2] + '/' + parts[1];
}

export function getNonSpe(obl) {
  const [uObl, dObl] = obl.split('/');
  const u = uObl.split(' ').pop();
  const d = dObl.split(' ').pop();
  const candidates = POSSIBLE_OBL
    .filter(c => c.includes(u) && c.includes(d))
    .map(oblName);
  for (const cand of candidates) {
    const specials = OBL_TRANSLATION[cand] || [];
    for (const spe of specials) {
      if (spe === obl) return cand;
      const [s1, s2] = spe.split('/');
      if (`${s2}/${s1}` === obl) return layerFlipName(cand);
    }
  }
  throw new Error(`No non-specific OBL found for: ${obl}`);
}

// OBL case lookup from BbWw pattern
function isOblCase(l, target) {
  const targetPattern = Object.entries(OBL_PATTERNS).find(([,v]) => v === target)?.[0];
  if (!targetPattern) return false;
  for (let m = 0; m < 4; m++) {
    if (targetPattern === shift(l, 3 * m)) return true;
  }
  const noTT = !['T', 'tie'].includes(target.split(' ').pop());
  if (noTT) {
    const fl = layerFlip(l);
    for (let m = 0; m < 4; m++) {
      if (targetPattern === shift(fl, 3 * m)) return true;
    }
  }
  return false;
}

export function toLayerName(m) {
  const bw = ['W','W','w','W','W','w','W','W','w','W','W','w'];
  for (const ch of m) {
    const num = parseInt(ch);
    if (num % 2 !== 0) {
      // corner
      bw[Math.floor(num/2)*3] = 'B';
      bw[Math.floor(num/2)*3+1] = 'B';
    } else {
      // edge
      bw[Math.floor(num/2)*3-1] = 'b';
    }
  }
  const obl = bw.join('');
  for (const [pattern, name] of Object.entries(OBL_PATTERNS)) {
    if (isOblCase(obl, name)) return name;
  }
  throw new Error('OBL not found: ' + obl);
}

export function toCaseName(m) {
  const [u, d] = m.split(' ');
  const uName = toLayerName(u);
  const dName = toLayerName(d);
  return getNonSpe(`${uName}/${dName}`);
}

export function sortOblp(seq) {
  return [...seq].sort((a, b) => parseInt(a) - parseInt(b)).join('');
}

// Trainer data
export const CORNERS = [[''], ['1','3','5','7'], ['13','15','17','35','37','57'], ['135','137','157','357'], ['1357']];
export const EDGES   = [[''], ['2','4','6','8'], ['24','26','28','46','48','68'], ['246','248','268','468'], ['2468']];
export const TOTAL_CORNERS = ['','1','3','5','7','13','15','17','35','37','57','135','137','157','357','1357'];
export const TOTAL_EDGES   = ['','2','4','6','8','24','26','28','46','48','68','246','248','268','468','2468'];

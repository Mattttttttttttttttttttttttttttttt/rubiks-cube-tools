// sq1lib.js — Square-1 unified library
// Karn / unkarnify / ergonomics logic kept in sync with karn.js (source of truth).
// OBLP trainer data and normalize() live here only.

// =============================================================================
// SECTION 1 — DATA TABLES  (from karn.js)
// =============================================================================

// karnToWCA — Karnotation token → WCA numeric slash segments.
// Space-padded so global replace cannot match partial tokens.
export const karnToWCA = {
  " U4 ": " / U U' U U' / ", " U4' ": " / U' U U' U / ",
  " D4 ": " / D D' D D' / ", " D4' ": " / D' D D' D / ",
  " u4 ": " / u u' u u' / ", " u4' ": " / u' u u' u / ",
  " d4 ": " / d d' d d' / ", " d4' ": " / d' d d' d / ",

  " U3 ": " / U U' U / ", " U3' ": " / U' U U' / ",
  " D3 ": " / D D' D / ", " D3' ": " / D' D D' / ",
  " u3 ": " / u u' u / ", " u3' ": " / u' u u' / ",
  " d3 ": " / d d' d / ", " d3' ": " / d' d d' / ",
  " F3 ": " / F F' F / ", " F3' ": " / F' F F' / ",
  " f3 ": " / f f' f / ", " f3' ": " / f' f f' / ",

  " W ": " / U U' / ", " W' ": " / U' U / ",
  " B ": " / D D' / ", " B' ": " / D' D / ",
  " w ": " / u u' / ", " w' ": " / u' u / ",
  " b ": " / d d' / ", " b' ": " / d' d / ",
  " F2 ": " / F F' / ", " F2' ": " / F' F / ",
  " f2 ": " / f f' / ", " f2' ": " / f' f / ",
  " UU ": " / U U / ", " UU' ": " / U' U' / ",
  " DD ": " / D D / ", " DD' ": " / D' D' / ",
  " T2 ": " / T T' / ", " T2' ": " / T' T / ",
  " t2 ": " / t t' / ", " t2' ": " / t' t / ",
  " E2 ": " / E E' / ", " E2' ": " / E' E / ",
  " ɇ ": " / U D / ", " ɇ' ": " / U' D' / ",
  " Ɇ ": " / U D' / ", " Ɇ' ": " / U' D / ",

  " U2 ": " /6,0/ ", " U2' ": " /6,0/ ",
  " D2 ": " /0,6/ ",
  " U2D ": " /6,3/ ", " U2D' ": " /6,-3/ ",
  " U2'D ": " /6,3/ ", " U2'D' ": " /6,-3/ ",
  " U2D2 ": " /6,6/ ",
  " UD2 ": " /3,6/ ", " U'D2 ": " /-3,6/ ",

  " U ": " /3,0/ ", " U' ": " /-3,0/ ",
  " D ": " /0,3/ ", " D' ": " /0,-3/ ",
  " E ": " /3,-3/ ", " E' ": " /-3,3/ ",
  " e ": " /3,3/ ", " e' ": " /-3,-3/ ",
  " u ": " /2,-1/ ", " u' ": " /-2,1/ ",
  " d ": " /-1,2/ ", " d' ": " /1,-2/ ",
  " F ": " /4,1/ ", " F' ": " /-4,-1/ ",
  " f ": " /1,4/ ", " f' ": " /-1,-4/ ",
  " T ": " /2,-4/ ", " T' ": " /-2,4/ ",
  " t ": " /4,-2/ ", " t' ": " /-4,2/ ",
  " m ": " /2,2/ ", " m' ": " /-2,-2/ ",
  " M ": " /1,1/ ", " M' ": " /-1,-1/ ",
  " u2 ": " /5,-1/ ", " u2' ": " /-5,1/ ",
  " d2 ": " /-1,5/ ", " d2' ": " /1,-5/ ",
  " K ": " /5,2/ ", " K' ": " /-5,-2/ ",
  " k ": " /2,5/ ", " k' ": " /-2,-5/ ",
  " A ": " /1,0/ ", " A' ": " /-1,0/ ",
  " G ": " /5,-4/ ", " G' ": " /-5,4/ ",
  " g ": " /4,-5/ ", " g' ": " /-4,5/ ",
};

// wcaToKarn — inverse direction: WCA token streams → Karnotation names.
export const wcaToKarn = {
  " U U' U U' ": " U4 ", " U' U U' U ": " U4' ",
  " D D' D D' ": " D4 ", " D' D D' D ": " D4' ",
  " u u' u u' ": " u4 ", " u' u u' u ": " u4' ",
  " d d' d d' ": " d4 ", " d' d d' d ": " d4' ",

  " U U' U ": " U3 ", " U' U U' ": " U3' ",
  " D D' D ": " D3 ", " D' D D' ": " D3' ",
  " u u' u ": " u3 ", " u' u u' ": " u3' ",
  " d d' d ": " d3 ", " d' d d' ": " d3' ",
  " F F' F ": " F3 ", " F' F F' ": " F3' ",
  " f f' f ": " f3 ", " f' f f' ": " f3' ",

  " U U' ": " W ", " U' U ": " W' ",
  " D D' ": " B ", " D' D ": " B' ",
  " u u' ": " w ", " u' u ": " w' ",
  " d d' ": " b ", " d' d ": " b' ",
  " F F' ": " F2 ", " F' F ": " F2' ",
  " f f' ": " f2 ", " f' f ": " f2' ",
  " U U ": " UU ", " U' U' ": " UU' ",
  " D D ": " DD ", " D' D' ": " DD' ",

  " 6,0 ": " U2 ",
  " 6,3 ": " U2D ", " 6,-3 ": " U2D' ", " 6,6 ": " U2D2 ",
  " 0,6 ": " D2 ",
  " 3,6 ": " UD2 ", " -3,6 ": " U'D2 ",

  " 3,0 ": " U ", " -3,0 ": " U' ",
  " 0,3 ": " D ", " 0,-3 ": " D' ",
  " 3,-3 ": " E ", " -3,3 ": " E' ",
  " 3,3 ": " e ", " -3,-3 ": " e' ",
  " 2,-1 ": " u ", " -2,1 ": " u' ",
  " -1,2 ": " d ", " 1,-2 ": " d' ",
  " 4,1 ": " F ", " -4,-1 ": " F' ",
  " 1,4 ": " f ", " -1,-4 ": " f' ",
  " 2,-4 ": " T ", " -2,4 ": " T' ",
  " 4,-2 ": " t ", " -4,2 ": " t' ",
  " 2,2 ": " m ", " -2,-2 ": " m' ",
  " 1,1 ": " M ", " -1,-1 ": " M' ",
  " 5,-1 ": " u2 ", " -5,1 ": " u2' ",
  " -1,5 ": " d2 ", " 1,-5 ": " d2' ",
  " 5,2 ": " K ", " -5,-2 ": " K' ",
  " 2,5 ": " k ", " -2,-5 ": " k' ",
};

// Backward-compat aliases for tools that still import INV_NORM / NORM.
export const INV_NORM = wcaToKarn;
export const NORM = karnToWCA;

export const shorthandToKarn = {
  "bjj": "/U' e D'/", "fjj": "/U e' D/",
  "e2bjj": "/U' e' U'/", "e2fjj": "/U e U/",
  "nn": "/E E'/",
  "jn": "/D4'/", "nj": "/U4/",
  "jj": "/U e' D/", "bjj+e2": "/U' e' U'/",
  "-nn": "/E' E/",
  "-jn": "/D4/", "-nj": "/D4'/",
  "bpj10": "/d m' U/", "bpj0-1": "/u' m D'/",
  "fpj10": "/u m' D/", "fpj0-1": "/d' m U'/",
  "aa10": "/u m' u T'/", "aa0-1": "/U m' U t'/",
  "fadj10": "/D M' d'/", "dadj10": "/D M' d'/",
  "fadj0-1": "/U' M u/", "u'adj0-1": "/U' M u/",
  "badj10": "/U M' u'/", "uadj10": "/U M' u'/",
  "badj0-1": "/D' M d/", "d'adj0-1": "/D' M d/",
  "bb10": "/T u' e U'/", "bb0-1": "/t d e' D/",
  "fdd10": "/D e' d t/", "fdd0-1": "/U' e u' T/",
  "bdd10": "/U e' u T'/", "bdd0-1": "/D' e d' t'/",
  "ff10": "/d m' d M E/", "ff0-1": "/u' m U' M T/",
  "fv10": "/d4/", "fv0-1": "/d4'/",
  "vf10": "/u4/", "vf0-1": "/u4'/",
  "y2fv10": "/u d' u -5,4/",
  "jf10": "/w D' u T'/", "jf0-1": "/w' D u' T/",
  "fj10": "/b U' d t/", "fj0-1": "/b' U d' t'/",
  "jr00": "/e' w e/", "jr10": "/e' b e/",
  "jr0-1": "/e' w' e/", "jr1-1": "/e' b' e/",
  "rj00": "/e b' e'/", "rj10": "/e w e'/",
  "rj0-1": "/e b' e'/", "rj1-1": "/e w e'/",
  "jv10": "/b D d d2'/", "jv0-1": "/b' D' d' d2/",
  "vj10": "/w U u u2'/", "vj0-1": "/w' U' u' u2/",
  "kk10": "/u m' U E'/", "kk0-1": "/U m' u E'/",
  "opp10": "/u2 u2'/", "opp0-1": "/u2' u2/",
  "pn10": "/T T'/", "pn0-1": "/t t'/",
  "px10": "/f' d3' f'/", "px0-1": "/f d3 f/",
  "xp10": "/F' u3' F'/", "xp0-1": "/F u3 F/",
  "tt10": "/d m' F' u2'/",
  "fss10": "/u M D' E'/", "fss0-1": "/D' M u E'/",
  "bss10": "/D M' u' E/", "bss0-1": "/U' M d E/",
  "vv10": "/u M u m' E'/",
  "zz10": "/u M t' M D'/", "zz0-1": "/D' M t' M u/",
  "30adj10": "/U M' u'/", "-30adj0-1": "/U' M u/",
  "03adj10": "/D M' d'/",
  "obopp00": "1,0/M' F M' F M'/0,1",
  "oaopp1-1": "0,1/M' u' M' u' M'/0,1",
  "but00": "", "also00": "", "done!00": "0,0",
};

// User-editable one-off string replacements applied before anything else.
export const tempReplacements = {};

// Set of user-registered extra shorthands (populated externally if needed).
export const extraShorthands = new Set();

const GOOD_FINISHES = new Set([
  "11", "-1-1", "22", "-2-2", "2-1", "-21", "1-2", "-12",
  "30", "-30", "03", "0-3", "33", "3-3", "-3-3", "-33",
  "41", "-4-1", "14", "-1-4", "2-4", "-24", "4-2", "-42",
  "5-1", "-51", "-45", "-54", "63",
]);

export const CLOSEST_MAP = new Map([
  [-5, -6], [-4, -3], [-3, -3], [-2, -3], [-1, 0], [0, 0],
  [1, 0], [2, 3], [3, 3], [4, 3], [5, 6], [6, 6],
]);

export const MOVE_VALUES = new Map([
  // aligned top, upslice
  ["A/0,3", 16], ["A/0,6", 1], ["A/0,-3", 18],
  ["A/3,0", 16], ["A/3,3", 12], ["A/3,6", 0], ["A/3,-3", 13],
  ["A/6,0", 12], ["A/6,3", 11], ["A/6,6", 2], ["A/6,-3", 12],
  ["A/-3,0", 9], ["A/-3,3", 13], ["A/-3,6", 4], ["A/-3,-3", 12],
  // aligned top, downslice
  ["A\\0,3", 17], ["A\\0,6", 1], ["A\\0,-3", 8],
  ["A\\3,0", 6], ["A\\3,3", 14], ["A\\3,6", 1], ["A\\3,-3", 12],
  ["A\\6,0", 14], ["A\\6,3", 11], ["A\\6,6", 5], ["A\\6,-3", 8],
  ["A\\-3,0", 11], ["A\\-3,3", 14], ["A\\-3,6", 6], ["A\\-3,-3", 9],
  // unaligned top, upslice
  ["a/0,3", 5], ["a/0,6", 5], ["a/0,-3", 12],
  ["a/3,0", 17], ["a/3,3", 10], ["a/3,6", 5], ["a/3,-3", 7],
  ["a/6,0", 4], ["a/6,3", 2], ["a/6,6", 0], ["a/6,-3", 3],
  ["a/-3,0", 18], ["a/-3,3", 12], ["a/-3,6", 7], ["a/-3,-3", 11],
  // unaligned top, downslice
  ["a\\0,3", 5], ["a\\0,6", 5], ["a\\0,-3", 5],
  ["a\\3,0", 16], ["a\\3,3", 11], ["a\\3,6", 4], ["a\\3,-3", 6],
  ["a\\6,0", 4], ["a\\6,3", 2], ["a\\6,6", 0], ["a\\6,-3", 1],
  ["a\\-3,0", 15], ["a\\-3,3", 10], ["a\\-3,6", 2], ["a\\-3,-3", 5],
  // fractional moves — alignment prefix omitted
  ["/1,-2", 4], ["\\1,-2", 17], ["/-1,2", 15], ["\\-1,2", 14],
  ["/1,-5", 3], ["\\1,-5", 1], ["/-1,5", 8], ["\\-1,5", 3],
  ["/1,4", 7], ["\\1,4", 14], ["/-1,-4", 12], ["\\-1,-4", 9],
  ["/1,1", 11], ["\\1,1", 20], ["/-1,-1", 20], ["\\-1,-1", 10],
  ["/2,-1", 20], ["\\2,-1", 12], ["/-2,1", 14], ["\\-2,1", 18],
  ["/2,2", 12], ["\\2,2", 13], ["/-2,-2", 14], ["\\-2,-2", 8],
  ["/2,5", 5], ["\\2,5", 3], ["/-2,-5", 4], ["\\-2,-5", 3],
  ["/2,-4", 14], ["\\2,-4", 6], ["/-2,4", 13], ["\\-2,4", 13],
  ["/4,4", 5], ["\\4,4", 12], ["/-4,-4", 12], ["\\-4,-4", 4],
  ["/4,1", 6], ["\\4,1", 13], ["/-4,-1", 16], ["\\-4,-1", 6],
  ["/4,-2", 12], ["\\4,-2", 9], ["/-4,2", 16], ["\\-4,2", 13],
  ["/4,-5", 2], ["\\4,-5", 5], ["/-4,5", 13], ["\\-4,5", 3],
  ["/5,5", 1], ["\\5,5", 4], ["/-5,-5", 2], ["\\-5,-5", 0],
  ["/5,2", 6], ["\\5,2", 10], ["/-5,-2", 12], ["\\-5,-2", 13],
  ["/5,-1", 11], ["\\5,-1", 7], ["/-5,1", 14], ["\\-5,1", 15],
  ["/5,-4", 2], ["\\5,-4", 2], ["/-5,4", 12], ["\\-5,4", 14],
]);


// =============================================================================
// SECTION 2 — CORE UTILITIES  (from karn.js)
// =============================================================================

export function dictReplace(str, dict) {
  const pattern = new RegExp(
    Object.keys(dict).map(k => k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|"),
    "g"
  );
  let prev;
  do { prev = str; str = str.replace(pattern, m => dict[m]); } while (str !== prev);
  return str;
}

export function isKarn(str) {
  return /[a-zA-Z]/.test(str.replace(/[0-9\s\/\\,\-()']/g, ""));
}

export function legalMove(m) {
  m = parseInt(m, 10);
  if (m < -5) return m + 12;
  if (m > 6) return m - 12;
  return m;
}

export function changesAlignment(m) {
  return m % 3 !== 0;
}

// addMoves — adds two "top,bot" move strings.
export function addMoves(move1, move2) {
  const [u1, d1] = move1.split(",").map(Number);
  const [u2, d2] = move2.split(",").map(Number);
  return `${legalMove(u1 + u2)},${legalMove(d1 + d2)}`;
}

// Backward-compat alias (numeric-only, no A/a handling).
export function addMovesStr(move1, move2) {
  return addMoves(move1, move2);
}

export function getAlignment(topA, bottomA) {
  return (topA ? "1" : "0") + (bottomA ? "-1" : "0");
}


// =============================================================================
// SECTION 3 — UNKARNIFY PIPELINE
// =============================================================================

export function unkarnifyHelp(scramble) {
  scramble = scramble.replaceAll("/", " / ");
  return dictReplace(" " + scramble + " ", karnToWCA)
    .trim()
    .replaceAll(/ ?\/( \/?)*/g, "/")
    .replaceAll(/\s+/g, "/");
}

// addCommas — expands compact karn numeric tokens e.g. "2-1" → "2,-1".
export function addCommas(scramble) {
  return scramble.split(" ").map(move => {
    if (!move || isNaN(Number(move.replaceAll("-", "")))) return move;
    switch (move.length) {
      case 1: return move + ",0";
      case 2: return move[0] === "-" ? move + ",0" : move[0] + "," + move[1];
      case 3: return move[0] === "-" ? move.slice(0, 2) + "," + move[2]
        : move[0] + "," + move.slice(1);
      case 4: return move.slice(0, 2) + "," + move.slice(2);
      default: throw new Error(`"${move}" is not a valid karn numeric move`);
    }
  }).join(" ");
}

export function replaceShorthands(scramble) {
  const moves = scramble.split("/");

  const allKnown = moves.every(m => !m || (" " + m + " " in karnToWCA));
  if (allKnown) return unkarnifyHelp(scramble);

  const alignmentIndependent = new Set([
    "bjj", "fjj", "nn", "jn", "nj", "e2bjj", "e2fjj",
    "jj", "bjj+e2", "-nn", "-jn", "-nj",
  ]);

  let topA = false, bottomA = false;
  for (const move of moves) {
    if (!move) continue;
    if (move.includes(",")) {
      const [u, d] = move.split(",");
      if (parseInt(u, 10) % 3 !== 0) topA = !topA;
      if (parseInt(d, 10) % 3 !== 0) bottomA = !bottomA;
    } else {
      const key = alignmentIndependent.has(move.toLowerCase())
        ? move.toLowerCase()
        : move.toLowerCase() + getAlignment(topA, bottomA);
      if (!(key in shorthandToKarn) && !extraShorthands.has(key)) return scramble;
      const replacement = shorthandToKarn[key];
      if (replacement === undefined)
        throw new Error(`"${move}" with alignment ${getAlignment(topA, bottomA)} is not defined.`);
      scramble = scramble.replace(move, replacement);
      for (const sub of unkarnifyHelp(replacement).split("/")) {
        if (!sub) continue;
        const [u, d] = sub.split(",");
        if (parseInt(u, 10) % 3 !== 0) topA = !topA;
        if (parseInt(d, 10) % 3 !== 0) bottomA = !bottomA;
      }
    }
  }
  scramble = scramble
    .replaceAll(/ *\/ */g, "/")
    .replaceAll(/\/\//g, "/")
    .replaceAll(/\//g, " ");
  return unkarnifyHelp(scramble);
}

export function unkarnify(scramble) {
  if (scramble in tempReplacements) scramble = tempReplacements[scramble];
  if (scramble.includes("meow")) return scramble;

  let isPScramble = /^p[ /\\|]/.test(scramble);
  if (isPScramble) scramble = scramble.slice(2, -3);

  scramble = scramble
    .replaceAll("&", "-1").replaceAll("^", "-2")
    .replaceAll("9", "-3").replaceAll("8", "-4").replaceAll("7", "-5");

  const firstToken = scramble.match(/^[^\/\\ ]*/)?.[0] ?? "";
  const firstSlice = scramble.startsWith("/") || scramble.startsWith("\\") ||
    scramble.startsWith("|") || (" " + firstToken + " " in karnToWCA);
  const lastToken = scramble.match(/[^\/\\ ]*$/)?.[0] ?? "";
  const lastSlice = " " + lastToken + " " in karnToWCA;

  for (const group of scramble.matchAll(/(\(.*?\))(\d+)/g)) {
    const inner = group[1].replaceAll(/[()]/g, "");
    const count = parseInt(group[2], 10);
    scramble = scramble.replace(group[0], Array(count).fill(inner).join(" "));
  }

  scramble = scramble
    .replaceAll(/[\/\\|]/g, " ")
    .replaceAll(/[()]/g, "")
    .replaceAll(/ +/g, " ");

  scramble = addCommas(scramble);
  let final = replaceShorthands(unkarnifyHelp(scramble));

  if (firstSlice) final = "/" + final;
  if (lastSlice) final = final + "/";
  if (isPScramble) final = "p/" + final + "/p'";
  final = final.replaceAll(/\/+/g, "/");
  return final;
}


// =============================================================================
// SECTION 4 — KARNIFY  (from karn.js)
// =============================================================================

export function karnify(scramble) {
  const startsSlice = ["/", "\\"].includes(scramble.charAt(0));
  let s = scramble.replaceAll("/", " ").replaceAll("\\", " ");
  s = dictReplace(" " + s.trim() + " ", wcaToKarn).trim();
  return (startsSlice ? "/" : "") + s.replaceAll(/ {2,}/g, " ").replaceAll(",", "");
}


// =============================================================================
// SECTION 5 — ERGONOMICS RATING  (from karn.js)
// =============================================================================

export function getMoveValue(startA, upslice, move) {
  const comma = move.indexOf(",");
  const topVal = parseInt(move.slice(0, comma), 10);
  const sl = upslice ? "/" : "\\";
  const key = topVal % 3 === 0 ? (startA ? "A" : "a") + sl + move : sl + move;
  return MOVE_VALUES.get(key) ?? 5;
}

export function getOverwork(moves) {
  const tops = [], bots = [];
  for (const m of moves) {
    const c = m.indexOf(",");
    if (c === -1) { tops.push(0); bots.push(0); continue; }
    tops.push(parseInt(m.slice(0, c), 10) || 0);
    bots.push(parseInt(m.slice(c + 1), 10) || 0);
  }
  let movement = 0, bonus = 0, streak = 0, closestMov = 0, buffer = 0;
  for (const t of tops) {
    if (t === 6 || t < 0) {
      streak++; closestMov += Math.abs(CLOSEST_MAP.get(t) ?? 0); buffer += Math.abs(t);
      if (streak > 1 && closestMov > 3) { movement += buffer; buffer = 0; }
    } else { streak = 0; closestMov = 0; buffer = 0; }
  }
  streak = 0; closestMov = 0; buffer = 0;
  for (const b of bots) {
    if (b > 0) {
      streak++; closestMov += Math.abs(CLOSEST_MAP.get(b) ?? 0); buffer += Math.abs(b);
      if (streak > 1 && closestMov > 3) { movement += buffer; buffer = 0; }
    } else { streak = 0; closestMov = 0; buffer = 0; }
  }
  for (let i = 0; i + 1 < tops.length; i++) {
    if (tops[i] + tops[i + 1] !== 0) bonus++;
    if (bots[i] + bots[i + 1] !== 0) bonus++;
  }
  return { movement, bonus };
}

export function rateAlg(algRaw, initialTopA = false, weights = {}) {
  const W1 = weights.W1 ?? 34;
  const W2 = weights.W2 ?? 100;
  const W3 = weights.W3 ?? 38;
  const W4 = weights.W4 ?? 500;
  const W5 = weights.W5 ?? 10;

  let a = algRaw.replace(/\[.*$/, "").trim();
  const numeric = isKarn(a) ? unkarnify(a) : a.replaceAll(" ", "");

  const rawParts = numeric.split("/");
  const r = rawParts.filter((pt, i) => i === 0 || pt.trim() !== "").map(p => p.trim());
  if (r.length < 2) return { score: W4, sliceStart: " " };

  const sliceCount = r.length - 1;
  if (sliceCount <= 0) return { score: W4, sliceStart: " " };

  let ergoUp = 0, ergoDown = 0, isTopA = false, oddSlice = true;
  for (let i = 0; i < r.length - 1; i++) {
    if (i === 0) {
      const c = r[i].indexOf(",");
      const t = c !== -1 ? (parseInt(r[i].slice(0, c), 10) || 0) : 0;
      isTopA = initialTopA !== (t % 3 !== 0);
      oddSlice = true;
      continue;
    }
    ergoUp += getMoveValue(isTopA, oddSlice, r[i]);
    ergoDown += getMoveValue(isTopA, !oddSlice, r[i]);
    const c = r[i].indexOf(",");
    const t = c !== -1 ? (parseInt(r[i].slice(0, c), 10) || 0) : 0;
    isTopA = isTopA !== (t % 3 !== 0);
    oddSlice = !oddSlice;
  }

  const phase1 = W1 * Math.max(ergoUp, ergoDown) / sliceCount;
  let sliceStart = " ";
  if (Math.abs(ergoUp - ergoDown) / sliceCount > 5)
    sliceStart = ergoUp > ergoDown ? "/" : "\\";

  const phase2 = W2 * sliceCount;
  const { movement, bonus } = getOverwork(r.slice(1, -1));
  return {
    score: phase1 - phase2 - W3 * movement / sliceCount + bonus * W5 / sliceCount + W4,
    sliceStart,
  };
}

export function rateAndSort(algLines, posHex = "", useKarn = true) {
  let initialTopA = false;
  if (posHex) {
    const ch = posHex[0];
    initialTopA = /[0-9XYZ]/i.test(ch);
  }
  return algLines.map(line => {
    const bracketPos = line.indexOf("[");
    const algOnly = bracketPos > 0 ? line.slice(0, bracketPos).trim() : line.trim();
    let result = { alg: line, score: 500 };
    let rated = false, sliceStart = " ";
    try {
      const numericAlg = isKarn(algOnly) ? unkarnify(algOnly) : algOnly;
      ({ score: result.score, sliceStart } = rateAlg(numericAlg, initialTopA));
      rated = true;
    } catch (_) { /* leave defaults */ }
    if (rated && (sliceStart === "/" || sliceStart === "\\")) {
      const algPart = bracketPos > 0 ? line.slice(0, bracketPos) : line;
      const rest = bracketPos > 0 ? line.slice(bracketPos) : "";
      const slashPos = algPart.indexOf("/");
      if (slashPos >= 0)
        result.alg = algPart.slice(0, slashPos) + sliceStart + algPart.slice(slashPos + 1) + rest;
    }
    return result;
  }).sort((a, b) => b.score - a.score);
}


// =============================================================================
// SECTION 6 — NORMALIZE
// =============================================================================

function sepIndex(a) {
  let inx = 0;
  for (const ch of a) { inx++; if (/\d/.test(ch)) break; }
  return inx;
}

function compl(a) {
  const inx = sepIndex(a);
  return String(legalMove(6 + parseInt(a.slice(0, inx), 10))) +
    String(legalMove(6 + parseInt(a.slice(inx), 10)));
}

function lf(a) {
  const inx = sepIndex(a);
  return a.slice(inx) + a.slice(0, inx);
}

function comma(a) {
  const inx = sepIndex(a);
  return a.slice(0, inx) + "," + a.slice(inx);
}

// algToInternal — parse any input format into space-separated no-comma compact
// segments, e.g. "30 -33 30".  Uses full unkarnify for Karn input.
function algToInternal(algIn) {
  let alg = algIn.replace(/\[.*?\]/g, "").trim();
  if (isKarn(alg)) {
    const numeric = unkarnify(alg);
    return numeric.split("/").filter(p => p.trim()).map(m => {
      if (!m.includes(",")) return "00";
      const [u, d] = m.split(",");
      return String(legalMove(parseInt(u, 10) || 0)) +
        String(legalMove(parseInt(d, 10) || 0));
    }).join(" ");
  }
  alg = alg.replace(/[()]/g, "");
  if (alg.includes("/")) {
    return alg.replace(/ /g, "").split("/").filter(p => p).map(m => {
      const [u, d] = m.split(",");
      return String(legalMove(parseInt(u, 10) || 0)) +
        String(legalMove(parseInt(d, 10) || 0));
    }).join(" ");
  }
  alg = alg.replace(/ +/g, " ").trim();
  return alg.split(" ").filter(p => p).map(m => {
    const p = m.includes(",")
      ? m.split(",")
      : [m.slice(0, sepIndex(m)), m.slice(sepIndex(m))];
    return String(legalMove(parseInt(p[0], 10) || 0)) +
      String(legalMove(parseInt(p[1], 10) || 0));
  }).join(" ");
}

// countY2Positions — number of interior positions where a Y2 can be inserted.
export function countY2Positions(algIn) {
  try {
    const segs = algToInternal(algIn).split(" ").filter(p => p);
    return Math.max(0, segs.length - 3);
  } catch { return 0; }
}

// normalize — applies explicit 2s at the positions listed in lfLst (1-based),
// optimizes, and returns the result with optional comment annotations.
// `leave` param is kept for API compatibility but normalization (auto-complement)
// has been removed; only explicit lfLst Y2s are applied
export function normalize(algIn, lfLst, k = null, leave = true) {
  let alg = algIn.replace(/\[.*?\]/g, "").trim();
  if (!lfLst || lfLst.length === 0) lfLst = [];

  const ki = isKarn(alg);
  const kOut = k === null ? ki : k;

  // Parse to internal space-separated no-comma format
  alg = algToInternal(algIn);
  let alst = alg.split(" ").filter(p => p);

  // Save boundary compact values now — optimize may merge them into adjacent moves
  const boundaryStart = alst[0];
  const boundaryEnd = alst[alst.length - 1];

  // Apply explicit y2s to interior moves
  let lfing = false, facingD = false;
  for (let i = 1; i <= alst.length - 3; i++) {
    let m = alst[i];
    m = facingD ? lf(m) : m;
    if (lfLst.includes(i)) { m = compl(m); lfing = !lfing; }
    facingD = lfing ? !facingD : facingD;
    alst[i] = m;
  }

  // Fix last interior move
  const lastMoveIdx = alst.length - 2;
  alst[lastMoveIdx] = facingD ? lf(alst[lastMoveIdx]) : alst[lastMoveIdx];
  alst[lastMoveIdx] = (lfing !== facingD) ? compl(alst[lastMoveIdx]) : alst[lastMoveIdx];
  const lastMove = alst[lastMoveIdx];

  // Add commas to all segments including boundaries
  for (let i = 0; i < alst.length; i++) alst[i] = comma(alst[i]);
  alg = alst.join('/');

  // Build comment
  let comment = GOOD_FINISHES.has(lastMove) ? '' : ' (bad finish)';
  const topAligned = seg => parseInt(seg.slice(0, sepIndex(seg)), 10) % 3 === 0;
  if (topAligned(boundaryStart) !== topAligned(boundaryEnd)) comment += ' (alignment changes)';

  if (kOut) {
    alg = karnify(alg);
  }

  return alg + comment;
}


// =============================================================================
// SECTION 7 — OBLP TRAINER
// =============================================================================

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
  ['', 'solved', 'solved'],
  ['', '1c', '1c'], ['', 'cadj', 'cadj'], ['', 'cadj', 'copp'], ['', 'copp', 'copp'],
  ['', '3c', '3c'], ['', '4e', '4e'], ['', '3e', '3e'], ['', 'line', 'line'],
  ['', 'L', 'line'], ['', 'L', 'L'], ['', '1e', '1e'],
  ['good', 'pair', 'pair'], ['bad', 'pair', 'pair'],
  ['good', 'arrow', 'pair'], ['bad', 'arrow', 'pair'],
  ['good', 'arrow', 'arrow'], ['bad', 'arrow', 'arrow'],
  ['', 'gem', 'gem'], ['', 'gem', 'knight'], ['', 'gem', 'axe'], ['', 'gem', 'squid'],
  ['good', 'knight', 'knight'], ['bad', 'knight', 'knight'],
  ['good', 'knight', 'axe'], ['bad', 'knight', 'axe'],
  ['same', 'axe', 'axe'], ['diff', 'axe', 'axe'],
  ['', 'squid', 'knight'], ['', 'squid', 'axe'], ['', 'squid', 'squid'],
  ['good', 'thumb', 'thumb'], ['bad', 'thumb', 'thumb'],
  ['good', 'thumb', 'bunny'], ['bad', 'thumb', 'bunny'],
  ['good', 'bunny', 'bunny'], ['bad', 'bunny', 'bunny'],
  ['', 'shell', 'shell'], ['', 'shell', 'bird'], ['', 'shell', 'hazard'],
  ['', 'yoshi', 'shell'],
  ['good', 'bird', 'bird'], ['bad', 'bird', 'bird'],
  ['', 'bird', 'hazard'], ['', 'hazard', 'hazard'],
  ['good', 'yoshi', 'bird'], ['bad', 'yoshi', 'bird'],
  ['', 'yoshi', 'hazard'], ['same', 'yoshi', 'yoshi'], ['diff', 'yoshi', 'yoshi'],
  ['good', 'kite', 'kite'], ['bad', 'kite', 'kite'],
  ['good', 'kite', 'cut'], ['bad', 'kite', 'cut'],
  ['', 'kite', 'T'], ['good', 'kite', 'N'], ['bad', 'kite', 'N'], ['', 'kite', 'tie'],
  ['', 'cut', 'T'], ['good', 'cut', 'N'], ['bad', 'cut', 'N'], ['', 'cut', 'tie'],
  ['good', 'cut', 'cut'], ['bad', 'cut', 'cut'],
  ['good', 'T', 'T'], ['bad', 'T', 'T'], ['', 'T', 'N'],
  ['good', 'T', 'tie'], ['bad', 'T', 'tie'],
  ['good', 'N', 'N'], ['bad', 'N', 'N'], ['', 'tie', 'N'],
  ['good', 'tie', 'tie'], ['bad', 'tie', 'tie']
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
  'good pair/pair': ['left pair/left pair', 'right pair/right pair'],
  'bad pair/pair': ['left pair/right pair'],
  'good arrow/pair': ['left arrow/right pair', 'right arrow/left pair'],
  'bad arrow/pair': ['left arrow/left pair', 'right arrow/right pair'],
  'good arrow/arrow': ['left arrow/left arrow', 'right arrow/right arrow'],
  'bad arrow/arrow': ['left arrow/right arrow'],
  'gem/gem': ['gem/gem'],
  'gem/knight': ['gem/left knight', 'gem/right knight'],
  'gem/axe': ['gem/left axe', 'gem/right axe'],
  'gem/squid': ['gem/squid'],
  'good knight/knight': ['left knight/right knight'],
  'bad knight/knight': ['left knight/left knight', 'right knight/right knight'],
  'good knight/axe': ['left knight/left axe', 'right knight/right axe'],
  'bad knight/axe': ['left knight/right axe', 'right knight/left axe'],
  'same axe/axe': ['left axe/left axe', 'right axe/right axe'],
  'diff axe/axe': ['left axe/right axe'],
  'squid/knight': ['squid/left knight', 'squid/right knight'],
  'squid/axe': ['squid/left axe', 'squid/right axe'],
  'squid/squid': ['squid/squid'],
  'good thumb/thumb': ['left thumb/left thumb', 'right thumb/right thumb'],
  'bad thumb/thumb': ['left thumb/right thumb'],
  'good thumb/bunny': ['left thumb/right bunny', 'right thumb/left bunny'],
  'bad thumb/bunny': ['left thumb/left bunny', 'right thumb/right bunny'],
  'good bunny/bunny': ['left bunny/left bunny', 'right bunny/right bunny'],
  'bad bunny/bunny': ['left bunny/right bunny'],
  'shell/shell': ['shell/shell'],
  'shell/bird': ['shell/left bird', 'shell/right bird'],
  'shell/hazard': ['shell/hazard'],
  'yoshi/shell': ['left yoshi/shell', 'right yoshi/shell'],
  'good bird/bird': ['left bird/right bird'],
  'bad bird/bird': ['left bird/left bird', 'right bird/right bird'],
  'bird/hazard': ['left bird/hazard', 'right bird/hazard'],
  'hazard/hazard': ['hazard/hazard'],
  'good yoshi/bird': ['left yoshi/left bird', 'right yoshi/right bird'],
  'bad yoshi/bird': ['left yoshi/right bird', 'right yoshi/left bird'],
  'yoshi/hazard': ['left yoshi/hazard', 'right yoshi/hazard'],
  'same yoshi/yoshi': ['left yoshi/left yoshi', 'right yoshi/right yoshi'],
  'diff yoshi/yoshi': ['left yoshi/right yoshi'],
  'good kite/kite': ['left kite/left kite', 'right kite/right kite'],
  'bad kite/kite': ['left kite/right kite'],
  'good kite/cut': ['left kite/left cut', 'right kite/right cut'],
  'bad kite/cut': ['left kite/right cut', 'right kite/left cut'],
  'kite/T': ['left kite/black T', 'left kite/white T', 'right kite/black T', 'right kite/white T'],
  'good kite/N': ['left kite/right N', 'right kite/left N'],
  'bad kite/N': ['left kite/left N', 'right kite/right N'],
  'kite/tie': ['left kite/black tie', 'left kite/white tie', 'right kite/black tie', 'right kite/white tie'],
  'cut/T': ['left cut/black T', 'left cut/white T', 'right cut/black T', 'right cut/white T'],
  'good cut/N': ['left cut/left N', 'right cut/right N'],
  'bad cut/N': ['left cut/right N', 'right cut/left N'],
  'cut/tie': ['left cut/black tie', 'left cut/white tie', 'right cut/black tie', 'right cut/white tie'],
  'good cut/cut': ['left cut/left cut', 'right cut/right cut'],
  'bad cut/cut': ['left cut/right cut'],
  'good T/T': ['black T/black T', 'white T/white T'],
  'bad T/T': ['black T/white T'],
  'T/N': ['black T/left N', 'black T/right N', 'white T/left N', 'white T/right N'],
  'good T/tie': ['black T/black tie', 'white T/white tie'],
  'bad T/tie': ['black T/white tie', 'white T/black tie'],
  'good N/N': ['left N/left N', 'right N/right N'],
  'bad N/N': ['left N/right N'],
  'tie/N': ['black tie/left N', 'black tie/right N', 'white tie/left N', 'white tie/right N'],
  'good tie/tie': ['black tie/black tie', 'white tie/white tie'],
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

function isOblCase(l, target) {
  const targetPattern = Object.entries(OBL_PATTERNS).find(([, v]) => v === target)?.[0];
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
  const bw = ['W', 'W', 'w', 'W', 'W', 'w', 'W', 'W', 'w', 'W', 'W', 'w'];
  for (const ch of m) {
    const num = parseInt(ch);
    if (num % 2 !== 0) {
      // corner
      bw[Math.floor(num / 2) * 3] = 'B';
      bw[Math.floor(num / 2) * 3 + 1] = 'B';
    } else {
      // edge
      bw[Math.floor(num / 2) * 3 - 1] = 'b';
    }
  }
  const obl = bw.join('');
  for (const [, name] of Object.entries(OBL_PATTERNS)) {
    if (isOblCase(obl, name)) return name;
  }
  throw new Error('OBL not found: ' + obl);
}

export function toCaseName(m) {
  const [u, d] = m.split(' ');
  return getNonSpe(`${toLayerName(u)}/${toLayerName(d)}`);
}

export function sortOblp(seq) {
  return [...seq].sort((a, b) => parseInt(a) - parseInt(b)).join('');
}

// Trainer data
export const CORNERS = [[''], ['1', '3', '5', '7'], ['13', '15', '17', '35', '37', '57'], ['135', '137', '157', '357'], ['1357']];
export const EDGES = [[''], ['2', '4', '6', '8'], ['24', '26', '28', '46', '48', '68'], ['246', '248', '268', '468'], ['2468']];
export const TOTAL_CORNERS = ['', '1', '3', '5', '7', '13', '15', '17', '35', '37', '57', '135', '137', '157', '357', '1357'];
export const TOTAL_EDGES = ['', '2', '4', '6', '8', '24', '26', '28', '46', '48', '68', '246', '248', '268', '468', '2468'];

// nav.js — injects the shared nav into any page
// Usage: import './nav.js' and call buildNav(activePath)

export const TOOLS = [
  { path: 'average', label: 'Avg Gen',      longLabel: 'Average Generator',         color: '#ffd500' },
  { path: 'stats',   label: 'Avg Stats',    longLabel: 'Average Statistics',         color: '#009b48' },
  { path: 'aox',     label: 'AoX List',     longLabel: 'Average of X List',          color: '#0046ad' },
  { path: 'subx',    label: 'Sub-X Count',  longLabel: 'Sub-X Count',                color: '#9855d4' },
  { path: 'mean',    label: 'Mean Gen',     longLabel: 'Mean of 3 Generator',        color: '#ff5800' },
  { path: 'add',     label: 'Time Add',     longLabel: 'Time Adder',                 color: '#c41e3a' },
  { path: 'filter',  label: 'Alg Filter',   longLabel: 'Algorithm Filter',           color: '#00a6d6' },
  { path: 'mega',    label: 'Mega Scram',   longLabel: 'Megaminx Scramble Converter',color: '#ff6b6b' },
  { path: 'sq1',     label: 'SQ1 Norm',     longLabel: 'Square-1 Normalizer',        color: '#ffa500' },
  { path: 'oblp',    label: 'OBLP',         longLabel: 'OBLP Trainer',               color: '#a0e080' },
  { path: 'notation',label: 'Notation',     longLabel: 'Notation Converter',         color: '#e0a0ff' },
];

export function buildNav(activePath) {
  const base = activePath ? '../' : './';

  const nav = document.getElementById('nav');
  if (!nav) return;

  const activeColor = TOOLS.find(t => t.path === activePath)?.color ?? '#ffd500';
  document.documentElement.style.setProperty('--tool-color', activeColor);

  nav.innerHTML = `
    <div class="nav-inner">
      <a class="nav-logo" href="${base}">cubing <em>tools</em></a>
      <div class="nav-sep"></div>
      <div class="nav-tools">
        ${TOOLS.map(t => `
          <a class="nav-tool ${activePath === t.path ? 'active' : ''}"
             style="--tool-color:${t.color}"
             href="${base}${t.path}/">${t.label}</a>
        `).join('')}
      </div>
    </div>`;
}

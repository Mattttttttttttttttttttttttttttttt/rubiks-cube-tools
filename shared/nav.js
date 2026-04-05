// nav.js — injects the shared nav into any page
// Usage: import './nav.js' and call buildNav(activePath)

export const TOOLS = [
  { path: 'average', label: 'Average Gen',    color: '#ffd500' },
  { path: 'stats',   label: 'Avg Stats',      color: '#009b48' },
  { path: 'aox',     label: 'AoX List',       color: '#0046ad' },
  { path: 'subx',    label: 'Sub-X Count',    color: '#9855d4' },
  { path: 'mean',    label: 'Mean Gen',        color: '#ff5800' },
  { path: 'add',     label: 'Time Add',        color: '#c41e3a' },
  { path: 'filter',  label: 'Alg Filter',      color: '#00a6d6' },
  { path: 'mega',    label: 'Mega Scram',      color: '#ff6b6b' },
  { path: 'sq1',     label: 'SQ1 Norm',       color: '#ffa500' },
  { path: 'oblp',    label: 'OBLP Trainer',   color: '#a0e080' },
  { path: 'notation',label: 'Notation',        color: '#e0a0ff' },
];

export function buildNav(activePath) {
  // Detect depth: if we're in a subdir, go up one level
  const here = window.location.pathname;
  const depth = here.split('/').filter(Boolean).length;
  // base is relative — 0 depth = './', 1 depth = '../', etc.
  // We'll just use relative from the tool page (one level deep from root)
  const base = activePath ? '../' : './';

  const nav = document.getElementById('nav');
  if (!nav) return;

  const activeColor = TOOLS.find(t => t.path === activePath)?.color ?? '#ffd500';
  document.documentElement.style.setProperty('--tool-color', activeColor);

  nav.innerHTML = `
    <div class="nav-inner">
      <a class="nav-logo" href="${base}index.html"><em>cube</em>tools</a>
      <div class="nav-sep"></div>
      <div class="nav-tools">
        ${TOOLS.map(t => `
          <a class="nav-tool ${activePath === t.path ? 'active' : ''}"
             style="--tool-color:${t.color}"
             href="${base}${t.path}/index.html">${t.label}</a>
        `).join('')}
      </div>
    </div>`;
}

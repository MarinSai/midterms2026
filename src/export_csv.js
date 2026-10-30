// Exporte les données de sondages de la page forecast en CSV (data/sondages-*.csv),
// lus par le Google Sheets de l'Observatoire via IMPORTDATA. Lancé par build.py.
const fs = require('fs'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, 'forecast.dc.html'), 'utf8');
const cls = src.slice(src.indexOf('class Component'), src.lastIndexOf('</script>'));
global.DCLogic = class {};
const C = eval('(' + cls.replace(/^class Component/, 'class') + ')');
const c = Object.create(C.prototype);
const POLLS = c.polls(), COOK = c.cookSenate(), HOUSE = c.houseData(), RACES = c.races(), NAMES = c.names();
const COOKL = ['Démocrate sûr', 'Démocrate probable', 'Penche démocrate', 'Indécis', 'Penche républicain', 'Républicain probable', 'Républicain sûr'];
const PARTY = { D: 'Démocrate', R: 'Républicain', I: 'Indépendant', O: 'Autre' };
const last = (n) => n.replace(/ (Jr\.|Sr\.|II|III)$/, '').split(' ').slice(-1)[0];
// Nom complet à partir du nom de famille utilisé dans la base de sondages
const full = (n, cands) => { const m = cands.filter((k) => last(k[0]) === n || k[0] === n); return m.length === 1 ? m[0][0] : n; };
const q = (v) => (v == null ? '' : typeof v === 'number' ? String(v) : /[",\n]/.test(String(v)) ? '"' + String(v).replace(/"/g, '""') + '"' : String(v));
const csv = (rows) => rows.map((r) => r.map(q).join(',')).join('\n') + '\n';
const pollCols = (p, cands) => {
  if (!p) return ['', '', '', '', '', '', '', '', ''];
  const s = [...p.c].sort((a, b) => b[2] - a[2]);
  const o = s.slice(2).map((k) => full(k[0], cands) + ' (' + k[1] + ') ' + k[2].toFixed(1).replace('.', ',')).join(' ; ');
  return [full(s[0][0], cands), s[0][1], s[0][2], s[1] ? full(s[1][0], cands) : '', s[1] ? s[1][1] : '', s[1] ? s[1][2] : '', p.n, p.f, o];
};
const out = path.join(__dirname, '..', 'data');

// Sénat
const S = [['État', 'Code', 'Siège détenu par', 'Sortant candidat', 'Remarque', 'Classement Cook', 'Candidats (* sortant)', 'Candidat en tête', 'Parti', 'Moyenne (%)', 'Deuxième', 'Parti', 'Moyenne (%)', 'Sondages', 'Instituts', 'Autres candidats (moyenne %)']];
for (const st of Object.keys(RACES).sort((a, b) => NAMES[a].localeCompare(NAMES[b], 'fr'))) {
  const [type, holder, , , cands] = RACES[st], p = POLLS['S:' + st];
  const inc = cands.find((k) => k[2]);
  const list = cands.map((k) => k[0] + (k[2] ? '*' : '') + ' (' + k[1] + ')').join(' ; ');
  const pc = p ? pollCols(p, cands) : ['', '', '', '', '', '', '', '', 'Pas de moyenne Silver Bulletin (il en faut au moins trois, de deux instituts)'];
  S.push([NAMES[st], st, PARTY[holder], inc ? inc[0] : (type === 'Sortant battu' ? 'Aucun (sortant battu à la primaire)' : 'Siège ouvert'), type === 'Partielle' ? 'Élection partielle' : type === 'Sortant battu' ? 'Sortant battu à la primaire' : '', COOKL[COOK[st]], list, ...pc]);
}
fs.writeFileSync(path.join(out, 'sondages-senat.csv'), csv(S));

// Chambre
const H = [['Circonscription', 'État', 'Siège détenu par', 'Classement Cook', 'Candidats (* sortant)', 'Candidat en tête', 'Parti', 'Moyenne (%)', 'Deuxième', 'Parti', 'Moyenne (%)', 'Sondages', 'Instituts', 'Autres candidats (moyenne %)']];
const ord = (id) => id.slice(0, 2) + (id.endsWith('AL') ? '00' : id.slice(3).padStart(2, '0'));
for (const id of Object.keys(HOUSE).sort((a, b) => ord(a).localeCompare(ord(b)))) {
  const [holder, cook, cands] = HOUSE[id], p = POLLS['H:' + id];
  const list = cands.map((k) => k[0] + (k[2] ? '*' : '') + ' (' + k[1] + ')').join(' ; ');
  H.push([id, NAMES[id.slice(0, 2)], PARTY[holder], COOKL[cook], list, ...pollCols(p, cands)]);
}
fs.writeFileSync(path.join(out, 'sondages-chambre.csv'), csv(H));

// Vote générique
const G = POLLS.GB;
fs.writeFileSync(path.join(out, 'vote-generique.csv'), csv([['Parti', 'Moyenne (%)', 'Sondages', 'Instituts'], ...G.c.map((k) => [k[0] === 'Democrats' ? 'Démocrates' : k[0] === 'Republicans' ? 'Républicains' : k[0], k[2], G.n, G.f])]));
console.log('csv', S.length - 1, H.length - 1);

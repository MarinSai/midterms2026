# Construit les trois pages du site à partir des maquettes du canevas :
#   midterms/           résultats du scrutin (vide tant qu'aucun flux réel n'est branché)
#   midterms-test/      maquette avec résultats fictifs (scénarios ?scenario=avant|soiree|final)
#   midterm-forecast/   état des courses (classements Cook, moyennes Silver Bulletin)
import pathlib
d = pathlib.Path(__file__).parent
def build(dc, shell, out):
    s = (d / dc).read_text()
    comp = s[s.index('class Component'):s.rindex('</script>')]
    page = (d / shell).read_text().replace('/*__COMPONENT__*/', comp)
    page = page.replace('url(fonts/', 'url(../fonts/').replace("'senat-geo.json'", "'../senat-geo.json'").replace("'house-grid.json'", "'../house-grid.json'")
    p = d.parent / out / 'index.html'; p.parent.mkdir(exist_ok=True); p.write_text(page)
build('results.dc.html', 'shell.html', 'midterms')
build('senat.dc.html', 'shell.html', 'midterms-test')
build('forecast.dc.html', 'shell_forecast.html', 'midterm-forecast')

# Carte de la Chambre seule, pour la page d'accueil (iframe) : carte-chambre/ (état des courses), carte-chambre-resultats/ (résultats)
def build_embed(dc, shell_for_blobs, out):
    blobs = next(l for l in (d / shell_for_blobs).read_text().split('\n') if 'const BLOBS' in l).strip()
    t = (d / 'shell_embed_house.html').read_text().replace('/*__BLOBS__*/', blobs)
    (d / '_embed_tmp.html').write_text(t)
    build(dc, '_embed_tmp.html', out); (d / '_embed_tmp.html').unlink()
    p = d.parent / out / 'index.html'
    p.write_text(p.read_text().replace("'../../", "'../"))
build_embed('forecast.dc.html', 'shell_forecast.html', 'carte-chambre')
build_embed('results.dc.html', 'shell.html', 'carte-chambre-resultats')
# Racine : renvoi vers la page des résultats
(d.parent / 'index.html').write_text('<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Midterms 2026 - Le Grand Continent</title><meta http-equiv="refresh" content="0; url=midterms/"><link rel="canonical" href="midterms/"></head><body><a href="midterms/">Résultats des midterms 2026</a></body></html>\n')
print('ok')
import subprocess; subprocess.run(['node', str(d / 'export_csv.js')], check=True)
# Versions espagnole et italienne des pages résultats et forecast : es/<page>/, it/<page>/
import re, sys
sys.path.insert(0, str(d)); from i18n import translate
for lang in ('es', 'it'):
    for page in ('midterms', 'midterm-forecast'):
        s = (d.parent / page / 'index.html').read_text()
        s = re.sub(r'(["\'(])\.\./', r'\1../../', translate(s, lang))
        p = d.parent / lang / page / 'index.html'; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s)
print('i18n ok')

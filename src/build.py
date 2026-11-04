# Construit les trois pages du site à partir des maquettes du canevas :
#   midterms/           résultats du scrutin (vide tant qu'aucun flux réel n'est branché)
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
build('forecast.dc.html', 'shell_forecast.html', 'midterm-forecast')

# Carte de la Chambre seule, pour la page d'accueil (iframe) : carte-chambre/ (état des courses), carte-chambre-resultats/ (résultats)
def build_embed(dc, shell_for_blobs, out, tpl='shell_embed_house.html', chamber=None):
    blobs = next(l for l in (d / shell_for_blobs).read_text().split('\n') if 'const BLOBS' in l).strip()
    t = (d / tpl).read_text().replace('/*__BLOBS__*/', blobs)
    scn = next((l for l in (d / shell_for_blobs).read_text().split('\n') if 'id="scenarios"' in l), '').strip()
    t = t.replace('/*__SCN__*/', scn)
    if chamber: t = t.replace("/*__CHAMBER__*/'S'", repr(chamber))
    (d / '_embed_tmp.html').write_text(t)
    build(dc, '_embed_tmp.html', out); (d / '_embed_tmp.html').unlink()
    p = d.parent / out / 'index.html'
    p.write_text(p.read_text().replace("'../../", "'../"))
build_embed('forecast.dc.html', 'shell_forecast.html', 'carte-chambre')
build_embed('results.dc.html', 'shell.html', 'carte-chambre-resultats')
# Courses indécises seules + panneau récapitulatif, une iframe par chambre
build_embed('forecast.dc.html', 'shell_forecast.html', 'indecis-senat', 'shell_embed_tossup.html', 'S')
build_embed('forecast.dc.html', 'shell_forecast.html', 'indecis-chambre', 'shell_embed_tossup.html', 'H')
# Bloc « Quatre scénarios pour le Congrès » seul, pour un article (iframe)
build_embed('forecast.dc.html', 'shell_forecast.html', 'scenarios', 'shell_embed_scenarios.html')
# Cartes isolées (iframes) : carte-senat-resultats/ et carte-chambre-resultats-complete/, issues de la page des résultats
def build_isolated(chamber, out):
    t = (d / 'shell.html').read_text()
    a = "startChamber: q.get('chambre') === 'chambre' || q.get('chamber') === 'house' ? 'Chambre' : 'Sénat',"
    assert t.count(a) == 1
    t = t.replace(a, "startChamber: " + repr(chamber) + ",")
    css = ('#app header h1,#app header>p,#app header>span,#app nav[aria-label="Dans cette page"],.thumbs,.tl-side,.tl-below,.seg{display:none!important}'
           '#app header{padding-bottom:10px!important}#app>div>div{padding-top:8px!important;padding-bottom:16px!important}#cartes{padding-top:18px!important;margin-top:18px!important}')
    t = t.replace('</style>', css + '</style>', 1)
    (d / '_iso_tmp.html').write_text(t); build('results.dc.html', '_iso_tmp.html', out); (d / '_iso_tmp.html').unlink()
build_isolated('Sénat', 'carte-senat-resultats')
build_isolated('Chambre', 'carte-chambre-resultats-complete')
# Carte des heures de fermeture des bureaux de vote (page autonome)
(d.parent / 'fermeture').mkdir(exist_ok=True); (d.parent / 'fermeture' / 'index.html').write_text((d / 'fermeture.html').read_text())
# Racine : renvoi vers la page des résultats
(d.parent / 'index.html').write_text('<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Midterms 2026 - Le Grand Continent</title><meta http-equiv="refresh" content="0; url=midterms/"><link rel="canonical" href="midterms/"></head><body><a href="midterms/">Résultats des midterms 2026</a></body></html>\n')
print('ok')
import subprocess; subprocess.run(['node', str(d / 'export_csv.js')], check=True)
# Versions espagnole et italienne des pages résultats et forecast : es/<page>/, it/<page>/
import re, sys
sys.path.insert(0, str(d)); from i18n import translate
for lang in ('es', 'it'):
    for page in ('midterms', 'midterm-forecast', 'carte-chambre', 'carte-chambre-resultats', 'indecis-senat', 'indecis-chambre', 'scenarios', 'fermeture', 'carte-senat-resultats', 'carte-chambre-resultats-complete'):
        s = (d.parent / page / 'index.html').read_text()
        s = re.sub(r'(["\'(])\.\./', r'\1../../', translate(s, lang))
        p = d.parent / lang / page / 'index.html'; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s)
print('i18n ok')

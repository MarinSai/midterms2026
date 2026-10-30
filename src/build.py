# Construit index.html (résultats) et midterm-forecast/index.html (état des courses)
# à partir des maquettes du canevas (src/senat.dc.html, src/forecast.dc.html)
import pathlib
d = pathlib.Path(__file__).parent
def build(dc, shell, outs):
    s = (d / dc).read_text()
    comp = s[s.index('class Component'):s.rindex('</script>')]
    page = (d / shell).read_text().replace('/*__COMPONENT__*/', comp)
    for o in outs:
        p = d.parent / o; p.parent.mkdir(exist_ok=True); p.write_text(page)
build('senat.dc.html', 'shell.html', ['index.html', 'senat.html'])
build('forecast.dc.html', 'shell_forecast.html', ['midterm-forecast/index.html'])
print('ok')

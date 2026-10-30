# Midterms 2026 — Le Grand Continent

Pages des élections de mi-mandat américaines du 3 novembre 2026 (Sénat et Chambre) :

| Adresse | Contenu |
|---|---|
| `midterms/` | Résultats du scrutin. Vide tant qu'aucun flux de résultats réel n'est branché : aucun résultat fictif. |
| `midterms-test/` | Maquette avec résultats fictifs (`?scenario=avant`, `soiree` ou `final` ; `?chambre=chambre`). |
| `midterm-forecast/` | État des courses : classements Cook Political Report et moyennes de sondages Silver Bulletin. |

La racine renvoie vers `midterms/`. Les pages sont générées par `src/build.py` à partir des maquettes `src/*.dc.html`. Données sources : `data/`.

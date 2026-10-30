# Marge d'erreur indicative des fiches de prévision

Source : base brute des sondages Silver Bulletin (« Rawpolls 040626 », 12 350 sondages publiés dans les 21 jours précédant l'élection, 1998-2025),
https://www.natesilver.net/api/v1/file/95ab4b0b-119b-4330-9392-f767d35ad2a7.xlsx (lien sur https://www.natesilver.net/p/pollster-ratings-silver-bulletin), téléchargée le 30 octobre 2026.

Méthode : pour chaque course ayant au moins 3 sondages, moyenne simple de l'écart entre les deux premiers (margin_poll),
puis valeur absolue de la différence avec l'écart réel (margin_actual). Moyenne sur les courses.

| Type | Courses (≥ 3 sondages) | Erreur moyenne de la moyenne | 90e centile | Erreur moyenne d'un sondage isolé |
|---|---|---|---|---|
| Sénat (Sen-G, 1998-2024) | 309 | 4,05 pts | 8,63 pts | 5,05 pts (3 099 sondages) |
| Chambre (House-G, 1998-2025) | 157 | 4,43 pts | 9,60 pts | 5,73 pts (1 877 sondages) |
| Gouverneurs (Gov-G) | 241 | 4,19 pts | 9,27 pts | 5,14 pts |
| Présidentielle (Pres-G) | 252 | 3,53 pts | 7,35 pts | 3,95 pts |

Années de mi-mandat seules (≥ 3 sondages) : Sénat 3,75 pts (148 courses), Chambre 4,08 pts (94 courses).
Valeurs retenues dans les fiches : ±4,1 pts (Sénat), ±4,4 pts (Chambre).

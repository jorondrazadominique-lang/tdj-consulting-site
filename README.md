# TDJ Consulting — site web

Site statique (HTML/CSS/JS pur), hébergé gratuitement sur Vercel : https://tdj-consulting-site.vercel.app

## Structure
- `index.html` — accueil (héros, cartouche, 9 activités, secteurs, méthode, à propos, FAQ, contact)
- `activites/*.html` — une page par activité (servies sans `.html` grâce à `vercel.json`)
- `styles.css` — charte TDJ : noir #08090A, vert armée #57693F, or #C8A868 ; Space Grotesk / Inter / JetBrains Mono ; pas de dégradé ni d'ombre
- `script.js` — menu, onglets des activités, formulaire (e-mail pré-rempli, sujet pré-sélectionné via `?sujet=`)
- `assets/img/` — photos (WebP) générées pour le site, logo optimisé

## Modifier le contenu
Les pages sont générées depuis `_build/content.py` :
```
python3 _build/build.py
```
Règles : aucun tarif affiché (devis sur demande) ; aucune activité solaire / ENR.

Chaque `git push` sur `main` redéploie automatiquement sur Vercel.

# TDJ Consulting — site web

Site statique (HTML/CSS/JS pur, sans framework, sans build). Compatible avec le plan "Vercel + statique" à coût 0 : pas de Next.js nécessaire ici, c'est même plus simple à déployer.

## Fichiers
- `index.html` — page unique (Accueil / Services / À propos / Contact)
- `styles.css` — palette noir & or, typographies Space Grotesk / Inter / JetBrains Mono
- `script.js` — script minimal (année du footer)

## Déploiement sur Vercel (gratuit)

1. Créer un dépôt GitHub et y pousser ce dossier :
   ```
   git init
   git add .
   git commit -m "site TDJ Consulting"
   git branch -M main
   git remote add origin <url-du-repo>
   git push -u origin main
   ```
2. Sur vercel.com → "Add New Project" → importer le dépôt GitHub.
3. Framework Preset : **Other** (aucune commande de build nécessaire, le dossier est déjà statique).
4. Déployer → URL fournie du type `https://tdj-consulting.vercel.app`.

Chaque `git push` redéploie automatiquement.

## Étapes suivantes possibles
- Domaine personnalisé `tdjconsulting.mg` (payant, à ajouter plus tard dans Vercel → Settings → Domains) une fois l'activité validée.
- Formulaire de contact réel via Formspree (gratuit) si un formulaire (plutôt qu'un lien WhatsApp/mailto) est souhaité.
- Ajout du logo final (fichier image) à la place du texte "TDJ" dans le header — actuellement du texte stylé pour rester léger.

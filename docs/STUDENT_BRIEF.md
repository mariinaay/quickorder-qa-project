# Projet — Audit qualité de QuickOrder

## Contexte

Vous êtes une équipe QA avant la mise en production de **QuickOrder**, une plateforme de livraison de repas.

L'application est déjà développée. Votre mission n'est pas de la reconstruire : vous devez **évaluer sa qualité**, trouver les anomalies et déterminer si elle peut être mise en production.

## Objectifs

Vous devez démontrer votre capacité à :

- comprendre un produit existant ;
- identifier les parcours critiques ;
- prioriser les risques ;
- rédiger des cas de test ;
- exécuter une campagne ;
- tester une interface web ;
- tester une API REST ;
- identifier et documenter des anomalies ;
- analyser les résultats ;
- recueillir des retours utilisateurs ;
- proposer des améliorations ;
- revalider les corrections lorsqu'elles sont disponibles.

## Accès

Application : `http://127.0.0.1:5000`

Swagger : `http://127.0.0.1:5000/docs/`

### Accès API avec Swagger

Dans Swagger, cliquer sur **Authorize**, puis saisir dans `X-API-Key` : `quickorder-demo-key`.

Cette clé permet d'exécuter les endpoints API pédagogiques.

Comptes fournis dans la documentation de lancement.

## Travail demandé

### 1. Stratégie de test

Produire une stratégie précisant :

- périmètre ;
- hors périmètre ;
- parcours critiques ;
- risques ;
- types de tests ;
- priorisation risque × impact.

### 2. Cas de test

Écrire au minimum **24 cas de test** :

- 6 nominaux ;
- 6 limites ;
- 6 erreurs ;
- 6 règles métier.

Chaque cas doit contenir au minimum :

- ID ;
- titre ;
- objectif ;
- préconditions ;
- données ;
- étapes ;
- résultat attendu ;
- résultat obtenu ;
- statut.

### 3. Campagne de test

Exécuter les cas et utiliser :

- navigateur ;
- DevTools ;
- Swagger / API ;
- éventuellement Postman ou Bruno.

Les preuves sont attendues lorsque cela est pertinent : capture, vidéo, console, requête ou réponse API.

### 4. Bug reports

Produire au minimum **8 bug reports** réellement reproductibles.

Chaque bug doit contenir :

- titre ;
- contexte ;
- préconditions ;
- étapes ;
- résultat attendu ;
- résultat obtenu ;
- preuve ;
- sévérité ;
- priorité.

### 5. Analyse de campagne

Présenter :

- nombre de tests ;
- Pass ;
- Fail ;
- Blocked ;
- Skipped ;
- principaux risques ;
- recommandation Go / No-Go.

### 6. Tests utilisateurs

Faire réaliser au moins **3 scénarios** par au moins **2 personnes**.

Documenter :

- profil ;
- contexte ;
- problème ;
- fréquence ;
- impact ;
- verbatim ;
- hypothèse d'amélioration ;
- priorité.

### 7. Plan d'amélioration

Proposer au minimum **6 améliorations**, priorisées et justifiées.

## Livrables

Github Repo

```text
quality-audit-team-X/
├── README.md
├── docs/
│   ├── test-strategy.md
│   ├── risk-matrix.md
│   ├── test-cases.xlsx
│   ├── execution-report.md
│   ├── bug-reports/
│   ├── user-feedback.md
│   └── improvement-plan.md
```

## Important

Ne modifiez pas le code source de QuickOrder pendant la campagne initiale. Vous pouvez ensuite proposer des corrections ou des améliorations dans une branche séparée.

Le but est de **prouver** les problèmes, pas de simplement les supposer.

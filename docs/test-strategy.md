## Stratégie de test

1. Périmètre
Sont testés dans cette campagne :
- Le catalogue de restaurants (liste, filtres, recherche)
- La consultation d'un menu (produits, gestion du stock, prix)
- La gestion du panier (ajout, modification de quantité, calcul dynamique du total)
- L'authentification et la gestion des comptes (création, connexion)
- Le processus de commande 
- Le système de promotions et de coupons de réduction
- Les interfaces cibles : Interface Web (UI) et API REST (via Swagger)

2. Hors périmètre
Ne sont pas testés dans cette campagne :
- L'intégration avec de véritables passerelles de paiement bancaire 
- Les tests de sécurité approfondis 

3. Parcours critiques

- Parcours nominal client : Consulter un restaurant → ajouter un produit disponible au panier → se connecter → valider la commande
- Parcours nouveau client : Créer un compte → se connecter → passer une commande
- Parcours promotionnel : Appliquer un coupon de réduction → vérifier l'impact direct sur le calcul du total

4. Risques identifiés
- R1 (Critique) : Le total de la commande peut être mal calculé (erreurs sur les remises, la livraison ou les taxes)
- R2 (Majeur) :Un produit affiché en rupture de stock peut tout de même être ajouté au panier et validé en commande
- R3 (Majeur) : Un coupon annoncé ou saisi ne s'applique pas correctement sur le montant final
- R4 (Majeur) : Absence de règles  sur la structure des mots de passe lors de la création de compte

5. Types de tests utilisés
- Tests fonctionnels : Cas nominaux, cas limites (bornes minimales/maximales), cas d'erreur (données invalides) et règles métier (gestion des stocks, coupons)
- Tests API : Codes de statut (ex: 200, 400, 401) et réponses via Swagger
- Tests End-to-End  : Validation des parcours utilisateurs complets 

6. Priorisation (Matrice Risque × Impact)
- Priorité Haute :Paiement, Panier, Authentification 
- Priorité Moyenne : Gestion du catalogue, recherche et profils
- Priorité Basse : Préférences UI et éléments secondaires
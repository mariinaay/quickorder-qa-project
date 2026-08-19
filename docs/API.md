# QuickOrder — Tester l'API avec Swagger

## 1. Ouvrir Swagger

Lancer l'application puis ouvrir :

**http://127.0.0.1:5000/docs/**

Il n'est pas nécessaire d'ouvrir le fichier OpenAPI séparément.

## 2. Configurer la clé API

QuickOrder utilise une clé API de démonstration pour les appels REST.

Dans Swagger :

1. Ouvrir `http://127.0.0.1:5000/docs/`.
2. En haut à droite, cliquer sur **Authorize**.
3. Dans le champ **X-API-Key**, saisir :

```text
quickorder-demo-key
```

4. Cliquer sur **Authorize**.
5. Fermer la fenêtre.

Les requêtes Swagger enverront alors automatiquement :

```text
X-API-Key: quickorder-demo-key
```

Le compte API de démonstration correspond au client `alice@example.com`.

## 3. Premier test

Commencer par :

`GET /health`

Puis :

`GET /restaurants`

`GET /restaurants/{restaurant_id}/products`

`POST /coupons/validate`

`POST /orders`

## 4. Idées de tests API

Les étudiants doivent notamment tester :

- API key absente ;
- API key incorrecte ;
- ID inexistant ;
- quantité 0 ;
- quantité négative ;
- quantité supérieure au stock ;
- produit hors stock ;
- restaurant fermé ;
- commande sous le minimum ;
- coupon expiré ;
- coupon avec minimum non atteint ;
- modification artificielle du `subtotal` envoyé à `/coupons/validate` ;
- paiement `cash` avec montant insuffisant ;
- paiement PayPal ;
- statuts HTTP ;
- contenu JSON.

## 5. Exemples

### Vérifier un coupon

```json
{
  "code": "WELCOME10",
  "subtotal": 32.50
}
```

### Créer une commande

```json
{
  "items": [
    {"product_id": 1, "quantity": 1}
  ],
  "payment_method": "card"
}
```

### Tester les espèces

```json
{
  "items": [
    {"product_id": 1, "quantity": 1}
  ],
  "payment_method": "cash",
  "cash_received": 1
}
```

Le but est de vérifier si l'application refuse correctement un montant inférieur au total.

# QuickOrder — Installation et lancement

Ce guide part du principe que l'étudiant **n'a encore rien installé**.

## 1. Choisir sa méthode

### Recommandée pour débuter : Docker

Docker permet de lancer QuickOrder sans installer Python ni les dépendances Flask sur la machine. Docker Compose orchestre le service de l'application et son volume de données.

### Alternative : Python + venv

Cette méthode est recommandée si l'étudiant veut développer directement avec Python et comprendre l'environnement du projet.

---

# PARTIE A — Python + environnement virtuel

## 2. Installer Python

### Windows

1. Installer Python 3.12 ou 3.13 depuis le site officiel Python.
2. Pendant l'installation, activer l'option **Add Python to PATH**.
3. Ouvrir PowerShell.
4. Vérifier :

```powershell
py --version
```

Si `py` n'est pas disponible :

```powershell
python --version
```

### macOS

Vérifier d'abord :

```bash
python3 --version
```

Si Python n'est pas installé, installer Python 3.12 ou 3.13 depuis le site officiel Python.

### Linux

Vérifier :

```bash
python3 --version
```

Sur Ubuntu/Debian, si nécessaire :

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

---

## 3. Télécharger le projet

Décompresser le projet, puis ouvrir un terminal dans le dossier :

```text
quickorder/
```

Il doit contenir notamment `run.py`, `seed.py`, `requirements.txt` et `docker-compose.yml`.

---

## 4. Créer le virtual environment

### Windows

```powershell
py -m venv .venv
```

Activer avec PowerShell :

```powershell
.venv\Scripts\Activate.ps1
```

Si PowerShell bloque l'exécution du script :

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Puis recommencer l'activation.

Avec CMD :

```cmd
.venv\Scripts\activate.bat
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Quand l'environnement est actif, le terminal affiche généralement `(.venv)`.

---

## 5. Installer les dépendances

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 6. Préparer la base de données

Pour une installation neuve :

```bash
python seed.py
```

Cette commande crée une base SQLite et des données de démonstration.

⚠️ `seed.py` réinitialise la base locale. Ne pas l'utiliser si vous voulez conserver vos données.

---

## 7. Lancer QuickOrder

```bash
python run.py
```

Ouvrir :

**http://127.0.0.1:5000**

Swagger :

**http://127.0.0.1:5000/docs/**

Pour tester l'API, cliquer sur **Authorize** dans Swagger et saisir la clé : `quickorder-demo-key`.


Arrêter avec `Ctrl+C`.

---

# PARTIE B — Docker + Docker Compose

## 8. Installer Docker

### Windows

Installer Docker Desktop pour Windows puis démarrer Docker Desktop.

Vérifier :

```powershell
docker --version
docker compose version
```

### macOS

Installer Docker Desktop pour Mac puis démarrer Docker Desktop.

Vérifier :

```bash
docker --version
docker compose version
```

### Linux

Installer Docker Engine et Docker Compose Plugin selon la distribution, ou utiliser Docker Desktop si souhaité.

Vérifier :

```bash
docker --version
docker compose version
```

---

## 9. Lancer QuickOrder avec Docker Compose

Depuis le dossier du projet :

```bash
docker compose up --build
```

Le premier lancement peut prendre quelques minutes.

Puis ouvrir :

**http://127.0.0.1:5000**

Swagger :

**http://127.0.0.1:5000/docs/**

Pour tester l'API, cliquer sur **Authorize** dans Swagger et saisir la clé : `quickorder-demo-key`.

---

## 10. Lancer en arrière-plan

```bash
docker compose up -d --build
```

Voir les conteneurs :

```bash
docker compose ps
```

Voir les logs :

```bash
docker compose logs -f
```

Arrêter :

```bash
docker compose down
```

---

## 11. Réinitialiser la base Docker

La base est conservée dans un volume Docker.

Pour supprimer également les données :

```bash
docker compose down -v
docker compose up --build
```

---

# PARTIE C — Problèmes fréquents

## `python` ou `py` n'est pas reconnu

Python n'est probablement pas installé ou n'est pas dans le PATH. Vérifier l'installation puis rouvrir le terminal.

## PowerShell refuse `Activate.ps1`

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## `pip` n'est pas reconnu

Utiliser :

```bash
python -m pip ...
```

ou :

```bash
python3 -m pip ...
```

## `docker compose` n'est pas reconnu

Docker Desktop n'est probablement pas installé, ou Docker n'est pas démarré. Vérifier :

```bash
docker --version
docker compose version
```

## Le port 5000 est déjà utilisé

Sous Windows PowerShell :

```powershell
netstat -ano | findstr :5000
```

Sous macOS/Linux :

```bash
lsof -i :5000
```

Vous pouvez aussi lancer Flask sur un autre port avec :

```bash
PORT=5001 python run.py
```

Sous PowerShell :

```powershell
$env:PORT="5001"
python run.py
```

---

# PARTIE D — Vérification rapide

Après démarrage, vérifier dans cet ordre :

- [ ] `http://127.0.0.1:5000` s'affiche
- [ ] les restaurants sont visibles
- [ ] un menu peut être ouvert
- [ ] un produit peut être ajouté au panier
- [ ] une connexion fonctionne
- [ ] le checkout fonctionne
- [ ] `http://127.0.0.1:5000/docs/` affiche Swagger
- [ ] `http://127.0.0.1:5000/api/health` retourne un JSON avec `status: ok`

# Comptes de démonstration

- Client : `alice@example.com` / `Password123!`
- Client : `bob@example.com` / `Password123!`
- Admin : `admin@quickorder.local` / `Admin123!`

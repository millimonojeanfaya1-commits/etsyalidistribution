# Système de Gestion des Ventes - GestionStock

Un système complet de gestion des ventes développé avec Django, comprenant 8 modules fonctionnels pour gérer tous les aspects d'une entreprise commerciale.

## 🚀 Fonctionnalités

### 📦 Module 1 : Gestion des Fournisseurs
- Enregistrement des fournisseurs
- Suivi des livraisons et coûts d'achat
- Historique des approvisionnements
- Statistiques mensuelles/annuelles

### 💰 Module 2 : Gestion des Ventes
- Enregistrement des ventes (cash/crédit)
- Gestion des clients et magasins
- Chiffre d'affaires journalier/mensuel
- Ventilation par magasin, produit, client

### 💳 Module 3 : Crédits Clients
- Suivi des ventes à crédit
- Gestion des encaissements
- Liste des clients débiteurs
- Taux de recouvrement

### 📊 Module 4 : Gestion des Stocks
- Contrôle des entrées/sorties
- État des stocks en temps réel
- Alertes sur les ruptures
- Inventaires périodiques

### 🚗 Module 5 : Parc Motorisé
- Gestion des véhicules
- Suivi de la consommation de carburant
- Coût total par véhicule
- Prévisions budgétaires

### 👥 Module 6 : Personnel et Salaires
- Gestion des employés
- Paie mensuelle et annuelle
- Masse salariale
- Gestion des congés

### 💸 Module 7 : Gestion des Charges
- Charges fixes et variables
- Budgets annuels
- Comparaison charges vs revenus
- Planification des dépenses

### 📈 Module 8 : Analyse des Profits
- Calcul de rentabilité
- Classement des produits
- Analyse des marges
- Tableaux de bord

## 🛠️ Installation

### Prérequis
- Python 3.8+
- pip
 - Git

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone https://github.com/millimonojeanfaya1-commits/etsyalidistribution.git
cd etsyalidistribution
```

2. **Créer un environnement virtuel** :
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel** :
```bash
# Windows
venv\Scripts\activate
```

4. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

5. **Effectuer les migrations** :
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Créer un superutilisateur** :
```bash
python manage.py createsuperuser
```

7. **Lancer le serveur de développement** :
```bash
python manage.py runserver
```

## 🖼️ Captures d'écran (placeholders)

Ajoutez vos captures d'écran dans un dossier `docs/screenshots/` et référencez-les ici.

Exemples:

![Dashboard](docs/screenshots/dashboard.png)
![Liste des ventes](docs/screenshots/ventes_list.png)
![Stocks](docs/screenshots/stocks.png)

8. **Accéder à l'application** :
   - Interface principale : http://127.0.0.1:8000/
   - Interface d'administration : http://127.0.0.1:8000/admin/

## 📱 Utilisation

### Première connexion
1. Connectez-vous avec le compte superutilisateur créé
2. Accédez à l'interface d'administration pour configurer les données de base :
   - Créer des magasins
   - Ajouter des fournisseurs
   - Enregistrer des produits
   - Configurer les catégories de charges

### Navigation
- **Tableau de bord** : Vue d'ensemble des statistiques
- **Menu latéral** : Accès rapide à tous les modules
- **Actions rapides** : Boutons pour les opérations courantes

### Modules principaux
- Commencez par configurer vos **Fournisseurs** et **Produits**
- Créez vos **Magasins** et **Clients**
- Enregistrez vos **Ventes** et **Livraisons**
- Suivez vos **Stocks** et **Crédits**
- Analysez vos **Profits** et **Charges**

## 🏗️ Architecture

### Structure du projet
```
gestionstock/
├── core/                   # Application principale
├── fournisseurs/          # Gestion des fournisseurs
├── ventes/                # Gestion des ventes
├── credits/               # Crédits clients
├── stocks/                # Gestion des stocks
├── parc_motorise/         # Parc motorisé
├── personnel/             # Personnel et salaires
├── charges/               # Gestion des charges
├── profits/               # Analyse des profits
├── templates/             # Templates HTML
├── static/                # Fichiers statiques
├── media/                 # Fichiers uploadés
└── gestionstock/          # Configuration Django
```

### Technologies utilisées
- **Backend** : Django 4.2.x
- **Frontend** : Bootstrap 5.3, Font Awesome
- **Base de données** : SQLite (développement)
- **Formulaires** : Django Crispy Forms
- **Graphiques** : Chart.js

## 📊 Rapports et Exports

Le système génère automatiquement :
- Rapports de ventes journaliers/mensuels
- Statistiques des fournisseurs
- États des stocks
- Analyses de rentabilité
- Rapports de paie

## 🔧 Configuration

### Base de données
Par défaut, le système utilise SQLite. Pour la production, modifiez `settings.py` pour utiliser PostgreSQL ou MySQL.

### Paramètres régionaux (exemple)
- Langue : Français (fr-fr)
- Fuseau horaire : Africa/Kinshasa
- Devise : GNF

### Authentification GitHub (si vous contribuez)
- Utilisez une clé SSH ou un Personal Access Token (PAT) pour pousser sur GitHub.
- Ajouter le remote (déjà configuré) : `git remote -v`.

## 🚀 Déploiement

Pour déployer en production :
1. Configurez une base de données robuste
2. Modifiez `DEBUG = False` dans settings.py
3. Configurez les fichiers statiques
4. Utilisez un serveur web (Nginx + Gunicorn)

## ⚡ Démarrage rapide

```bash
git clone https://github.com/millimonojeanfaya1-commits/etsyalidistribution.git
cd etsyalidistribution
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 📞 Support

Pour toute question ou assistance :
- Consultez la documentation Django
- Vérifiez les logs d'erreur
- Contactez l'équipe de développement

## 📝 Licence

Ce projet est développé pour un usage interne. Tous droits réservés.

---

**GestionStock** - Système de Gestion des Ventes
Version 1.0 - Développé avec Django

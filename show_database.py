#!/usr/bin/env python
"""
Script pour afficher la structure de la base de données
"""
import os
import django
import sqlite3

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestionstock.settings')
django.setup()

from django.db import connection

def show_database_structure():
    """Afficher la structure de la base de données"""
    print("=" * 60)
    print("STRUCTURE DE LA BASE DE DONNEES - SYSTEME DE GESTION DES VENTES")
    print("=" * 60)
    
    # Connexion à la base de données SQLite
    cursor = connection.cursor()
    
    # Obtenir la liste des tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\nNOMBRE TOTAL DE TABLES: {len(tables)}")
    print("-" * 40)
    
    for table in tables:
        table_name = table[0]
        print(f"\nTABLE: {table_name}")
        
        # Obtenir la structure de chaque table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        print("   Colonnes:")
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            pk_indicator = " (PK)" if pk else ""
            null_indicator = " NOT NULL" if not_null else ""
            default_indicator = f" DEFAULT {default_val}" if default_val else ""
            print(f"   - {col_name}: {col_type}{pk_indicator}{null_indicator}{default_indicator}")
        
        # Compter les enregistrements
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"   Nombre d'enregistrements: {count}")
        except:
            print("   Nombre d'enregistrements: N/A")
    
    print("\n" + "=" * 60)
    print("MODULES DJANGO INSTALLÉS")
    print("=" * 60)
    
    # Afficher les modules par catégorie
    modules = {
        "GESTION COMMERCIALE": [
            "fournisseurs", "ventes", "credits", "stocks"
        ],
        "GESTION OPERATIONNELLE": [
            "parc_motorise", "personnel", "charges"
        ],
        "ANALYSE": [
            "profits"
        ],
        "SYSTEME": [
            "core", "auth", "admin", "sessions", "contenttypes"
        ]
    }
    
    for category, module_list in modules.items():
        print(f"\n{category}:")
        for module in module_list:
            # Vérifier si le module a des tables
            module_tables = [t[0] for t in tables if module in t[0]]
            if module_tables:
                print(f"   OK {module} ({len(module_tables)} tables)")
                for table in module_tables:
                    print(f"      - {table}")
            else:
                print(f"   -- {module} (aucune table trouvee)")

def show_sample_data():
    """Afficher quelques données d'exemple"""
    print("\n" + "=" * 60)
    print("DONNÉES D'EXEMPLE")
    print("=" * 60)
    
    cursor = connection.cursor()
    
    # Vérifier les utilisateurs
    try:
        cursor.execute("SELECT username, email, is_superuser, date_joined FROM auth_user LIMIT 5;")
        users = cursor.fetchall()
        print(f"\nUTILISATEURS ({len(users)}):")
        for user in users:
            username, email, is_super, date_joined = user
            super_indicator = " (ADMIN)" if is_super else ""
            print(f"   - {username}{super_indicator} | {email} | {date_joined}")
    except Exception as e:
        print(f"   ERREUR lors de la lecture des utilisateurs: {e}")

if __name__ == '__main__':
    show_database_structure()
    show_sample_data()
    print("\nLe calcul automatique du total a ete ameliore avec plusieurs evenements:")
    print("   - 'input' : Calcul pendant la frappe")
    print("   - 'keyup' : Calcul apres chaque touche relachee") 
    print("   - 'change': Calcul quand le champ perd le focus")
    print("\nLe total se calcule maintenant en TEMPS REEL des que vous tapez!")

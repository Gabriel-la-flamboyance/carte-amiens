#!/usr/bin/env python3
"""
Générateur d'IDs pour l'application de distribution de flyers.
Seule la personne ayant accès à ce code peut générer des IDs valides.

Usage:
    python generate_ids.py generate <prenom>    - Génère un ID pour un prénom
    python generate_ids.py list                  - Liste tous les IDs générés
    python generate_ids.py delete <id>           - Supprime un ID
    python generate_ids.py reset <id>            - Réinitialise les rues d'un ID (dans Firebase)
"""

import hashlib
import json
import os
import sys
from datetime import datetime

# Clé secrète - NE PAS PARTAGER CE FICHIER
SECRET_KEY = "amiens_flyers_2024_secret_key_xyz789"

# Fichier de stockage des IDs
IDS_FILE = "authorized_ids.json"


def generate_id(prenom: str) -> str:
    """Génère un ID unique à partir d'un prénom."""
    prenom_clean = prenom.strip().lower()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    raw = f"{SECRET_KEY}_{prenom_clean}_{timestamp}"
    hash_value = hashlib.sha256(raw.encode()).hexdigest()[:12]
    return f"{prenom_clean[:3].upper()}{hash_value.upper()}"


def load_ids() -> dict:
    """Charge les IDs depuis le fichier JSON."""
    if os.path.exists(IDS_FILE):
        with open(IDS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"ids": [], "metadata": {}}


def save_ids(data: dict):
    """Sauvegarde les IDs dans le fichier JSON."""
    with open(IDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_id(prenom: str) -> str:
    """Ajoute un nouvel ID pour un prénom."""
    data = load_ids()
    new_id = generate_id(prenom)
    
    id_entry = {
        "id": new_id,
        "prenom": prenom.strip(),
        "created_at": datetime.now().isoformat(),
        "active": True
    }
    
    data["ids"].append(id_entry)
    data["metadata"][new_id] = id_entry
    save_ids(data)
    
    return new_id


def list_ids():
    """Affiche tous les IDs générés."""
    data = load_ids()
    
    if not data["ids"]:
        print("Aucun ID généré pour le moment.")
        return
    
    print("\n" + "="*60)
    print("LISTE DES IDs AUTORISÉS")
    print("="*60)
    
    for entry in data["ids"]:
        status = "✓ Actif" if entry.get("active", True) else "✗ Inactif"
        print(f"\n  Prénom: {entry['prenom']}")
        print(f"  ID: {entry['id']}")
        print(f"  Créé le: {entry['created_at']}")
        print(f"  Status: {status}")
        print("-"*40)
    
    print(f"\nTotal: {len(data['ids'])} ID(s)")
    print("="*60)


def delete_id(id_to_delete: str):
    """Supprime un ID de la liste."""
    data = load_ids()
    
    original_count = len(data["ids"])
    data["ids"] = [entry for entry in data["ids"] if entry["id"] != id_to_delete.upper()]
    
    if id_to_delete.upper() in data["metadata"]:
        del data["metadata"][id_to_delete.upper()]
    
    if len(data["ids"]) < original_count:
        save_ids(data)
        print(f"✓ ID {id_to_delete.upper()} supprimé avec succès.")
    else:
        print(f"✗ ID {id_to_delete} non trouvé.")


def export_for_app():
    """Exporte les IDs pour l'application (à copier dans index.html)."""
    data = load_ids()
    active_ids = [entry["id"] for entry in data["ids"] if entry.get("active", True)]
    
    print("\n" + "="*60)
    print("COPIEZ CETTE LISTE DANS index.html (variable AUTHORIZED_IDS):")
    print("="*60)
    print(f"\nconst AUTHORIZED_IDS = {json.dumps(active_ids)};")
    print("\n" + "="*60)


def print_usage():
    """Affiche l'aide."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║        GÉNÉRATEUR D'IDs - Distribution de Flyers Amiens        ║
╚════════════════════════════════════════════════════════════════╝

COMMANDES DISPONIBLES:

  python generate_ids.py generate <prenom>
      → Génère un nouvel ID pour le prénom donné
      → Exemple: python generate_ids.py generate Marie
  
  python generate_ids.py list
      → Affiche tous les IDs générés
  
  python generate_ids.py delete <id>
      → Supprime un ID de la liste des autorisés
      → Exemple: python generate_ids.py delete MAR1A2B3C4D5E
  
  python generate_ids.py export
      → Exporte les IDs pour les copier dans l'application

NOTES:
  - Seuls les IDs générés par ce script fonctionneront dans l'app
  - Le fichier authorized_ids.json contient tous les IDs
  - Ne partagez JAMAIS ce script ou le fichier JSON
  - Les collègues n'ont besoin que de leur ID pour se connecter
""")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == "generate":
        if len(sys.argv) < 3:
            print("Erreur: Veuillez fournir un prénom.")
            print("Usage: python generate_ids.py generate <prenom>")
            return
        
        prenom = " ".join(sys.argv[2:])
        new_id = add_id(prenom)
        
        print("\n" + "="*50)
        print("✓ NOUVEL ID GÉNÉRÉ AVEC SUCCÈS")
        print("="*50)
        print(f"\n  Prénom: {prenom}")
        print(f"  ID: {new_id}")
        print(f"\n  → Donnez cet ID à {prenom} pour qu'il/elle")
        print("    puisse se connecter à l'application.")
        print("\n  ⚠ N'oubliez pas de mettre à jour l'application")
        print("    avec 'python generate_ids.py export'")
        print("="*50)
    
    elif command == "list":
        list_ids()
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Erreur: Veuillez fournir l'ID à supprimer.")
            print("Usage: python generate_ids.py delete <id>")
            return
        delete_id(sys.argv[2])
    
    elif command == "export":
        export_for_app()
    
    else:
        print(f"Commande inconnue: {command}")
        print_usage()


if __name__ == "__main__":
    main()

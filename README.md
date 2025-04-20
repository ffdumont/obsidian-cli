# obsidian-cli

## 🎯 Objectif

`obsidian-cli` est un outil en ligne de commande (CLI) écrit en Python, destiné à gérer automatiquement un ensemble de notes Obsidian structurées. Il permet de créer, classifier, lier, et scanner les notes Markdown en utilisant une configuration personnalisée basée sur des fichiers JSON.

## 📦 Fonctionnalités principales

- ✅ Création de notes selon un type (`area`, `project`, `task`, etc.) avec modèles et nommage configurables
- 🔗 Indexation automatique des liens (parent, sibling, etc.) dans un fichier `uuid_index.json`
- 🧠 Vérification de la cohérence des types via frontmatter YAML
- 🗂️ Utilisation d’un fichier `classification.txt` pour enrichir les noms de fichiers avec des classifieurs
- 📁 Organisation hiérarchique des notes avec des chemins spécifiques par type
- 🧪 Génération de tests unitaires et artefacts inspectables
- 🧼 Commande `clean` pour nettoyer les artefacts temporaires

## 📂 Structure du projet

```bash
obsidian-cli/
├── obsidian_cli/
│   ├── main.py            # Point d'entrée CLI (Typer)
│   ├── create.py          # Commande de création de note
│   ├── scan.py            # Commande de scan du vault
│   ├── link.py            # Gestion des liens entre notes
│   ├── utils.py           # Fonctions utilitaires
│   └── helpers/           # Fonctions de support (naming, frontmatter, etc.)
│
├── tests/
│   ├── test_create.py     # Tests pour la commande `create`
│   ├── test_scan.py       # Tests pour la commande `scan`
│   └── test_link.py       # Tests pour la commande `link`
│
├── configs/
│   └── home_config.json   # Configuration de structure pour le contexte "home"
│
├── config.json            # Configuration principale du vault
├── uuid_index.json        # Index UUID → métadonnées (type, liens, etc.)
├── classification.txt     # Fichier de classifieurs utilisés pour le nommage
└── README.md              # Ce fichier
```

## ⚙️ Exemple de configuration (`config.json`)

```json
{
  "structure": ["area", "project", "task"],
  "structurePaths": {
    "area": "01-Areas",
    "project": "03-Projects",
    "task": "04-Tasks"
  },
  "namingPattern": {
    "area": "{title}",
    "project": "[{classifier}] {title}",
    "task": "{yyMM}-{title}"
  },
  "templateMapping": {
    "area": "Area.md",
    "project": "Project.md",
    "task": "Task.md"
  },
  "templatesLocation": "!5-Resources/0200 Gestion du Système d'Information/0270 Modèles",
  "classificationPath": "classification.txt"
}
```

## 🧠 Exemple de frontmatter YAML dans une note

```yaml
---
uuid: 123e4567-e89b-12d3-a456-426614174000
type: project
classifier: 1000
parent: dca28d93-1e58-4c68-8a9a-b5d891c9e7e0
---
```

## 🛠️ Utilisation typique

```bash
# Créer une note de type "project"
obsidian-cli create --type project --title "Numérisation des documents"

# Scanner le vault et mettre à jour l’index
obsidian-cli scan

# Lier une note à une autre
obsidian-cli link --source <uuid1> --target <uuid2> --relation parent
```

## 🧪 Tests

Tous les tests sont basés sur `pytest` et créent des artefacts inspectables : fichiers temporaires, index JSON simulés, etc.  
Commande recommandée :

```bash
pytest --capture=no
```

Nettoyage des artefacts :

```bash
obsidian-cli make clean
```

## 🧭 Prochaines étapes (roadmap technique)

- [ ] Finaliser la commande `create` avec gestion de l'ontologie depuis la config

---

## 🧱 Architecture technique

```
                          +----------------------+
                          |    config.json       |
                          | structure, naming... |
                          +----------+-----------+
                                     |
                                     v
                           +---------+--------+
                           |   main.py (Typer) |
                           +---------+--------+
                                     |
           +-------------------------+----------------------------+
           |                         |                            |
           v                         v                            v
    create.py                scan.py                      link.py
 (création de note)    (analyse du vault)        (relations entre notes)
           |                         |                            |
           +----------+     +--------+----------+        +--------+--------+
                      |     |                   |        |                 |
                helpers/   utils.py        uuid_index.json        classification.txt
                (naming,  (IO, parsing,     (stocke les         (classifieurs utilisés
                frontmatter) templates...)   métadonnées UUID)    dans les noms)
```

---

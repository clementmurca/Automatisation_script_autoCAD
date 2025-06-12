# Automatisation_script_autoCAD
Un générateur de scripts AutoCAD qui automatise la création de scripts en utilisant des données extraites d'un fichier TXT et un système de templates personnalisables.

📋 Description
Ce projet permet de générer automatiquement des scripts AutoCAD (.scr) en combinant :

Des données extraites d'un fichier TXT au format CSV

Des variables système récupérées depuis le registre Windows

Un template de script AutoCAD personnalisable

🏗️ Architecture du projet
text
projet/
├── Extract_data_csv/
│   └── extract.txt          # Fichier de données source
├── Template/
│   └── gabarit_autoCAD.txt  # Template de script AutoCAD
├── Output_folder/
│   └── script_autocad.scr   # Script généré
└── main.py                  # Code principal
⚙️ Fonctionnalités
Lecture de données
Charge un fichier TXT formaté en CSV avec un séparateur personnalisable (par défaut ;)

Extrait spécifiquement le champ 5 (CBER_REF) de chaque ligne

Gestion d'erreurs robuste avec messages informatifs

Intégration registre Windows
Lit automatiquement les variables CBER_DATE et CBER_NR depuis le registre AutoCAD

Chemin registre : HKEY_CURRENT_USER\Software\appdatalow\software\Autodes\AutoCAD LT\R30\CoreUser\BlockPreviewUser\FixedProfile\General

Gestion des erreurs si les clés n'existent pas

Génération de scripts
Utilise un système de templates avec variables remplaçables

Variables disponibles : {CBER_REF}, {CBER_DATE}, {CBER_NR}

Génère un script pour chaque ligne de données

Sortie au format .scr compatible AutoCAD

🚀 Installation et utilisation
Prérequis
Python 3.6+

Windows (pour l'accès au registre)

AutoCAD ou AutoCAD LT installé

Utilisation
Préparer les fichiers :

Placer vos données dans Extract_data_csv/extract.txt

Créer votre template dans Template/gabarit_autoCAD.txt

Format du fichier de données :

text
col1;col2;col3;col4;CBER_REF;col6
data1;data2;data3;data4;REF001;data6
data1;data2;data3;data4;REF002;data6
Format du template :

text
COMMAND1 {CBER_REF}
COMMAND2 {CBER_DATE}
COMMAND3 {CBER_NR}
Exécuter le script :

bash
python main.py
📁 Structure des dossiers
Extract_data_csv/
Contient le fichier extract.txt avec les données à traiter. Le fichier doit être au format CSV avec le séparateur ; et la référence dans la 5ème colonne.

Template/
Stocke le fichier gabarit_autoCAD.txt qui sert de modèle pour la génération des scripts. Utilisez les variables {CBER_REF}, {CBER_DATE}, et {CBER_NR} pour l'injection de données.

Output_folder/
Répertoire de sortie où sera généré le fichier script_autocad.scr final.

🔧 Configuration
Personnalisation du séparateur
python
generator = AutoCADScriptGenerator(txt_file, separator=',')  # Utiliser virgule
Modification des chemins
python
txt_file = "votre_chemin/extract.txt"
template_file = "votre_chemin/template.txt"
output_file = "votre_chemin/output.scr"
📝 Exemple de sortie
Le script génère des messages de progression détaillés :

text
🚀 Starting AutoCAD script generation from TXT file
✅ TXT file loaded: 10 rows
✅ Registry CBER_DATE: 2025-06-12
✅ Registry CBER_NR: 12345
Processing row 1/10
  CBER_REF: REF001
✅ Script generated: Output_folder/script_autocad.scr
⚠️ Gestion d'erreurs
Fichier TXT manquant : Message d'erreur explicite

Clés registre absentes : Valeurs par défaut [KEY_NOT_FOUND]

Template invalide : Arrêt avec message d'erreur

Colonnes insuffisantes : Valeur [MISSING_REF] utilisée

🔍 Débogage
Le script affiche automatiquement :

Les 3 premières lignes du fichier de données

Les valeurs extraites du registre

Le progrès de traitement ligne par ligne

Les erreurs rencontrées avec détails

Cet outil s'intègre parfaitement dans un workflow d'automatisation DevOps pour la génération de scripts CAO

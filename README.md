# BhilNet - Chat Terminal Réseau Local

Une application de messagerie pour terminal fonctionnant sur réseau local.

## Fonctionnalités

- Découverte automatique des utilisateurs via broadcast UDP
- Messagerie privée et de groupe via TCP
- Mise à jour en temps réel de la liste des utilisateurs
- Chiffrement AES des messages
- Interface terminal claire et intuitive
- Architecture multi-thread

## Installation

### Démarrage Rapide
```bash
# Cloner et configurer
git clone https://github.com/7Bhil/BhilNet.git
cd BhilNet
./setup_dev.sh

# Lancer l'application
source venv/bin/activate
python main.py
```

### Installation Manuelle
```bash
# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

## Utilisation

1. Lancez l'application sur plusieurs machines du même réseau local
2. Choisissez un pseudo lorsque demandé
3. Visualisez les utilisateurs connectés et envoyez des messages

## Usage

1. Run the application on multiple machines in the same LAN
2. Choose a username when prompted
3. View connected users and send messages

## Architecture

- `main.py` - Point d'entrée et application principale
- `network/` - Modules de communication réseau
- `discovery/` - Service de découverte d'utilisateurs
- `messaging/` - Gestion des messages
- `ui/` - Interface terminal
- `crypto/` - Utilitaires de chiffrement
- `config_manager.py` - Gestion de la configuration
- `sound_manager.py` - Notifications sonores
- `user_status.py` - Gestion des statuts utilisateur
- `utils/` - Helper functions

## Support des Plateformes

- **Linux** ✅ - Pleinement supporté et testé
- **Windows** ⚠️ - Supporté avec modifications mineures
- **macOS** ⚠️ - Supporté avec modifications mineures

### Configuration Windows/macOS

1. Installez Python 3.8+ depuis python.org
2. Installez les dépendances : `pip install -r requirements.txt`
3. Lancez : `python main.py`

Pour les utilisateurs Windows, vous devrez peut-être :
- Autoriser Python dans le pare-feu Windows
- Exécuter l'invite de commande en tant qu'administrateur

## Développeur

**Développé par Bhilal CHITOU (Bhil€)**

- **Email** : 7bhilal.chitou7@gmail.com
- **GitHub** : https://github.com/7Bhil
- **Projet** : https://github.com/7Bhil/BhilNet

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Remerciements

Merci à tous les contributeurs et utilisateurs de BhilNet !

---

**BhilNet v1.0** - *Créé avec ❤️ par Bhilal CHITOU*

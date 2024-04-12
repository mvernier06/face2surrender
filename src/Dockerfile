# Utiliser une image de base Python 3.8
FROM python:3.9-slim-buster

# Définir le répertoire de travail dans le conteneur Docker
WORKDIR /app

# Copier les fichiers de dépendances dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code dans le répertoire de travail
COPY . .

# Exposer le port sur lequel l'application s'exécute
EXPOSE 8080

# Définir la commande pour exécuter l'application
CMD ["python", "serveur.py"]
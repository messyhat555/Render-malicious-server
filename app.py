#Of course i used AI

import os
from flask import Flask, render_template_string, request, send_from_directory

app = Flask(__name__)

# Dossier où les fichiers seront stockés temporairement
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Le HTML de ta page d'accueil (très basique pour l'exemple)
HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head><title>DropBox Pro - Transfert</title></head>
<body>
    <h2>Déposez votre script de configuration (.txt ou .py)</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file_upload">
        <input type="submit" value="Envoyer et Analyser">
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_INTERFACE

@app.route('/upload', method=['POST'])
def upload():
    file = request.files['file_upload']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # --- LE HACK : Modification du fichier ---
        # On ouvre le fichier en mode "append" (ajout à la fin)
        with open(filepath, "a") as f:
            f.write("\n\n# --- SYSTEM CHECK ---\n")
            f.write("print('ALERTE : Ce fichier a été modifié par le serveur !')\n")
            f.write("# Ici, un vrai hacker mettrait un reverse shell.\n")

        return f"Fichier reçu et analysé ! <a href='/download/{file.filename}'>Cliquez ici pour le récupérer</a>"
    return "Erreur lors de l'upload."

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)

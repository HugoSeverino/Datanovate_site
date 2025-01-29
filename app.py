from flask import Flask,request, render_template, jsonify, send_from_directory
import subprocess
import hmac
import hashlib
from secret import GITHUB_TOKEN
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import os

app = Flask(__name__)



def verify_signature(request):
    # Obtenir la signature de l’en-tête
    signature = request.headers.get('X-Hub-Signature-256')
    if signature is None:
        print("Erreur : Signature absente dans l'en-tête")
        return False

    # Calculer le hash HMAC de la charge utile
    mac = hmac.new(GITHUB_TOKEN.encode(), msg=request.data, digestmod=hashlib.sha256)
    expected_signature = 'sha256=' + mac.hexdigest()

    # Comparer les signatures pour vérifier l'authenticité
    return hmac.compare_digest(expected_signature, signature)



@app.route('/update-server', methods=['POST'])
def webhook():
    # Vérifie la signature pour sécuriser l'accès
    if not verify_signature(request):
        return 'Accès non autorisé', 403

    try:
        # Exécute `git pull` si la vérification est réussie
        result_git = subprocess.run(
            ['/usr/bin/git', 'pull'], 
            cwd='/root/Datanovate_site', 
            capture_output=True, text=True
        )
        print("Résultat de git pull :", result_git.stdout)
        if result_git.returncode != 0:
            return f"Erreur lors de git pull : {result_git.stderr}", 500

        # Redémarre l'application avec un script différé
        subprocess.Popen(['/root/Datanovate_site/restart_service.sh'])
        return 'Mise à jour effectuée et service redémarré', 200
    except Exception as e:
        print(f"Erreur lors de la mise à jour : {e}")
        return f"Erreur lors de la mise à jour : {e}", 500
    
#@app.route('/favicon.ico')
#def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    return render_template('general.html', current_page='index')

@app.route('/save_drawing', methods=['POST'])
def save_drawing():
    data = request.json.get('image')
    _, encoded = data.split(",", 1)
    # Décoder l'image base64
    image_data = base64.b64decode(encoded)
    img = Image.open(BytesIO(image_data))
    img.save("static/img/chiffre.png")
    img = img.resize((28,28), Image.NEAREST)
    img = img.convert("1")
    img.save("static/img/chiffre_norm.png")
    np_img = np.array(img)
    # IA
    return jsonify({'message': '/static/img/chiffre.png'})

@app.route('/<page>/')
def render_page(page):
    return render_template('general.html', current_page=page)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('general.html', current_page='erreur', error=404), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('general.html', current_page='erreur', error=500), 500


if __name__ == '__main__':
    app.run(debug=True)
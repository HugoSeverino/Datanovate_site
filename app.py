from flask import Flask, render_template
import subprocess
import hmac
import hashlib

app = Flask(__name__)

# Ton secret, pour vérifier les requêtes (même valeur que celle définie dans le webhook)
SECRET_TOKEN = "ton_secret_token"

def verify_signature(request):
    signature = 'sha256=' + hmac.new(
        key=SECRET_TOKEN.encode(),
        msg=request.data,
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, request.headers.get('X-Hub-Signature-256'))

@app.route('/update-server', methods=['POST'])
def webhook():
    # Vérifie la signature pour sécuriser l'accès
    if not verify_signature(request):
        return 'Accès non autorisé', 403

    # Si la requête est valide, lance un git pull
    try:
        subprocess.run(['git', 'pull'], cwd='/root/Datanovate_site')
        # Redémarrer le service
        subprocess.run(['sudo', 'systemctl', 'restart', 'datanovate_flask'])  # Remplace 'my_flask_app' par ton nom de service
        return 'Mise à jour effectuée et service redémarré', 200
    except Exception as e:
        print(f"Erreur : {e}")
        return 'Erreur lors de la mise à jour', 500
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
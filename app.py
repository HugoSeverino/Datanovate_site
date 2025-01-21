from flask import Flask,request, render_template
import subprocess
import hmac
import hashlib
from secret import GITHUB_TOKEN

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
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ia_reconnaissance_chiffre')
def ia():
    return render_template('ia_reconnaissance_chiffre.html')

if __name__ == '__main__':
    app.run(debug=True)
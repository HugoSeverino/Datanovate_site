from flask import Flask,request, render_template
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
    try:
        result_git = subprocess.run(
            ['/usr/bin/git', 'pull'], 
            cwd='/root/Datanovate_site', 
            capture_output=True, text=True
        )
        print("Résultat de git pull :", result_git.stdout)
        if result_git.returncode != 0:
            return f"Erreur lors de git pull : {result_git.stderr}", 500
        
        # Appelle le script de redémarrage en arrière-plan
        subprocess.Popen(['/root/Datanovate_site/restart_service.sh'])
        return 'Mise à jour effectuée et service redémarré', 200
    except Exception as e:
        print(f"Erreur lors de la mise à jour : {e}")
        return f"Erreur lors de la mise à jour : {e}", 500
    
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
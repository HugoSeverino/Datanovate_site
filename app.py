from flask import Flask,request, render_template, jsonify, send_from_directory
import subprocess
import hmac
import hashlib
from secret import GITHUB_TOKEN
import os
import models.model as md
import services.image_processing as img_p
import fcntl

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
    if not verify_signature(request):
        return 'Accès non autorisé', 403

    try:
        # Chemins vers les fichiers ONNX
        MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
        MODEL_PATH = os.path.join(MODEL_DIR, "model.onnx")
        OTHER_MODEL_PATH = os.path.join(MODEL_DIR, "other_output_model.onnx")

        # 1. Verrouiller les fichiers
        with open(MODEL_PATH, "rb") as f1:
            fcntl.flock(f1, fcntl.LOCK_EX)
            with open(OTHER_MODEL_PATH, "rb") as f2:
                fcntl.flock(f2, fcntl.LOCK_EX)

                # 2. Git pull
                result_git = subprocess.run(
                    ['/usr/bin/git', 'pull'],
                    cwd='/root/Datanovate_site',
                    capture_output=True, text=True
                )
                if result_git.returncode != 0:
                    return f"Erreur Git : {result_git.stderr}", 500

                # 3. Changer les permissions
                subprocess.run(["chmod", "644", MODEL_PATH])
                subprocess.run(["chmod", "644", OTHER_MODEL_PATH])

        # 4. Redémarrer le service
        subprocess.Popen(['/root/Datanovate_site/restart_service.sh'])
        return 'Mise à jour effectuée et service redémarré', 200

    except Exception as e:
        print(f"Erreur lors de la mise à jour : {e}")
        return f"Erreur lors de la mise à jour : {e}", 500
    
@app.route('/favicon.ico/')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'img/favicon.ico')

@app.route('/')
def home():
    return render_template('general.html', current_page='index')

@app.route('/save_drawing', methods=['POST'])
def save_drawing():
    data = request.json.get('image')
    _, encoded = data.split(",", 1)

    # Décoder l'image base64
    np_img, enlarged_base64 = img_p.encoded_to_array(encoded)
    
    predict, predict_probas = md.predict(np_img)

    other_outputs = md.predict_reshape(np_img)

    first_conv_pool = img_p.array_to_base64(other_outputs[0][0][1], 5)
    second_conv_pool = img_p.array_to_base64(other_outputs[1][0][1], 5)
    third_conv_pool = img_p.array_to_base64(other_outputs[2][0][1], 5)
    after_reshape = img_p.array_to_base64(other_outputs[3][0])

    return jsonify({'predict': int(predict), 
                    'predict_probas': predict_probas.tolist(),
                    'images': {
                        'enlarged': enlarged_base64,
                        'first_conv_pool': first_conv_pool,
                        'second_conv_pool': second_conv_pool,
                        'third_conv_pool': third_conv_pool,
                        'after_reshape': after_reshape
                    }
                })

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
